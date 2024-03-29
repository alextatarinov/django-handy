import unittest

from django.test.runner import DiscoverRunner


class FixedTestLoader(unittest.TestLoader):
    def _find_test_path(self, full_path, *args, **kwargs):
        # Don't look for tests inside models and admin packages - this will break Django
        if full_path.endswith('/models') or full_path.endswith('/admin'):
            return None, False
        return super()._find_test_path(full_path, *args, **kwargs)


class FixedDiscoverRunner(DiscoverRunner):
    test_loader = FixedTestLoader()
