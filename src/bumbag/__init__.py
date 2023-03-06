from importlib import metadata

__version__ = metadata.version("bumbag")

from .core import *
from .io import *
from .math import *
from .random import *
from .string import *
from .time import *

del (
    metadata,
    core,
    io,
    math,
    random,
    string,
    time,
)
