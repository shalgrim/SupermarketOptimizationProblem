from unittest import TestCase
from gen_assoc_rules import solve

IN_LINES = [
'0 1 2 3 4 5 6 7\n',
'30 31 32\n',
'33 34 35\n',
'0 20 28 30\n',
'0 1 2 3 20 30 31 32\n',
'33 34 35\n',
'33 34 35 36\n',
'33 34 35 36 37 38 39 40\n',
'33 34 35 36\n',
'33 34 35 36 37\n',
]

# first key is N
# second key is sigma
# value is answer
ANSWER_KEY = {
    3: {
        4: {
            ('33','34','35'): 6,
            ('33','34','36'): 4,
            ('33','35','36'): 4,
            ('34','35','36'): 4,
            ('33','34','35','36'): 4
        }
    }
}


class TestSolve(TestCase):
    def test_solve_toy(self):
        retval = solve(IN_LINES, 3, 4)
        self.assertEqual(retval, ANSWER_KEY[3][4])

