from celery import shared_task
import logging
import os
from settings import config
from utils.edge_key import decode_edge_key, EdgeKey
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger('agent_logger')


#  Old method : to keep
# @shared_task()
# def send_result_backup(file_path: str, generated_id: str, result: str, method: str):
#     logger.info("Starting task : Sending result backup")
#     try:
#         edge_key = config.EDGE_KEY
#         edge_key_data, status = decode_edge_key(edge_key)
#         url = f"{edge_key_data.serverUrl}/api/agent/{edge_key_data.agentId}/backup"
#         logger.info(f'Status request | {url}')
#
#         form_data = {
#             "generatedId": (None, generated_id),  # Use (None, value) for non-file fields
#             "status": (None, result),
#             "method": (None, method),
#         }
#
#         if file_path:  # Check if file_path is not an empty string
#             form_data["file"] = (f"{generated_id}.dump", open(file_path, "rb"), "application/octet-stream")
#         else:
#             form_data["file"] = (None, "")  # Use an empty value instead of a file
#
#         print(form_data)
#
#         response = requests.post(url=url, files=form_data)
#         response.raise_for_status()
#         message = response.json()
#         logger.info(f'Successfully sent result backup')
#         return {"message": message, "result": True}
#
#     except Exception as e:
#         message = f"Error sending result backup: {e}"
#         logger.error(message)
#         return {"message": message, "result": False}

@shared_task()
def send_result_backup(file_path: str, generated_id: str, result: str, method: str):
    logger.info("Starting task : Sending result backup")
    try:
        edge_key = config.EDGE_KEY
        edge_key_data, status = decode_edge_key(edge_key)
        url = f"{edge_key_data.serverUrl}/api/agent/{edge_key_data.agentId}/backup"
        logger.info(f'Status request | {url}')

        form_data = {
            "generatedId": (None, generated_id),  # Use (None, value) for non-file fields
            "status": (None, result),
            "method": (None, method),
        }

        # Load server public key
        # with open("/app/server_public.pem", "rb") as f:
        #     server_pub = serialization.load_pem_public_key(f.read())
        server_pub = serialization.load_pem_public_key(edge_key_data.publicKey.encode("utf-8"))

        aes_key = os.urandom(32)  # 256-bit key, AES key

        # Encrypt dump with AES (CBC mode)
        iv = os.urandom(16)
        with open(file_path, "rb") as f:
            data = f.read()

        # PKCS7 padding
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_dump = encryptor.update(padded_data) + encryptor.finalize()

        # Encrypt AES key with server public RSA key
        encrypted_key = server_pub.encrypt(
            aes_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        if file_path:  # Check if file_path is not an empty string
            # form_data["file"] = (f"{generated_id}.dump", open(file_path, "rb"), "application/octet-stream")
            form_data["file"] = (f"{generated_id}.enc", encrypted_dump, "application/octet-stream")
        else:
            form_data["file"] = (None, "")  # Use an empty value instead of a file

        data = {
            "aes_key": encrypted_key.hex(),  # send as hex
            "iv": iv.hex()
        }

        # print(form_data)
        # print(data)

        response = requests.post(url=url, files=form_data, data=data)
        response.raise_for_status()
        message = response.json()
        logger.info(f'Successfully sent result backup')
        return {"message": message, "result": True}

    except Exception as e:
        message = f"Error sending result backup: {e}"
        logger.error(message)
        return {"message": message, "result": False}


@shared_task()
def send_result_restoration(generated_id: str, result: str):
    logger.info("Starting task : Sending result restoration")

    try:
        edge_key = config.EDGE_KEY
        edge_key_data, status = decode_edge_key(edge_key)
        url = f"{edge_key_data.serverUrl}/api/agent/{edge_key_data.agentId}/restore"
        logger.info(f'Status request | {url}')
        data = {
            "generatedId": generated_id,
            "status": result,
        }
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        message = response.json()
        logger.info(f'Successfully sent result restore')
        return {"message": message, "result": True}

    except Exception as e:
        message = f"Error sending result restore: {e}"
        logger.error(message)
        return {"message": message, "result": False}
