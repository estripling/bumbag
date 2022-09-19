from importlib.metadata import version

__version__ = version("bumbag")

from .core import *
from .io import *
from .math import *
from .random import *
from .string import *
from .time import *

del core, io, math, random, string, time, version
