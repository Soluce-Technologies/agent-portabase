

def get_file_extension(db_type: str) -> str | None:
    match db_type:
        case "postgresql":
            return ".dump"
        case "mysql":
            return ".sql"