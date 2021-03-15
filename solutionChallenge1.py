""" Function for string comprehension """


def compress(input_str):
    """
    This function compress the given string
    Args:
        input_str(str): Input string
    Return:
        It will return compressed string
    """
    if len(input_str) == 0:
        return input_str
    result = existing_char = input_str[0]
    count = 1
    for input_char in input_str[1:]:
        if existing_char == input_char:
            count += 1
        elif count > 1:
            result += str(count) + input_char
            existing_char = input_char
            count = 1
        else:
            result += input_char
            existing_char = input_char
    if count != 1:
        result += str(count)
    return result


print(compress(""))