import pandas as pd
import os, sys


def get_isc_codes(fname=None):
    """
    Get ISC agency codes from csv file

    :param fname: String representing path to csv file, defaults to None
    :type fname: str
    :return df_agency_codes: An instance of :class:`pandas.DataFrame`  
    """
    if fname is None:
        raise FileNotFoundError('File path not specified.')
    
    df_agency_codes = pd.read_csv(fname, encoding='windows-1252')

    return df_agency_codes


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        DIRNAME = os.path.dirname(__file__)
        FILENAME = 'isc_agency_contributors.csv'
        FILEPATH = os.path.join(DIRNAME, FILENAME)
        args = [FILEPATH]

    df_agency_codes = [get_isc_codes(arg) for arg in args]