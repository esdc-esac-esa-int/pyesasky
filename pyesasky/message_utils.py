import pyesasky.constants as const


def is_response_message(message):
    return get_message_id(message) is not None or is_init_message(message)


def is_init_message(message):
    try:
        return get_message_content(message)[const.MESSAGE_INIT]
    except (KeyError, TypeError):
        return False


def get_message_data(message):
    try:
        return message[const.MESSAGE_DATA]
    except (KeyError, TypeError):
        return None


def get_message_content(message):
    try:
        return get_message_data(message)[const.MESSAGE_CONTENT]
    except (KeyError, TypeError):
        return None


def get_nested_message_content(message):
    try:
        return get_message_content(message[const.MESSAGE_CONTENT])
    except (KeyError, TypeError):
        return None


def get_message_id(message):
    try:
        if is_init_message(message):
            return const.MESSAGE_INIT_ID_FLAG
        
        return get_message_content(message)[const.MESSAGE_CONTENT_ID]
    except (KeyError, TypeError):
        return None


def get_message_error(message):
    try:
        return get_message_content(message)[const.MESSAGE_CONTENT_ERROR]
    except (KeyError, TypeError):
        return None


def get_message_extras(message):
    try:
        return get_message_content(message)[const.MESSAGE_CONTENT_EXTRAS]
    except (KeyError, TypeError):
        return None


def get_message_values(message):
    try:
        return get_message_content(message)[const.MESSAGE_CONTENT_VALUES]
    except (KeyError, TypeError):
        return None


def is_message_success(message):
    return const.MESSAGE_CONTENT_SUCCESS in message


def create_message_output(message):
    result: list[str] = []

    err = get_message_error(message)
    extras = get_message_extras(message)

    if err is not None:
        if const.MESSAGE_ERROR_MESSAGE in err:
            result.append(err[const.MESSAGE_ERROR_MESSAGE])

        if const.MESSAGE_ERROR_AVAILABLE in err:
            result.append("Available options:")
            result.append(err[const.MESSAGE_ERROR_AVAILABLE])
    elif extras is not None and const.MESSAGE_EXTRAS_MESSAGE in extras:
        result.append(extras[const.MESSAGE_EXTRAS_MESSAGE])

    return "\n".join(str(item) for item in result)


def create_message_result(message):
    values = get_message_values(message)
    if values is not None:
        if isinstance(values, list) and len(values) == 1:
            return values[0]
        else:
            return values
