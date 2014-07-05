#!/usr/bin/python
import json, sys, argparse

def manipulate(json_object, manipulate_string):
    (key, rest) = get_key(manipulate_string)
   
    if type(key) == str:
        try:
            return {key : json_object[key]}
        except KeyError:
            raise KeyNotFound(key)
   
    if key == None:
       return json_object
   
def get_key(ms):
    if ms == '':
        return (None, None)
    
    if type(ms) == str:
        dot_pos = ms.find('.')
        pipe_pos = ms.find('|')
        parenthesis_pos = ms.find('(')
        square_bracket_pos = ms.find('[')
    
        # remove starting and trailing parenthesis
        if parenthesis_pos == 0:
            ms = ms[1:-1]
            parenthesis_pos = -1
            
        # remove starting and trailing square_brackets
        if square_bracket_pos == 0:
            ms = ms[1:-1]
            square_bracket_pos = -1
        
        # return (key, rest) tuple
        if square_bracket_pos != -1:
            return (ms[:square_bracket_pos], get_key(ms[square_bracket_pos+1:-1]))
        
        # return list of (key, rest) tuples
        if pipe_pos != -1 and (parenthesis_pos == -1 or pipe_pos < parenthesis_pos):
            return (map(get_key, get_piped_parts(ms)), None)
        
        # return (key, rest) tuple
        if dot_pos != -1:
            return (ms[:dot_pos], get_key(ms[dot_pos+1:]))
        
        return (ms, None)

def get_piped_parts(ms):
    if ms == '':
        return []
        
    pipe_pos = ms.find('|')
    parenthesis_pos = ms.find('(')
    
    if pipe_pos == -1 or (parenthesis_pos != -1 and pipe_pos > parenthesis_pos):
        return [ms]
    
    return [ms[:pipe_pos]] + get_piped_parts(ms[pipe_pos+1:])

def get_args(argument_list):
    parser = argparse.ArgumentParser(description='Show and manipulate json strings.')
    parser.add_argument('-m', '--manipulate_string', type=str, default='', help='A maniputation string, see description.')
    return parser.parse_args(argument_list[1:])

class KeyNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    json_object = json.load(sys.stdin)
    
    args = get_args(sys.argv)
    
    json_object = manipulate(json_object, args.manipulate_string)
    
    print json.dumps(json_object, indent=4, separators=(',', ': '))
