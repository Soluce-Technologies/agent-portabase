import subprocess

from settings import config
from utils.database import Database
import uuid


class PostgresDatabase(Database):
    def __init__(self, host: str, database: str, user: str, password: str, port: str, generated_id: str):
        super().__init__(host, database, user, password, port, generated_id, type="postgresql")

        self.backup_file = f"{config.DATA_PATH}/files/{generated_id}.dump"

        self.command_restore = ['pg_restore',
                                '--no-owner',
                                '--clean',
                                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database),
                                '-v',
                                self.backup_file]

        self.command_backup = ['pg_dump',
                               '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database),
                               '-Fc',
                               '-f', self.backup_file,
                               '-v']

        self.command_ping = [
            'pg_isready',
            '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
        ]

    def backup(self):
        status, result = self.execute(self.command_backup)
        return status, result, self.backup_file

    def restore(self):
        return self.execute(self.command_restore)

    def ping(self):
        return self.execute(self.command_ping)
