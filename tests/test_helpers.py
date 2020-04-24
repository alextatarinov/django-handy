from types import SimpleNamespace

from django.test import TestCase

from django_handy.attrs import get_attribute, has_attribute, is_empty
from django_handy.unique import unique_ordered
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

            ['https://google.com', 'search', 'all/'],
            ['https://', 'google.com', 'search', 'all/'],

            ['http://facebook.com/', 'https://google.com', 'search', 'all'],

            ['search', 'all'],
            ['/search', 'all'],
        )

        expected = (
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',
            'https://google.com/search/all',

            'https://google.com/search/all/',
            'https://google.com/search/all/',

            'https://google.com/search/all',

            'search/all',
            '/search/all',
        )

        for input_args, expected_out in zip(inputs, expected):
            self.assertEqual(simple_urljoin(*input_args), expected_out)

    def test_get_attribute(self):
        address_obj = SimpleNamespace(**self.address_dict)
        person_obj = SimpleNamespace(name='Bob', address=address_obj)

        for person in [person_obj, self.person_dict]:
            self.assertEqual(get_attribute(person, 'name'), self.person_dict['name'])
            self.assertEqual(get_attribute(person, 'address.city'), self.address_dict['city'])

            with self.assertRaises(AttributeError):
                get_attribute(person, 'surname')

            with self.assertRaises(AttributeError):
                get_attribute(person, 'address.country')

    def test_has_attribute(self):
        self.assertEqual(has_attribute(self.person_dict, 'name'), True)
        self.assertEqual(has_attribute(self.person_dict, 'address.city'), True)

        self.assertEqual(has_attribute(self.person_dict, 'surname'), False)
        self.assertEqual(has_attribute(self.person_dict, 'address.country'), False)

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
