import math
from functools import lru_cache
from logging import getLogger

from django.utils.functional import cached_property


""" 
    These functions convert an integer (from eg an ID AutoField) to a
    short unique string. This is done using a perfect hash (Knuth multiplicative hash)
    function and converting the result into a string of user friendly characters.
"""

logger = getLogger()


class Encoder:
    def __init__(self, length, valid_chars):
        self.length = length
        self.valid_chars = valid_chars

        size, alpha = self.get_params(self.length, self.valid_chars)
        self.size = size
        self.alpha = alpha

    @cached_property
    def base(self):
        return len(self.valid_chars)

    @classmethod
    @lru_cache()
    def get_params(cls, length, valid_chars):
        size = len(valid_chars) ** length
        power = math.floor(math.log2(size))

        # Use golden ratio to find alpha parameter.
        # It should not have common divider with size, and size is always even (2 ** power)
        # So alpha should be always odd
        alpha = int(2 ** power * (-1 + 5 ** 0.5) / 2)
        if alpha % 2 == 0:
            alpha += 1

        size = 2 ** power
        return size, alpha

    def perfect_hash(self, num):
        """
            Translate a number to another unique number, using a perfect hash function.
            Only meaningful where 0 < num < size.
        """
        return (num * self.alpha) % self.size

    def friendly_number(self, num):
        """
            Convert a base 10 number to a self.base X string.
            Charcters from VALID_CHARS are chosen, to convert the number
            to eg base 26, if there are 26 characters to choose from.
            Use valid chars to choose characters that are friendly, avoiding
            ones that could be confused in print or over the phone.
        """
        string = ''
        while len(string) < self.length:
            # It is better to prepend chars to avoid 1st char repetition
            string = self.valid_chars[num % self.base] + string
            num //= self.base
        return string

    def encode(self, num):
        """
            Encode a simple number, using a perfect hash and converting to a
            more user friendly string of characters.
        """
        if num is None:
            return None

        if num >= self.size:
            raise ValueError('Encode numbers is overflowing! Adjust size!')
        if num <= 0:
            raise ValueError('Number is <= 0')

        if num > self.size - 10000:
            logger.error('Encode numbers is going to overflow soon! Adjust size!')

        return self.friendly_number(self.perfect_hash(num))


def encode(num, length=7, valid_chars='3456789ACDEFGHJKLQRSTUVWXY'):
    """
        Encode a simple number, using a perfect hash and converting to a
        more user friendly string of characters.
        Generated 7-symbol codes by default - up to 4.294.967.296 of them
    """
    encoder = Encoder(length, valid_chars)
    return encoder.encode(num)
