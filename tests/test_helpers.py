from copy import copy
from types import SimpleNamespace

from django.test import TestCase
from django_handy.helpers import (
    simple_urljoin, get_attribute, has_attribute, bulk_dict_update, is_empty,
    all_not_empty,
    any_not_empty,
    join_not_empty,
)


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

    def test_bulk_dict_update(self):
        dicts = [
            copy(self.person_dict), copy(self.person_dict['address'])
        ]
        bulk_dict_update(dicts, {'id': 10})
        self.assertEqual(dicts[0]['id'], 10)
        self.assertEqual(dicts[1]['id'], 10)

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

    def test_all_not_empty(self):
        data = {
            'name': 'Bob',
            'surname': None,
            'address': {
                'city': 'New York',
                'building': 0,
                'apartments': None
            },
        }

        self.assertEqual(all_not_empty(data, 'name', 'address.building'), True)
        self.assertEqual(all_not_empty(data, 'name', 'address.apartments'), False)

    def test_any_not_empty(self):
        data = {
            'name': 'Bob',
            'surname': None,
            'address': {
                'city': 'New York',
                'building': 0,
                'apartments': None
            },
        }

        self.assertEqual(any_not_empty(data, 'name', 'address.apartments'), True)
        self.assertEqual(any_not_empty(data, 'surname', 'address.apartments'), False)

    def test_join_not_empty(self):
        self.assertEqual(join_not_empty(', ', 'New York', '', 'Baker Street', None), 'New York, Baker Street')
        self.assertEqual(join_not_empty(', '), '')
