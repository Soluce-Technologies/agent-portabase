import logging
import subprocess


logger = logging.getLogger('agent_logger')



class Database:
    def __init__(self, host: str, database: str, user: str, password: str, port: str, type: str):
        """
        Initialize the Database instance.

        :param host: Database host.
        :param database: Database name.
        :param user: Username.
        :param password: Password.
        :param port: Port number.
        """
        self.connection_params = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
            "type": type
        }


    @staticmethod
    def execute(command):
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Automatically decode bytes to strings
            )

            # Stream stdout and stderr in real time
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    logging.info(stdout_line.strip())
                if stderr_line:
                    logging.info(stderr_line.strip())

                # Break if both streams are closed and the process is complete
                if not stdout_line and not stderr_line and process.poll() is not None:
                    break

            # Check process return code
            if process.returncode != 0:
                return False, f"Command failed with return code {process.returncode}"
            return True, "Command executed successfully"

        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            return False, f"Error: Exception during execution - {e}"