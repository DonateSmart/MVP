import unittest


class MyTestCase(unittest.TestCase):
    def test_signup(self):
        form = {'username': 'username1', 'password': 'pass1'}
        # request = None
        # request.form = form
        # request.method = 'POST'
        # main.signup_user(request)


if __name__ == '__main__':
    unittest.main()
