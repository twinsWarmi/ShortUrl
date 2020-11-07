import os, sys
import unittest
import re
from dotenv import load_dotenv, find_dotenv

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from main import app, generate, msg


class MainTest(unittest.TestCase):

    def test_generate(self):
        load_dotenv(find_dotenv(), override=True)
        path_length = int(os.getenv('PATH_LENGTH'))
        ans = generate()
        assert (re.compile(r'[a-zA-Z0-9]').match(ans).endpos == path_length)

    def test_msg(self):
        ans = msg(200, 'success', 'ok')
        assert (ans == '{"code": 200, "status": "success", "msg": "ok"}')


if __name__ == '__main__':
    unittest.main()
