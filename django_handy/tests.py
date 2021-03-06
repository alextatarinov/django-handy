import unittest

from django.db import connection
from django.test.runner import DiscoverRunner


class FixedTestLoader(unittest.TestLoader):
    def _find_test_path(self, full_path, *args, **kwargs):
        # Don't look for tests inside models folder - this will cause invalid models import and RuntimeError
        if full_path.endswith('/models'):
            return None, False
        return super()._find_test_path(full_path, *args, **kwargs)


class FixedDiscoverRunner(DiscoverRunner):
    test_loader = FixedTestLoader()


def run_on_commit():
    while connection.run_on_commit:
        _, func = connection.run_on_commit.pop(0)
        func()
