import subprocess


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
            # Execute the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if process.returncode != 0:
                # Return failure and include the error message
                return False, f"Error: {error.decode('utf-8')} - {output.decode('utf-8')}"
            else:
                return True, output.decode('utf-8')

        except Exception as e:
            print(f"Exception occurred: {e}")
            return False, "Error: Exception during execution"
