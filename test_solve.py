from unittest import TestCase
from gen_assoc_rules import solve

IN_LINES = [
'0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 25 26 27 28 29\n',
'30 31 32\n',
'33 34 35\n',
'0 20 28 30\n',
'0 1 2 3 20 25 26 27 28 30 31 32\n',
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
            ('34','35','36'): 4
        }
    }
}


class TestSolve(TestCase):
    def test_solve_brute_force(self):
        retval = solve(IN_LINES, 3, 4, 'brute_force')
        self.assertEqual(retval, ANSWER_KEY[3][4])

    def test_solve_index(self):
        retval = solve(IN_LINES, 3, 4, 'index')
        self.assertEqual(retval, ANSWER_KEY[3][4])
