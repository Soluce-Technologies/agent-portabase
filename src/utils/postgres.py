import subprocess

from utils.database import Database
import uuid


class PostgresDatabase(Database):
    def __init__(self, host: str, database: str, user: str, password: str, port: str):
        super().__init__(host, database, user, password, port, type="postgresql")

        self.backup_file = f"src/files/{uuid.uuid4()}.dump"

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
