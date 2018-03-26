from apistar import typesystem
import typing
# custom typesystem type

class Violation():
    def fetch_violation_records(self, col_collection, df):
        v_records = df.groupby(col_collection).apply(lambda d: tuple(d.index) if len(d.index) > 1 else None).dropna().tolist()
        #append only if v_records is not empty
        if v_records:
            v_records.append(col_collection)
        return tuple(v_records)

class Date(typesystem.Object):
    native_type = str
    errors = {
        'type': 'Must be a valid date with the format "YYYY-mm-dd" '
    }

    def __new__(cls, *args, **kwargs) -> str:
        if isinstance(args[0], datetime.date):
            try:
                return datetime.datetime.strptime(str(args[0]), '%Y-%m-%d').strftime('%b %d %Y')
            except KeyError:
                raise TypeSystemError(cls=cls, code='type')
        elif not args:
            return args
        else:
            raise TypeSystemError(cls=cls, code='type')


def date(**kwargs) -> typing.Type:
    return type('Date', (Date,), kwargs)

def lisftify_columns(Table):
    '''Get all the Columns enforced by constraints
    '''
    pk_cols = []
    uc_cols = []
    for z in Table.__table_args__:
        if z.__visit_name__ == 'unique_constraint':
            uc_cols.append(tuple([k.name for k in z.columns.__iter__()]))
        elif z.__visit_name__ == 'primary_key_constraint':
            pk_cols.append(tuple([k.name for k in z.columns.__iter__()]))
    return uc_cols, pk_cols
