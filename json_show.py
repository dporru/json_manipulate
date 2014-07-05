#!/usr/bin/python
import json, sys, argparse

def manipulate(json_object, manipulate_string):
   (key, rest) = get_key(manipulate_string)
   
def get_key(manipulate_string):
    return (None, None)

def get_args(argument_list):
    parser = argparse.ArgumentParser(description='Show and manipulate json strings.')
    parser.add_argument('-m', '--manipulate_string', type=str, default='', help='A maniputation string, see description.')
    return parser.parse_args(argument_list[1:])

if __name__ == '__main__':
    json_object = json.load(sys.stdin)
    
    args = get_args(sys.argv)
    
    json_object = manipulate(json_object, args.manipulate_string)
    
    print json.dumps(json_object, indent=4, separators=(',', ': '))

# ''
# 'response.result.(persons|recepies)'
# 'response.result.persons[firstname|last_name]'
# 'response.result.persons[firstname|last_name|(address.street|number)]'
# 'response.result.persons[firstname]'
