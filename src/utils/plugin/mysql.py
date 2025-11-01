import os
from settings import config
from utils.database import Database


class MySQLDatabase(Database):
    def __init__(self, host: str, database: str, user: str, password: str, port: str, generated_id: str, method: str):
        super().__init__(host, database, user, password, port, generated_id, method, type="mysql")

        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self.backup_file = f"{config.DATA_PATH}/files/backups/{method}/{generated_id}.sql"
        self.restore_file = f"{config.DATA_PATH}/files/restorations/{generated_id}.sql"
        self.password = password

        self.command_backup = [
            'mysqldump',
            f'--host={host}',
            f'--port={port}',
            f'--user={user}',
            f'--password={password}',
            '--routines',
            '--events',
            '--triggers',
            '--single-transaction',
            '--quick',
            '--add-drop-database',
            '--verbose',
            '--databases', database,
            '-r', self.backup_file
        ]

        self.command_restore = [
            'mysql',
            f'--host={host}',
            f'--port={port}',
            f'--user={user}',
            f'--password={password}',
            # To confirm if interesting
            # '--verbose',
            database
        ]

        self.command_ping = [
            'mysqladmin',
            f'--host={host}',
            f'--port={port}',
            f'--user={user}',
            f'--password={password}',
            'ping'
        ]

    def backup(self):
        status, result = self.execute(self.command_backup)
        return status, result, self.backup_file

    def restore(self):
        env = os.environ.copy()
        env["MYSQL_PWD"] = self.password

        # Drop and recreate the database before restoring
        drop_create_cmd = [
            'mysql',
            f'--host={self.host}',
            f'--port={self.port}',
            f'--user={self.user}',
            f'--password={self.password}',
            '-e',
            f"DROP DATABASE IF EXISTS {self.database}; CREATE DATABASE {self.database};"
        ]
        self.execute(drop_create_cmd, env=env)

        with open(self.restore_file, 'r') as sql_file:
            restore_cmd = self.command_restore.copy()
            return self.execute(restore_cmd, env=env, input_content=sql_file.read())

    def ping(self):
        return self.execute(self.command_ping)
