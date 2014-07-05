#!/usr/bin/python
import sys
sys.path.append('../')
from json_show import json_show
import unittest

class TestJsonShow(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_args_no_arguments(self):
        argument_list = ['json_show.py']
        
        args = json_show.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, '')

    def test_get_args_manipulate_string(self):
        argument_list = ['json_show.py', '-m', 'result']
        
        args = json_show.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, 'result')
    
    def test_get_key_empty_string(self):
        manipulate_string = ''
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, (None, None))
        
    def test_get_key_one_key(self):
        manipulate_string = 'response'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', None))
        
if __name__ == '__main__':
    unittest.main()