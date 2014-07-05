#!/usr/bin/python
import sys
sys.path.append('../')
from json_show import json_show
import unittest

class TestJsonShow(unittest.TestCase):

    def setUp(self):
        self.json_object = {
            "response" : {
                "result" : {
                    "rows" : [
                        {
                            "row_nr" : 1,
                            "row_data" : "row number 1"
                        },
                        {
                            "row_nr" : 2,
                            "row_data" : "row number 2"
                        }
                    ]
                }
            }
        }
    
    def test_get_args_no_arguments(self):
        argument_list = ['json_show.py']
        
        args = json_show.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, '')

    def test_get_args_manipulate_string(self):
        argument_list = ['json_show.py', '-m', 'result']
        
        args = json_show.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, 'result')
    
    def test_manipulate_empty_string(self):
        manipulate_string = ''
        
        result = json_show.manipulate(self.json_object, manipulate_string)
        
        self.assertEqual(result, self.json_object)

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