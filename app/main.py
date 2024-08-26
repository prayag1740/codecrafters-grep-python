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

def match_for_combined_char_class(input_line, pattern):
    j = 0
    i = 0
    
    while i < len(pattern):
        ch_ip = pattern[i]
        if ch_ip == "\\":
            i = i +1
            ch_ip_next = pattern[i]
            if ch_ip_next == "d":
                if not match_for_integer(input_line[j]):
                    return False
                j +=1
            elif ch_ip_next == "w":
                if not match_for_alphanumeric(input_line[j]):
                    return False
                j +=1
        else:
            if input_line[j] != pattern[i]:
                return False
            j +=1
        i +=1
            
    return True
                

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
          
            
    #check for combined char class
    if match_for_combined_char_class(input_line, pattern):
        print("yyy")
        exit(0)
    else:
        print("noo")
        exit(1)
    


if __name__ == "__main__":
    main()
