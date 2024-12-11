def get_nested_value(data, *keys):
    """
    Retrieves a nested value from a dictionary.

    Args:
    - data (dict): The dictionary to search.
    - *keys (str): Variable number of keys to traverse.

    Returns:
    - The nested value if found, otherwise None.
    """
    for key in keys:
        data = data.get(key)
        if data is None:
            break
    return data
