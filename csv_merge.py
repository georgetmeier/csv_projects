import sys
import pandas as pd


def csv_to_pandas(csv1: str, csv2: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    input: 'example.csv'
    csv must have header
    both csvs must have the same header
    '''
    primary_frame = pd.read_csv(csv1)
    secondary_frame = pd.read_csv(csv2)
    # exit if keys do not match
    if [*primary_frame.columns] != [*secondary_frame.columns]:
        raise Exception('ERROR: non-matching headers')
    return primary_frame, secondary_frame


def pandas_to_dict(primary_frame: pd.DataFrame, secondary_frame: pd.DataFrame) -> dict[str, int]:
    '''
    combine keys from pandas and make a dict, add values on collision
    the last column is the value the preceding columns as keys
    k1,k2,k3,v -> {'k1k2k3': v}

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

    # make a dictionary of composite keys and values
    # 'x' 'y' 'z' -> {'aa': 1, 'ab': 1}
    # 'a' 'a'  0
    # 'a' 'b'  1
    primary_dict = {', '.join(str(primary_frame.iloc[i][j]) for j in range(primary_frame.shape[1] - 1))
                        : primary_frame.iloc[i][-1]
                    for i in range(primary_frame.shape[0])}
    secondary_dict = {', '.join(str(secondary_frame.iloc[i][j]) for j in range(secondary_frame.shape[1] - 1))
                          : secondary_frame.iloc[i][-1]
                      for i in range(secondary_frame.shape[0])}

    # merge dict adding values where keys match
    for k, v in secondary_dict.items():
        if k in primary_dict.keys():
            primary_dict[k] += int(v)
        else:
            primary_dict[k] = int(v)

    return primary_dict


def write_csv(headers: list[str], primary_dict: dict[str, int], outcsv: str) -> None:
    with open(outcsv, 'w') as f:
        f.write(','.join(headers) + '\n')
        for key in primary_dict.keys():
            f.write(f"{','.join(key.split(','))}, {primary_dict[key]}\n")


def csv_merge(csv1: str, csv2: str, outcsv: str) -> None:
    '''
    main function
    '''
    primary_frame, secondary_frame = csv_to_pandas(csv1, csv2)
    d = pandas_to_dict(primary_frame, secondary_frame)
    write_csv(primary_frame.columns, d, outcsv)


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
        csv_merge('test0.csv', 'test1.csv', 'out.csv')
    elif len(sys.argv) < 4:
        print('missing arguments')
    else:
        csv_merge(sys.argv[1], sys.argv[2], sys.argv[3])
