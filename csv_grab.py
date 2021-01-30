import pandas as pd

def csv_grab(primaryFile, secondaryFile, outputFile, myDict):
    '''
    myDict = {'primaryKeyPos': #, 'secondaryKeyPos': #, 'grabPos': (#,)}
    grabPos is a tuple (a tuple of 1 looks like (#,))
    '''

    # tuple check
    if type(myDict['grabPos']) is not tuple:
        raise Exception('grabPos must be tuple')

    # read in csv
    pf = pd.read_csv(primaryFile)
    sf = pd.read_csv(secondaryFile)

    # error check keys in bounds
    if myDict['primaryKeyPos'] > len(pf.columns)-1 \
            or myDict['secondaryKeyPos'] > len(sf.columns)-1 \
            or True in [myDict['grabPos'][i] > len(sf.columns)-1 for i in range(len(myDict['grabPos']))]:
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
    d = {'primaryKeyPos': 0, 'secondaryKeyPos': 1, 'grabPos': (2,)}
    foo=csv_grab('test0.csv', 'test1.csv', 'out.csv', d)

