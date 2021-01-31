import pandas as pd
import doctest
import sys

def errorCheck(pf, sf, myDict):
    '''
    errorCheck validates the values provided by myDict are valid.
    In other words 0 <= myDick.values() <= column count

    >>> myDict={'secondaryKeyPos': 1, 'primaryKeyPos': 0, 'grabPos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR with dictionary key names
    >>> myDict={'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': 1}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR grabPos must be tuple
    >>> myDict={'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': (3,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> myDict={'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': (-1,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> myDict={'primaryKeyPos': -1, 'secondaryKeyPos': 1, 'grabPos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> myDict={'primaryKeyPos': 3, 'secondaryKeyPos': 1, 'grabPos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> myDict={'primaryKeyPos': 0, 'secondaryKeyPos': -1, 'grabPos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    >>> myDict={'primaryKeyPos': 0, 'secondaryKeyPos': 3, 'grabPos': (2,)}; a = pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]});errorCheck(a,a,myDict)
    Traceback (most recent call last):
    ...
    Exception: ERROR dictionary element out of range
    '''
    # error check myDict
    if [key for key in myDict.keys()] != ['primaryKeyPos', 'secondaryKeyPos', 'grabPos']:
        raise Exception('ERROR with dictionary key names')

    # error check tuple
    if type(myDict['grabPos']) is not tuple:
        raise Exception('ERROR grabPos must be tuple')

    # error check 0<=keys<=cols
    if myDict['primaryKeyPos'] > len(pf.columns) - 1 \
            or myDict['secondaryKeyPos'] > len(sf.columns) - 1 \
            or True in [myDict['grabPos'][i] > len(sf.columns) - 1 for i in range(len(myDict['grabPos']))] \
            or myDict['primaryKeyPos'] < 0 \
            or myDict['secondaryKeyPos'] < 0 \
            or True in [myDict['grabPos'][i] < 0 for i in range(len(myDict['grabPos']))]:
        raise Exception('ERROR dictionary element out of range')

def csv_grab(primaryFile, secondaryFile, outputFile, myDict):
    '''
    csv_grab reads in 2 csvs then checks row by row if the primary key (as defined in myDict['primaryKeyPos'])
    in the first csv matches the secondary key (as defined in myDict['secondaryKeyPos']) in the secondary csv.
    If there is a match then the columns (as defined in myDict['grabPos']) are concatenated to the first csv
    which is written to the outputFile

    myDict = {'primaryKeyPos': #, 'secondaryKeyPos': #, 'grabPos': (#,)}
    grabPos is a tuple

    example
    ~$ python csv_grab.py foo.csv bar.csv out.csv '{"primaryKeyPos": 0, "secondaryKeyPos": 1, "grabPos": (2,)}'

    run tests
    ~$ python -m doctest -v csv_grab.pu
    '''
    # read in csv
    pf = pd.read_csv(primaryFile)
    sf = pd.read_csv(secondaryFile)

    errorCheck(pf,sf,myDict)

    # check if primary match secondary
    pKeys = [*pf[pf.columns[myDict['primaryKeyPos']]]]
    sKeys = [*sf[sf.columns[myDict['secondaryKeyPos']]]]
    for pKey, sKey in zip(pKeys, sKeys):
        if pKey == sKey:
            # grab and append
            getCol = lambda i: sf[sf.columns[i]]
            colList = list(map(getCol, myDict['grabPos']))
            for col in colList:
                pf[col.name] = col
            # stop on first match
            break

    # write csv
    with open(outputFile, 'w') as f:
        # header
        f.write(','.join(pf.columns)+'\n')
        # rows
        for i in range(len(pf.index)):
            f.write(','.join([str(j) for j in pf.loc[i]])+'\n')


if __name__=='__main__':
    if len(sys.argv) == 1:
        # debug
        # ~$ python csv_grab.py
        test = {'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': (2,)}
        csv_grab('test0.csv', 'test1.csv', 'out.csv', test)
    else:
        argDict = eval(sys.argv[4])
        csv_grab(sys.argv[1], sys.argv[2], sys.argv[3], argDict)
