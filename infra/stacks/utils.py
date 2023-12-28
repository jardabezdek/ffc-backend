"""Script with utils for AWS CDK."""

from pathlib import Path
from typing import Dict


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


def get_env_variables() -> Dict[str, str]:
    """Retrieve environment variables from a specified file and return them as a dictionary.

    The environment variables are read from the .env file located in the 'transform' directory.

    Returns:
    --------
    Dict[str, str]
        A dictionary containing environment variables where keys represent the variable names
        and values represent the corresponding variable values.
    """
    env_variables = {}
    env_file_path = Path(__file__).resolve().parent.parent / "transform" / ".env"

    with open(env_file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            var_name, var_value = line.split("=")
            env_variables[var_name] = var_value

    return env_variables
