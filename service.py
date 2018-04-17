from apistar import types, validators
from db import Base
import typing, datetime
from functools import partial
from sqlalchemy import and_, or_
import pandas as pd

class Violation():

    def fetch_violation_records_uniqueness(self, col_collection, df):
        v_records = []
        v_records = df.groupby(col_collection).apply(lambda d: tuple(d.index) if len(d.index) > 1 else None).dropna().values.tolist()
        #append only if v_records is not empty
        if v_records:
            v_records.append(col_collection)
        return tuple(v_records)

    def fetch_violation_records_nullable(self, df, cols):
        #s is a Series
        s = df[cols].stack(dropna=False)
        v_data = s[s.isnull()]
        v_records = [v_data.index[i] for i in range(v_data.size)]
        return v_records

# custom typesystem type
# class Date(typesystem.Object):
#     native_type = str
#     errors = {
#         'type': 'Must be a valid date with the format "YYYY-mm-dd"'
#     }
#
#     def __new__(cls, *args, **kwargs) -> str:
#         if isinstance(args[0], datetime.date):
#             try:
#                 return datetime.datetime.strptime(str(args[0]), '%Y-%m-%d').strftime('%b %d %Y')
#             except KeyError:
#                 raise TypeSystemError(cls=cls, code='type')
#         elif not args:
#             return args
#         else:
#             raise TypeSystemError(cls=cls, code='type')
#
#
# def date(**kwargs) -> typing.Type:
#     return type('Date', (Date,), kwargs)

def lisftify_columns(Table):
    '''Get all the Columns enforced by constraints
    '''
    pk_cols = []
    uc_cols = []
    for z in Table.__table_args__:
        if z.__visit_name__ == 'unique_constraint':
            uc_cols.append(tuple([k for k in z.columns.__iter__()]))
        elif z.__visit_name__ == 'primary_key_constraint':
            pk_cols.append(tuple([k for k in z.columns.__iter__()]))
    return uc_cols, pk_cols

def get_a_o_list(row, cols):

    o_list = []
    for col_tup in cols:
        a_list = []
        for col in col_tup:
            a_list.append(col.__eq__(row[col.name]))
        o_list.append(a_list)
    return o_list

def get_specific_records(df, Model:Base, cols, session):
    """Execute bulk SQL SELECT on database
    Args:
        df (pandas.DataFrame): dataframe
        cols (list of tuples): column patterns on which there are constraints
        session (sqlalchemy.orm.Session): handles commit/rollback behavior
    Returns:
        A pandas.DataFrame with the added translated column, if not already present in the pandas.DataFrame.
    """

    arguments = partial(get_a_o_list, cols=cols)
    #This(bexp_list)is a Series object if not casted to list
    bexp_list = df.apply(arguments, axis=1).tolist()
    flat_bexp_list = [item for sub_list in bexp_list for item in sub_list]
    or_clause = [and_(*b_exp) for b_exp in flat_bexp_list]
    s = session.query(Model).filter(or_(*or_clause)).statement
    rtn_df = pd.read_sql(s, session.bind)
    print(rtn_df)

    return rtn_df
