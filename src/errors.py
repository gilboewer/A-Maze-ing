class ConfigError(Exception):
    """
    Base exception for configuration-related errors.
    """


class ConfigFormatError(ConfigError):
    """
    Exception for configuration file format errors.
    """

    def __init__(self, line_number: int, line: str, msg: str):
        """
        Initializes the ConfigFormatError.

        Args:
            line_number (int): The line number where the error occurred.
            line (str): The content of the erroneous line.
            msg (str): Additional error message.
        """
        super().__init__(f"Line {line_number} '{line}'. {msg}")


class ConfigParseError(ConfigError):
    """
    Exception for configuration value parsing errors.
    """

    def __init__(self, setting: str, value: str, msg: str):
        """
        Initializes the ConfigParseError.

        Args:
            setting (str): The configuration setting name.
            value (str): The invalid value that was provided.
            msg (str): Additional error message.
        """
        super().__init__(f"Invalid value for '{setting}': '{value}'. {msg}")


class ConfigValueError(ConfigError):
    """
    Exception for invalid configuration values.
    """

    def __init__(self, setting: str, msg: str):
        """
        Initializes the ConfigValueError.

        Args:
            setting (str): The configuration setting name.
            msg (str): Error message describing the issue.
        """
        super().__init__(f"Invalid value for '{setting}'. {msg}")
