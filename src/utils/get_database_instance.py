from utils.get_databases_config import get_databases_config, DatabaseConfig
from utils.postgres import PostgresDatabase


def get_database_instance(db_type: str, generated_id: str, method: str):
    databases, result = get_databases_config()
    database: DatabaseConfig = next(
        (db for db in databases.databases if db.generatedId == generated_id and db.type == db_type), None)

    if database:
        match db_type:
            case 'postgresql':
                return PostgresDatabase(database.host, database.name, database.username, database.password,
                                        str(database.port), generated_id, method)

    else:
        return None
