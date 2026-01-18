"""Legacy test runner for Django < 1.8.

This module is deprecated and will raise an error if used.
DjangoTestSuiteRunner was removed in Django 1.8.

Use rainbowtests.test.runner.RainbowDiscoverRunner instead.
"""


class RainbowTestSuiteRunner:
    """Deprecated: This runner is not compatible with Django 1.8+.

    DjangoTestSuiteRunner was removed in Django 1.8. Please use
    RainbowDiscoverRunner instead:

        TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "RainbowTestSuiteRunner is not compatible with Django 1.8+. "
            "Please use 'rainbowtests.test.runner.RainbowDiscoverRunner' instead."
        )
