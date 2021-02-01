import pandas as pd
import doctest
import sys

def error_check(primary_frame: pd.DataFrame, secondary_frame: pd.DataFrame, my_dict: dict[str:int, str:int, str:tuple[int]]):
    '''
    error_check validates the values provided by my_dict are valid.
    In other words 0 <= my_dict.values() <= column count

    >>> my_dict={'secondary_key_pos': 1, 'primary_key_pos': 0, 'grab_pos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR with dictionary key names
    >>> my_dict={'primary_key_pos': 0, 'secondary_key_pos': 1, 'grab_pos': 1}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR grab_pos must be tuple
    >>> my_dict={'primary_key_pos': 0, 'secondary_key_pos': 1, 'grab_pos': (3,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> my_dict={'primary_key_pos': 0, 'secondary_key_pos': 1, 'grab_pos': (-1,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> my_dict={'primary_key_pos': -1, 'secondary_key_pos': 1, 'grab_pos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> my_dict={'primary_key_pos': 3, 'secondary_key_pos': 1, 'grab_pos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> my_dict={'primary_key_pos': 0, 'secondary_key_pos': -1, 'grab_pos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> my_dict={'primary_key_pos': 0, 'secondary_key_pos': 3, 'grab_pos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});error_check(a,a,my_dict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    '''
    primary_key_pos, secondary_key_pos, grab_pos = my_dict.values()

    # error check my_dict
    if [*my_dict.keys()] != ['primary_key_pos', 'secondary_key_pos', 'grab_pos']:
        raise Exception('ERROR with dictionary key names')

    # error check tuple
    if type(grab_pos) is not tuple:
        raise Exception('ERROR grab_pos must be tuple')

    # error check 0<=keys<=cols
    if primary_key_pos > len(primary_frame.columns) - 1 \
            or secondary_key_pos > len(secondary_frame.columns) - 1 \
            or True in [grab_pos[i] > len(secondary_frame.columns) - 1 for i in range(len(grab_pos))] \
            or primary_key_pos < 0 \
            or secondary_key_pos < 0 \
            or True in [grab_pos[i] < 0 for i in range(len(grab_pos))]:
        raise Exception('ERROR dictionary element out of range')

def csv_grab(primary_file: str, secondary_file: str, output_file: str, my_dict: dict[str:int, str:int, str:tuple[int]]) -> None:
    '''
    csv_grab reads in 2 csvs then checks row by row if the primary key (as defined in primary_key_pos)
    in the first csv matches the secondary key (as defined in secondary_key_pos) in the secondary csv.
    If there is a match then the columns (as defined in grab_pos) are concatenated to the first csv
    which is written to the outputFile

    my_dict = {'primary_key_pos': #, 'secondary_key_pos': #, 'grab_pos': (#,)}
    grab_pos is a tuple

    example
    ~$ python csv_grab.py foo.csv bar.csv out.csv '{"primary_key_pos": 0, "secondary_key_pos": 1, "grab_pos": (2,)}'

    run tests
    ~$ python -m doctest -v csv_grab.pu
    '''
    # read in csv
    primary_frame = pd.read_csv(primary_file)
    secondary_frame = pd.read_csv(secondary_file)

    error_check(primaryFrame, secondaryFrame, my_dict)

    # check if primary match secondary
    primary_key_pos, secondary_key_pos, grab_pos = my_dict.values()
    for primary_key, secondary_key in zip(primary_frame[primary_frame.columns[primary_key_pos]],
                                    secondary_Frame[secondary_frame.columns[secondary_key_pos]]):
        if primaryKey == secondaryKey:
            # make list of columns to add
            columns_to_add = list(map(lambda index: secondary_frame[secondary_frame.columns[index]], grab_pos))
            for column in columns_to_add:
                primary_frame[column.name] = column
            # stop on first match
            break

    # write csv
    with open(output_file, 'w') as f:
        # header
        f.write(','.join(primary_frame.columns) + '\n')
        # rows
        for index in range(len(primary_frame.index)):
            f.write(','.join([str(item) for item in primary_frame.loc[index]]) + '\n')


if __name__=='__main__':
    if len(sys.argv) == 1:
        # debug
        # ~$ python csv_grab.py
        test = {'primary_key_pos': 0, 'secondary_key_pos': 1, 'grab_pos': (2,)}
        csv_grab('test0.csv', 'test1.csv', 'out.csv', test)
    else:
        arg_dict = eval(sys.argv[4])
        csv_grab(sys.argv[1], sys.argv[2], sys.argv[3], arg_dict)
