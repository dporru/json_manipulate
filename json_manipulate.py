#!/usr/bin/python
import json, sys, argparse

def manipulate(json_object, key, rest):
    """ 
    Manipulate a dictionary.

    Args:
        json_object: dictionary or list to manipulate
        key:
            1) string            -> select only given key from dictionary
            2) list of strings   -> select only given keys from dictionary
                                    or select only givens keys from the dictionaries
                                    in the given list
            3) None              -> return given dictionary or list untouched
        rest:
            1) tuple (key, rest) -> recursively call manipulate on the by key selected
                                    part of the dictionary or list
            2) None              -> end recursive calls
    Returns:
        Manipulated dictonary or list
    """
    
    # json_object is list: select key from list of dictionaries
    if type(json_object) == list:
        return_list = []
        for item in json_object:
            return_list.append(manipulate(item, key, rest))
        return return_list
    
    # key is string: select key from dictionary
    if type(key) == str:
        try:
            if rest != None:
                rest_object = manipulate(json_object[key], rest[0], rest[1])
            else:
                rest_object = json_object[key]
            return {key : rest_object}
        except KeyError:
            raise KeyNotFound(key)
    
    # key is list: select keys from dictionary
    if type(key) == list:
        return_object = {}
        for sub_key in key:
            return_object[sub_key[0]] = manipulate(json_object, sub_key[0], sub_key[1])[sub_key[0]]
        return return_object
        
    if key == None:
       return json_object
   
def get_key(ms):
    """
    Creates a key and a rest tuple based on a manipulation string
    
    Args:
        ms: Manipulation string
            eg. '', 'result','result.rows' or 'result.rows[name|address]'
    Returns:
        A tuple of key and rest. In the above example respectivly:
            (None, None)
            ('result', None)
            ('result', ('rows', None))
            ('result', ('rows', (['name', 'address'], None)))
    """
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
        
        no_dot_before_brackets = (dot_pos == -1 or dot_pos > square_bracket_pos)
        pipe_not_inside_parenthesis = (parenthesis_pos == -1 or pipe_pos < parenthesis_pos)
        pipe_not_inside_brackets = (square_bracket_pos == -1 or pipe_pos < square_bracket_pos)
        
        # return (key, rest) tuple
        if square_bracket_pos != -1 and no_dot_before_brackets:
            return (ms[:square_bracket_pos], get_key(ms[square_bracket_pos+1:-1]))
        
        # return list of (key, rest) tuples
        if pipe_pos != -1 and pipe_not_inside_parenthesis and pipe_not_inside_brackets:
            return (map(get_key, get_piped_parts(ms)), None)
        
        # return (key, rest) tuple
        if dot_pos != -1:
            return (ms[:dot_pos], get_key(ms[dot_pos+1:]))
        
        return (ms, None)

def get_piped_parts(ms):
    """
    Splits a string on the pipe '|' character, but only if it
    is not inside parenthesis () or square brackets [].
    
    Args:
        ms: Manipulation string
    Returns:
        List of strings
    """
    if ms == '':
        return []
        
    pipe_pos = ms.find('|')
    square_bracket_pos = ms.find('[')
    parenthesis_pos = ms.find('(')
    
    if pipe_pos == -1 or (parenthesis_pos != -1 and pipe_pos > parenthesis_pos) or (square_bracket_pos != -1 and pipe_pos > square_bracket_pos):
        return [ms]
    
    return [ms[:pipe_pos]] + get_piped_parts(ms[pipe_pos+1:])

def get_args(argument_list):
    """
    Returns an object with command line arguments.
    """
    parser = argparse.ArgumentParser(description='Show and manipulate json strings.')
    parser.add_argument('-m', '--manipulate_string', type=str, default='', help='A maniputation string, see description.')
    return parser.parse_args(argument_list[1:])

class KeyNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    # load the json_object from the stdin
    json_object = json.load(sys.stdin)
    
    # parse command line arguments
    args = get_args(sys.argv)
    
    # create json manipulation object based on command line arguments
    (key, rest) = get_key(args.manipulate_string)
    
    # create the manipulated json object
    json_object = manipulate(json_object, key, rest)
    
    # print the manipulated json object to screen
    print json.dumps(json_object, indent=4, separators=(',', ': '))
