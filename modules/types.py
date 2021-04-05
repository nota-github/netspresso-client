from enum import Enum


class ReturnDataType(Enum):
    """return value types about api request"""

    DATA_FRAME = 1
    JSON = 2
    YAML = 3


class DataSetFormat(Enum):
    """when passing compression configs to api server, dataset format required"""

    FOLDER = 1
    imagefolder = 2
    TFRECORD = 3
    NUMPY = 4

class InputModelType(Enum):
    # models
    pb = 1
    h5 = 2

class Error(Exception):
    """Base class for exception in this module."""
    pass

class ModelTypeError(Error):
    """Exception raised for errors in the input model type."""
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
