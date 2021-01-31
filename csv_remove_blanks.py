import sys

def remove_blank_lines(input: str):
    '''
    removes the blank lines in an input file
    '''
    with open(input) as f:
        cleanedRows = [row for row in f if row != '\n']
    with open(input, 'w') as f:
        f.write(''.join([*cleanedRows]))

if __name__ == '__main__':
    try:
        remove_blank_lines(sys.argv[1])
    except:
        pass
