import math
from itertools import chain
from logging import getLogger


""" Credits to https://github.com/simonluijk/django-invoice
"""

""" Generates and decodes an unique invoice id, which can use characters
    to shorten its length.

     Author: Will Hardy
       Date: December 2008
      Usage: >>> encode(1)
             "488KR"
Description: Invoice numbers like "0000004" are unprofessional in that they
             expose how many sales a system has made, and can be used to monitor
             the rate of sales over a given time.  They are also harder for
             customers to read back to you, especially if they are 10 digits
             long.
             These functions convert an integer (from eg an ID AutoField) to a
             short unique string. This is done simply using a perfect hash
             function and converting the result into a string of user friendly
             characters.

"""
# Keep this small for shorter strings, but big enough to avoid changing
# it later. If you do change it later, it might be a good idea to specify a
# STRING_LENGTH change, making all future strings longer, and therefore unique.

# OPTIONAL PARAMETERS
# This just means we don't start with the first number, to mix things up
# Alpha numeric characters, only uppercase, no confusing values (eg 1/I,0/O,Z/2)
# Remove some letters if you prefer more numbers in your strings
# You may wish to remove letters that sound similar, to avoid confusion when a
# customer calls on the phone (B/P, M/N, 3/C/D/E/G/T/V)


logger = getLogger()
SIZE = 100000000
OFFSET = SIZE // 2 - 1
VALID_CHARS = '3456789ACDEFGHJKLQRSTUVWXY'


def find_suitable_period():
    """ Automatically find a suitable period to use.
        Factors are best, because they will have 1 left over when
        dividing SIZE+1.
        This only needs to be run once, on import.
    """
    # The highest acceptable factor will be the square root of the size.
    highest_acceptable_factor = int(math.sqrt(SIZE))

    # Too high a factor (eg SIZE/2) and the interval is too small, too
    # low (eg 2) and the period is too small.
    # We would prefer it to be lower than the number of VALID_CHARS, but more
    # than say 4.
    starting_point = len(VALID_CHARS) > 14 and len(VALID_CHARS) // 2 or 13
    for p in chain(range(starting_point, 7, -1),
                   range(highest_acceptable_factor, starting_point + 1, -1),
                   [6, 5, 4, 3, 2]):
        if SIZE % p == 0:
            return p
    raise ValueError("No valid period could be found for SIZE=%d.\nTry avoiding prime numbers :-)" % SIZE)


PERIOD = find_suitable_period()


def perfect_hash(num):
    """
        Translate a number to another unique number, using a perfect hash function.
        Only meaningful where 0 <= num <= SIZE.
    """
    return ((num + OFFSET) * (SIZE // PERIOD)) % (SIZE + 1) + 1


def friendly_number(num):
    """
        Convert a base 10 number to a base X string.
        Charcters from VALID_CHARS are chosen, to convert the number
        to eg base 24, if there are 24 characters to choose from.
        Use valid chars to choose characters that are friendly, avoiding
        ones that could be confused in print or over the phone.
    """
    # Convert to a (shorter) string for human consumption
    string = ''
    # The length of the string can be determined by STRING_LENGTH or by how many
    # characters are necessary to present a base 30 representation of SIZE.
    while len(VALID_CHARS) ** len(string) <= SIZE:
        # Prepend string (to remove all obvious signs of order)
        string = VALID_CHARS[num % len(VALID_CHARS)] + string
        num //= len(VALID_CHARS)
    return string


def encode(num):
    """ Encode a simple number, using a perfect hash and converting to a
        more user friendly string of characters.
    """
    if num is None:
        return None

    # Check the number is within our working range
    global SIZE
    if num > SIZE:
        raise ValueError(f'Encode numbers is overflowing! Adjust SIZE in {__file__}')
    if num < 0:
        raise ValueError(f'Number is less then {0}')

    if num > SIZE - 10000:
        logger.error(f'Encode numbers is going to overflow soon! Adjust SIZE in {__file__}')

    return friendly_number(perfect_hash(num))
