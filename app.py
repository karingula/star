from apistar import Include, Route, http
from apistar import App
from sqlalchemy.engine import reflection
import pandas as pd
import typing, functools
from sqlalchemy.sql.base import ColumnCollection
from sqlalchemy.schema import Column
from sqlalchemy import inspect
import service
from db import session
import pandas as pd
import csv
from lib.importer import Importer
Importer(globals())
import os
import star as ModuleAPI
    # df = pd.DataFrame.from_dict(flight_data, orient='columns')
    #----------- Creating a dummy dataframe for testing purposes
    # list1 = ['Halmstad', 'Athens', '2018-01-21']
    # list2 = ['Johannesburg', 'Venice', '2018-01-12']
    # list3 = ['Boston', 'Amsterdam', '2018-08-21']
    # data = [list1, list2,list3]
    # df = pd.DataFrame(data,columns=['from_location','to_location','schedule'])
    # # getting all primary keys
    # pk_list = []
    # pk_list = [x for x in inspect(Flight).primary_key]
    # uc_cols = []
    # pk_cols = []
    # nul_cols = []
    # # get all the columns involved in UniqueConstraints and PrimaryKeyConstraint separately
    # uc_cols, pk_cols = service.lisftify_columns(Flight)
    # pk_cols+=pk_list
    # #get all the records of df which are already in database
    # rtn_df = service.get_specific_records(df, Flight, uc_cols, session)
    # message = "DataFrame created!"

    # return render_template('index.html', message=message)
    # Routes for endpoint modules
# file_directory = os.path.dirname(os.path.abspath(__file__))
# source_directory = os.path.abspath(os.curdir)+'/src'
# for pkg in os.listdir(source_directory):
settings={}
routes = []
BASE_PATH = ''
for submodule_name in ModuleAPI.__all__:
    m = getattr(ModuleAPI, submodule_name)
    if hasattr(m, "__routes__"):
        routes.append(Include(BASE_PATH, name=m.__route_name__, routes=m.__routes__))

engine_string = 'mysql+pymysql://root:@localhost/star'
settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',
        'PACKAGE_DIRS': ['apistar']  # Built-in apistar templates
    }
}
app = App(routes=routes)
if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, use_debugger=True, use_reloader=True)
