import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")
    
def match_for_integer(input_line):
    return any(char.isdigit() for char in input_line)

def match_for_alphanumeric(input_line):
    return any(char.isdigit() or char.isalpha() for char in input_line)

def match_for_positive_char_groups(input_line, pattern):
    pattern_map = {p : True for p in pattern}
    for ip in input_line:
        if pattern_map.get(ip):
            return True
    return False

def match_for_negative_char_groups(input_line, pattern):
    pattern_map = {p : True for p in pattern}
    for ip in input_line:
        if pattern_map.get(ip):
            return False
    return True

def match_for_wildcard(input_line, pattern):
    pattern_split = pattern.split(".")
    before_pattern = pattern_split[0]
    after_pattern = pattern_split[1]
    start_idx = input_line.find(before_pattern)
    end_idx = input_line.find(after_pattern)
    if start_idx == -1 or end_idx == -1:
        return False
    if start_idx < end_idx:
        return True

def match_for_combined_char_class(input_line, pattern):
    
    if len(input_line) == 0 and len(pattern) == 0:
        return True
    
    if pattern == "$":
        if not input_line:
            return True
        return False
    
    if len(pattern) > 2 and pattern[:2][-1] == "?" and not input_line:
        return True 
    
    if not pattern:
        return True
    if not input_line:
        return False
    
    if pattern[:2][-1] == "+":
        last_char = pattern[:2][0]
        if input_line[0] != last_char:
            return False
        else:
            for i in range(len(input_line)):
                if input_line[i] == last_char:
                    continue
                else:
                    break
            return match_for_combined_char_class(input_line[i:], pattern[2:])
        
    elif pattern[:2][-1] == "?":
        last_char = pattern[:2][0]
        if input_line[0] != last_char:
            return match_for_combined_char_class(input_line, pattern[2:])
        else:
            for i in range(len(input_line)):
                if input_line[i] == last_char:
                    continue
                else:
                    break
            return match_for_combined_char_class(input_line[i:], pattern[2:])
    
    elif pattern[0] == input_line[0]:
        return match_for_combined_char_class(input_line[1:], pattern[1:])
    elif pattern[:2] == "\\d":
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_for_combined_char_class(input_line[i+1:], pattern[2:])
        else:
            return False
    elif pattern[:2] == "\\w":
        if input_line[0].isalnum():
            return match_for_combined_char_class(input_line[1:], pattern[2:])
        else:
            return False            
        
    elif pattern[:1] == "^":
        return match_for_combined_char_class(input_line, pattern[1:])
        
                

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    if pattern[0] == "[" and pattern[1] == "^" and pattern[-1] == "]":
        stripped_pattern = pattern[2:-1]
        if match_for_negative_char_groups(input_line, stripped_pattern):
            exit(0)
        else:
            exit(1)
    
    if pattern[0] == "[" and pattern[-1] == "]":
        stripped_pattern = pattern[1:-1]
        if match_for_positive_char_groups(input_line, stripped_pattern):
            exit(0)
        else:
            exit(1)
            
    if pattern == "\\d":
        if match_for_integer(input_line):
            exit(0)
        else:
            exit(1)
            
    if pattern == "\\w":
        if match_for_alphanumeric(input_line):
            exit(0)
        else:
            exit(1)
            
    if len(pattern) == 1:
        if match_pattern(input_line, pattern):
            exit(0)
        else:
            exit(1)
            
    if "." in pattern:
        if match_for_wildcard(input_line, pattern):
            print("YY")
            exit(0)
        else:
            print("NN")
            exit(1)
          
    #check for combined char class
    # print(input_line, len(input_line), input_line[0], input_line[3])
    input_line = input_line.rstrip()
    if "?" in pattern:
        first_letter_pat = pattern[0]
        for i in range(len(input_line)):
            if input_line[i] == first_letter_pat:
                if match_for_combined_char_class(input_line[i:], pattern):
                    exit(0)
                exit(1)
                
    if match_for_combined_char_class(input_line, pattern):
        print('YYYY')
        exit(0)
    else:
        print("NNN")
        exit(1)
    


if __name__ == "__main__":
    main()
