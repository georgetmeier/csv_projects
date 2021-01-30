import sys
import pandas as pd

def csv_to_pandas(csv1: str, csv2: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    input is a string 'example.csv'
    csv must have header
    both csvs must have the same header
    '''
    p1 = pd.read_csv(csv1)
    p2 = pd.read_csv(csv2)
    # exit if keys do not match
    if [i for i in p1.columns] != [i for i in p2.columns]:
        raise Exception('ERROR: non-matching headers')
    return p1, p2

def pandas_to_dict(p1: pd.DataFrame, p2: pd.DataFrame) -> dict[str, int]:
    '''
    combine keys from pandas and make a  dict, add values on collision

    add test
    >>> pandas_to_dict(pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}),
    ...                pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}))
    {'a, a': 2, 'b, b': 4, 'c, c': 6}

    join test
    >>> pandas_to_dict(pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}),
    ...                pd.DataFrame(data={'x': ['d', 'e', 'f'], 'y': ['d','e','f'], 'z': [1,2,3]}))
    {'a, a': 1, 'b, b': 2, 'c, c': 3, 'd, d': 1, 'e, e': 2, 'f, f': 3}

    join and add test
    >>> pandas_to_dict(pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}),
    ...                pd.DataFrame(data={'x': ['a', 'e', 'f'], 'y': ['a','e','f'], 'z': [1,2,3]}))
    {'a, a': 2, 'b, b': 2, 'c, c': 3, 'e, e': 2, 'f, f': 3}

    add empty test
    >>> pandas_to_dict(pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}),
    ...                pd.DataFrame(data={'x':[], 'y':[], 'z':[]}))
    {'a, a': 1, 'b, b': 2, 'c, c': 3}

    add to empty test
    >>> pandas_to_dict(pd.DataFrame(data={'x':[], 'y':[], 'z':[]}),
    ...                pd.DataFrame(data={'x': ['a', 'b', 'c'], 'y': ['a','b','c'], 'z': [1,2,3]}))
    {'a, a': 1, 'b, b': 2, 'c, c': 3}
    '''

    p1Dict = {}
    for i in range(len(p1)):
        p1Dict[', '.join(str(p1.iloc[i][j]) for j in range(len(p1.iloc[0])-1))] = p1.iloc[i][-1]
    p2Dict = {}
    for i in range(len(p2)):
        p2Dict[', '.join(str(p2.iloc[i][j]) for j in range(len(p2.iloc[0])-1))] = p2.iloc[i][-1]

    # merge dict adding values where keys match
    for k,v in p2Dict.items():
        if k in p1Dict.keys():
            p1Dict[k] += int(v)
        else:
            p1Dict[k] = int(v)

    return p1Dict

def write_csv(headers: list[str], pDict: dict[str, int], outcsv: str) -> None:
    with open(outcsv, 'w') as f:
        f.write(','.join(headers)+'\n')
        for key in pDict.keys():
            f.write(f"{','.join(key.split(','))}, {pDict[key]}\n")


def csv_merge(csv1: str, csv2: str, outcsv: str) -> None:
    '''
    call this one
    '''
    p1, p2 = csv_to_pandas(csv1, csv2)
    d = pandas_to_dict(p1, p2)
    write_csv(p1.columns, d, outcsv)

if __name__ == '__main__':
    '''
    run unit test
        python csv_merge.py
        python csv_merge.py -v
    use
        python csv_merge foo.csv bar.csv out.csv
        import csv_merge; csv_merge.csv_merge('foo.csv', 'bar.csv', 'out.csv')
    '''
    if len(sys.argv) <= 2:
        import doctest
        doctest.testmod()
    elif len(sys.argv) < 4:
        print('missing arguments')
    else:
        csv_merge(sys.argv[1], sys.argv[2], sys.argv[3])
