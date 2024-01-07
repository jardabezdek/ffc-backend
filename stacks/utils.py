"""Script with utils for AWS CDK."""


def get_name(name: str) -> str:
    """Prepend prefix to the AWS object name.

    Parameters:
    -----------
    name : str
        A name of AWS object.

    Returns:
    --------
    str
    """
    return f"frozen-facts-center-{name.lower()}"
