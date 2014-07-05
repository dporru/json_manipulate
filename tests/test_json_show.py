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
    
    def test_manipulate_no_key(self):
        key = None
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        result = json_show.manipulate(json_object, key, rest)
        
        self.assertEqual(result, json_object)
        
    def test_manipulate_key(self):
        key = 'object1'
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        result = json_show.manipulate(json_object, key, rest)
        
        self.assertEqual(result, {"object1" : json_object['object1']})
        
    def test_manipulate_non_existing_key(self):
        key = 'object3'
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        self.assertRaises(json_show.KeyNotFound, json_show.manipulate, json_object, key, rest)

    def test_get_key_empty_string(self):
        manipulate_string = ''
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, (None, None))
        
    def test_get_key_one_key(self):
        manipulate_string = 'response'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', None))
        
    def test_get_key_one_key_and_rest_key(self):
        manipulate_string = 'response.result'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', ('result', None)))
        
    def test_get_key_keys_separated_by_pipe(self):
        manipulate_string = 'persons|addresses|streets'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ([('persons', None), ('addresses', None), ('streets', None)], None))
        
    def test_get_key_keys_separated_by_pipe_in_parenthesis(self):
        manipulate_string = 'result.(addresses|streets)'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None)], None)))
    
    def test_get_key_keys_separated_by_pipe_in_square_brackets(self):
        manipulate_string = 'result[addresses|streets]'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None)], None)))
    
    def test_get_key_keys_separated_by_pipe_in_parenthesis_in_square_brackets(self):
        manipulate_string = 'result[addresses|streets|person.(name|birth_date)]'
        
        result = json_show.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None), (('person', ([('name', None),('birth_date', None)], None)))], None)))

    def test_get_piped_parts_empty_string(self):
        manipulate_string = ''
        
        result = json_show.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, [])
        
    def test_get_piped_parts_key(self):
        manipulate_string = 'persons'
        
        result = json_show.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['persons'])
        
    def test_get_piped_parts_keys_separated(self):
        manipulate_string = 'persons|addresses|streets'
        
        result = json_show.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['persons', 'addresses', 'streets'])
        
    def test_get_piped_parts_keys_separated_in_parenthesis(self):
        manipulate_string = 'person|address.(street|city)'
        
        result = json_show.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['person', 'address.(street|city)'])
        
if __name__ == '__main__':
    unittest.main()