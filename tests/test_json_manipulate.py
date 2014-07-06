#!/usr/bin/python
import sys
sys.path.append('../')
from json_manipulate import json_manipulate
import unittest

class TestJsonShow(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get_args_no_arguments(self):
        argument_list = ['json_manipulate.py']
        
        args = json_manipulate.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, '')

    def test_get_args_manipulate_string(self):
        argument_list = ['json_manipulate.py', '-m', 'result']
        
        args = json_manipulate.get_args(argument_list)
        
        self.assertEqual(args.manipulate_string, 'result')
    
    def test_manipulate_no_key(self):
        key = None
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, json_object)
        
    def test_manipulate_key(self):
        key = 'object1'
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, {"object1" : json_object['object1']})
        
    def test_manipulate_non_existing_key(self):
        key = 'object3'
        rest = None
        json_object = {"object1" : "value1", "object2": "value2"}
        
        self.assertRaises(json_manipulate.KeyNotFound, json_manipulate.manipulate, json_object, key, rest)

    def test_manipulate_key_and_rest_key(self):
        key = 'object1'
        rest = ('subobject2', None)
        json_object = {"object1" : {"subobject1" : "sub_value1", "subobject2": "sub_value2"}, "object2": "value2"}
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, {"object1" : {"subobject2" : "sub_value2"}})
        
    def test_manipulate_multiple_keys(self):
        key = [('object1', None), ('object2', None)]
        rest = None
        json_object = {"object1" : "value1", "object2": "value2", "object3" : "value3"}
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, {"object1" : "value1", "object2": "value2"})
        
    def test_manipulate_multiple_keys_with_subkey(self):
        key = [('object1', None), ('object2', ('subobject1', None))]
        rest = None
        json_object = {"object1" : "value1", "object2": {"subobject1" : "subvalue1", "subobject2" : "subvalue2"}, "object3" : "value3"}
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, {"object1" : "value1", "object2": {"subobject1" : "subvalue1"}})
    
    def test_manipulate_multiple_keys_in_list(self):
        key = [('name1', None), ('name2', None)]
        rest = None
        json_object = [{"name1" : "value1", "name2": "value1", "name3": "value1"}, {"name1" : "value2", "name2": "value2", "name3": "value2"}, {"name1" : "value3", "name2": "value3", "name3": "value3"}]
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, [{"name1" : "value1", "name2": "value1"}, {"name1" : "value2", "name2": "value2"}, {"name1" : "value3", "name2": "value3"}])
        
    def test_manipulate_single_key_in_list(self):
        key = 'name1'
        rest = None
        json_object = [{"name1" : "value1", "name2": "value1", "name3": "value1"}, {"name1" : "value2", "name2": "value2", "name3": "value2"}, {"name1" : "value3", "name2": "value3", "name3": "value3"}]
        
        result = json_manipulate.manipulate(json_object, key, rest)
        
        self.assertEqual(result, [{"name1" : "value1"}, {"name1" : "value2"}, {"name1" : "value3"}])
        
    def test_get_key_empty_string(self):
        manipulate_string = ''
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, (None, None))
        
    def test_get_key_one_key(self):
        manipulate_string = 'response'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', None))
        
    def test_get_key_one_key_and_rest_key(self):
        manipulate_string = 'response.result'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', ('result', None)))
        
    def test_get_key_keys_separated_by_pipe(self):
        manipulate_string = 'persons|addresses|streets'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ([('persons', None), ('addresses', None), ('streets', None)], None))
        
    def test_get_key_keys_separated_by_pipe_in_parenthesis(self):
        manipulate_string = 'result.(addresses|streets)'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None)], None)))
    
    def test_get_key_keys_separated_by_pipe_in_square_brackets(self):
        manipulate_string = 'result[addresses|streets]'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None)], None)))
    
    def test_get_key_keys_separated_by_pipe_in_parenthesis_in_square_brackets(self):
        manipulate_string = 'result[addresses|streets|person.(name|birth_date)]'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('result', ([('addresses', None), ('streets', None), (('person', ([('name', None),('birth_date', None)], None)))], None)))
        
    def test_get_key_sub_keys_separated_by_pipe_in_square_brackets(self):
        manipulate_string = 'response.result[addresses|streets]'
        
        result = json_manipulate.get_key(manipulate_string)
        
        self.assertEqual(result, ('response', ('result', ([('addresses', None), ('streets', None)], None))))

    def test_get_piped_parts_empty_string(self):
        manipulate_string = ''
        
        result = json_manipulate.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, [])
        
    def test_get_piped_parts_key(self):
        manipulate_string = 'persons'
        
        result = json_manipulate.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['persons'])
        
    def test_get_piped_parts_keys_separated(self):
        manipulate_string = 'persons|addresses|streets'
        
        result = json_manipulate.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['persons', 'addresses', 'streets'])
        
    def test_get_piped_parts_keys_separated_in_parenthesis(self):
        manipulate_string = 'person|address.(street|city)'
        
        result = json_manipulate.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['person', 'address.(street|city)'])
        
    def test_get_piped_parts_keys_separated_in_square_brackets(self):
        manipulate_string = 'person.addresses[street|city]'
        
        result = json_manipulate.get_piped_parts(manipulate_string)
        
        self.assertEqual(result, ['person.addresses[street|city]'])
        
if __name__ == '__main__':
    unittest.main()