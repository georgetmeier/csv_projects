import pandas as pd
import json
import sys

def csv_grab(primaryFile, secondaryFile, outputFile, myDict):
    '''
    myDict = {'primaryKeyPos': #, 'secondaryKeyPos': #, 'grabPos': (#,)}
    grabPos is a tuple

    example
    ~$ python csv_grab.py foo.csv bar.csv out.csv '{"primaryKeyPos": 0, "secondaryKeyPos": 1, "grabPos": (2,)}'
    '''
    # read in csv
    pf = pd.read_csv(primaryFile)
    sf = pd.read_csv(secondaryFile)

    # error check myDict
    if [key for key in myDict.keys()] != ['primaryKeyPos', 'secondaryKeyPos', 'grabPos']:
        raise Exception('ERROR with dictionary key names')

    # error check tuple
    if type(myDict['grabPos']) is not tuple:
        raise Exception('ERROR grabPos must be tuple')

    # error check 0<=keys<=cols
    if myDict['primaryKeyPos'] > len(pf.columns)-1 \
            or myDict['secondaryKeyPos'] > len(sf.columns) - 1 \
            or True in [myDict['grabPos'][i] > len(sf.columns) - 1 for i in range(len(myDict['grabPos']))] \
            or myDict['primaryKeyPos'] < 0 \
            or myDict['secondaryKeyPos'] < 0 \
            or True in [myDict['grabPos'][i] < 0 for i in range(len(myDict['grabPos']))]:
        raise Exception('ERROR dictionary element out of range')

    # check if primary match secondary
    pKeys = [i for i in pf[pf.columns[myDict['primaryKeyPos']]]]
    sKeys = [i for i in sf[sf.columns[myDict['secondaryKeyPos']]]]
    for pKey, sKey in zip(pKeys, sKeys):
        if pKey == sKey:
            # grab and append
            getCol = lambda i: sf[sf.columns[i]]
            colList = list(map(getCol, myDict['grabPos']))
            for col in colList:
                pf[col.name] = col
            break

    # write csv
    with open(outputFile, 'w') as f:
        # header
        f.write(','.join(pf.columns)+'\n')
        # rows
        for i in range(len(pf.index)):
            f.write(','.join([str(j) for j in pf.loc[i]])+'\n')


if __name__=='__main__':
    if len(sys.argv) <= 1:
        test = {'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': (2,)}
        csv_grab('test0.csv', 'test1.csv', 'out.csv', test)
    else:
        argDict = eval(sys.argv[4])
        csv_grab(sys.argv[1], sys.argv[2], sys.argv[3], argDict)