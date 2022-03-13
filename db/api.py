import pathlib
import sqlite3
import pandas as pd


DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("multi_table.db").resolve()

# categorical = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome', 'y']

def get_data(start, end):
    """
    Query continuous column data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT * FROM smartphone_sensor WHERE timestamp > {start} AND timestamp <= {end};'
    df = pd.read_sql_query(statement, con)
    # df.drop(categorical, axis=1, inplace=True)
    
    return df


def get_drop_down(col):
    """Query the first 1000 rows of our target column and feature column
    :params col: feature column
    :returns: pandas dataframe
    """

    target = "Z-AxisAgle(Azimuth)"

    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT "{col}", "{target}" FROM smartphone_sensor LIMIT 0, 1000;'
    df = pd.read_sql_query(statement, con)

    return df


def get_timestamp(rowid):
    """
    Query a row from the timestamp table

    :params id: a row id
    :returns: pandas dataframe object
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = f'''SELECT * FROM pointsmapping INNER JOIN timestamp ON timestamp.tid = pointsmapping.ID;'''
    label_df = pd.read_sql_query(statement, con)

    start, end = label_df["arrival"][rowid], label_df["departure"][rowid] 
    
    return start, end 
