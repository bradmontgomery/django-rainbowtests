try:
    from .tests import RainbowTestSuiteRunner
except ImportError:
    pass  # this isn't going to work while installing, but that's ok (i think)

__version__ = '0.1.1'
