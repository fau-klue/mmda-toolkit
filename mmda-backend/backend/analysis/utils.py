# General utils


from hashlib import sha256


def generate_hash(string):
    """
    Generate a hash from a string.

    :param str string: String to generate hash from.
    :return: hash for a given string
    :rtype: str
    """

    return sha256(str(string).encode()).hexdigest()
