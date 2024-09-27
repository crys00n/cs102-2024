"""Module providing a function printing 'hello world!'."""


def text(m):
    """Returns sum of three strings (takes first of them).

    Returns:
        message (str): string of the sum of strings m and two given: " " and "world!"
    """
    message = m + " " + "world!"
    return message


print(text("hello"))
