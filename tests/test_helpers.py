from django.test import TestCase

from django.test import TestCase

from django_handy.objs import is_empty, unique_ordered
from django_handy.url import simple_urljoin


class TestHelpers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address_dict = {
            'city': 'New York',
            'street': 'Baker st.',
            'building': 124,
        }
        cls.person_dict = {
            'name': 'Bob',
            'address': cls.address_dict
        }

    def test_simple_urljoin(self):
        inputs = (
            ['https://google.com', 'search', 'all'],
            ['https://google.com', '/search', 'all'],
            ['https://google.com', 'search/', 'all'],
            ['https://google.com', 'search', '/all'],
            ['https://google.com', 'search/', '/all'],
            ['https://google.com', 'search/', 5],

            ['https://google.com', 'search', 'all/'],
            ['https://', 'google.com', 'search', 'all/'],

            ['http://facebook.com/', 'https://google.com', 'search', 'all'],

            ['search', 'all'],
            ['/search', 'all'],
            ['/search', '/', 'all', '/'],
        )

        expected = (
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/5',

            'https://google.com/search/all/',
            'https://google.com/search/all/',

            'https://google.com/search/all',

            'search/all',
            '/search/all',
            '/search/all/',
        )

        for input_args, expected_out in zip(inputs, expected):
            self.assertEqual(expected_out, simple_urljoin(*input_args))

    def test_is_empty(self):
        empty = [
            None, '', [], tuple(), dict(), set()
        ]
        not_empty = [
            0, False, True, [''], {'': 1}, {None}
        ]
        for e in empty:
            self.assertEqual(is_empty(e), True)

        for ne in not_empty:
            self.assertEqual(is_empty(ne), False)

    def test_unique_ordered(self):
        self.assertEqual(unique_ordered([8, 1, 2, 2, 4, 5, 4, 8]), [8, 1, 2, 4, 5])
