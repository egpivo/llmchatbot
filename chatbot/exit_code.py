from enum import Enum


class ExitCode(Enum):
    """
    Enumeration of exit codes used in scripts or applications.

    - SUCCESS: Successful execution.
    - GENERAL_ERROR: General error or unspecified issue.
    - UNKNOWN_ERROR: Unknown or unexpected error.
    - INVALID_ARGUMENT: Invalid command-line argument.
    - RESOURCE_NOT_FOUND: Required resource not found.
    - CONFIG_PARSE_FAILED: Configuration parsing failed.
    - PACKAGE_NOT_INSTALLED: Required package not installed.
    - PERMISSION_DENIED: Permission denied for an operation.
    - DATA_NOT_FOUND: Required data not found.
    - DATA_TYPE_ERROR: Unexpected data type encountered.
    - KEY_NOT_FOUND: Key not found in a data structure.
    - DATABASE_ERROR: General database error.
    - DATABASE_TIMEOUT: Database operation timed out.
    - DATABASE_TABLE_NOT_FOUND: Database table not found.
    - FILE_NOT_FOUND: Required file not found.
    """

    SUCCESS = 0
    GENERAL_ERROR = 1
    UNKNOWN_ERROR = 2
    INVALID_ARGUMENT = 3
    RESOURCE_NOT_FOUND = 4
    CONFIG_PARSE_FAILED = 5
    PACKAGE_NOT_INSTALLED = 6
    PERMISSION_DENIED = 7
    DATA_NOT_FOUND = 8
    DATA_TYPE_ERROR = 9
    KEY_NOT_FOUND = 10
    DATABASE_ERROR = 11
    DATABASE_TIMEOUT = 12
    DATABASE_TABLE_NOT_FOUND = 13
    FILE_NOT_FOUND = 14
    MODEL_TRAINING_ERROR = 15
