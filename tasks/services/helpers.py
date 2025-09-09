# write a method to validate a field is empty or not, return boolean
def validate_not_empty(input_value):
    if input_value is None:
        return False
    if isinstance(input_value, str) and input_value.strip() == "":
        return False
    return True


# write a method to validate a string inout type inside, return boolean
def validate_string_input(input_value):
    if validate_not_empty(input_value) and isinstance(input_value, str):
        return True
    return False


# write a method to validate a dateTime input type inside, return boolean
def validate_dateTime_input(input_value):
    from datetime import datetime
    if validate_not_empty(input_value):
        try:
            datetime.fromisoformat(input_value)
            return True
        except ValueError:
            return False
    return False


# validate a list format
def validate_list_input(input_value):
    if validate_not_empty(input_value) and isinstance(input_value, list):
        return True
    return False


# validate UUID format
def validate_uuid_input(input_value):
    import uuid
    if validate_not_empty(input_value):
        try:
            uuid_obj = uuid.UUID(input_value, version=4)
            return str(uuid_obj) == input_value
        except ValueError:
            return False
    return False


#  create a method to convert string "09.09.2025" to dateTime format
def convert_string_to_dateTime(date_string):
    from datetime import datetime
    if date_string is None:
        return None
    try:
        return datetime.strptime(date_string, "%d.%m.%Y")
    except ValueError:
        return None
