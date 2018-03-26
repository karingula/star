from apistar import Include, Route, reverse_url, Response, http, annotate, render_template, typesystem
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.renderers import HTMLRenderer
from sqlalchemy.engine import reflection
from apistar.exceptions import TypeSystemError
import pandas as pd
import typing, functools
from sqlalchemy.sql.base import ColumnCollection
from sqlalchemy.schema import Column
from sqlalchemy import inspect
import service
from models import Flight
from components import FlightComponent


class Rating(typesystem.Integer):
    minimum = 1
    maximum = 5


class Sports(typesystem.Enum):
    enum = ['cricket', 'golf', 'formula-1', 'horse_racing']


class Player(typesystem.Object):
    properties = {
        'name': typesystem.string(max_length=100),
        'rating': Rating,
        'sports': Sports,
        'retired': typesystem.boolean()
    }


def get_players():
    player_list = ['apple', 'mango', 'banana', 'carrot', 'radish']

    return player_list


def example(player_name):
    return "this is just an example"


@annotate(renderers=[HTMLRenderer()])
def get_player_details(player_name: str):
    return render_template('index.html', player_name=player_name)


def get_all_players(request: http.Request):
    players = get_players()
    player_list = [{'name': player, 'url': reverse_url(
        'get_player_details', player_name=player)} for player in players]

    data = {'players': player_list}
    # print(type(data))
    # return data
    headers = {'this_is_my_url': request.url}
    return Response(data, headers=headers, status=200)

def get_flight_details() -> typing.List[Flight]:
    data = [FlightComponent(instance)
            for instance in session.query(Flight).all()]
    print(type(data[0]['schedule']))
    return data


routes = [
    Route(path='/players/', method='GET', view=get_all_players),
    Route(path='/players/{player_name}/',
          method='GET', view=get_player_details),
    Route(path='/flight', method='GET', view=get_flight_details),
    Include('/docs', docs_urls),
]
settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',
        'PACKAGE_DIRS': ['apistar']  # Built-in apistar templates
    }
}

#getting all primary keys
pk_list = []
pk_list = [x.key for x in inspect(Flight).primary_key]
print("Normal Inspection:", pk_list)

#  Ripping __table_args__ apart for clear understanding
for z in Flight.__table_args__:
    # Each item of __table_args__ is an UniqueConstraint object
    # UniqueConstraint object inherits ColumnCollection object
    # ColumnCollection object inherits util.OrderedProperties object
    # OrderedProperties object inherits Properties object
    print(type(z))
    #__visit_name__, columns are properties of a Properties object
    print(z.__visit_name__)
    # columns is a ColumnCollection object which is iterable
    print(type(z.columns))
    for y in z.columns:
        # Each element of ColumnCollection object is a Column object from schema
        # ex: <class 'sqlalchemy.sql.schema.Column'>
        print(type(y))
        #name is the property of Column object which gives the name of the Column of SQLAlchemy model
        print(y.name)
    col_list = tuple([k.name for k in z.columns.__iter__()])
    print("This is col list:",col_list)

uc_cols = []
pk_cols = []
nul_cols = []
#getting all the columns involved in UniqueConstraints and PrimaryKeyConstraint separately
uc_cols, pk_cols = service.lisftify_columns(Flight)
pk_cols+=pk_list
#create a dataframe
list1 = [1, ('Vanc','ouver', 'Canada'), 'Toronto', '3-Jan']
list2 = [2, ('Amst','erdam', 'Netherlands'), None, '15-Feb']
list3 = [4, None, 'Glasgow', '12-Jan']
list4 = [9, ('Halm','stad', 'Norway'), 'Athens', '21-Jan']
list5 = [3, ('Bris','bane', 'Australia'), 'Toronto', None]
list6 = [4, ('Johan','nesburg', 'South Africa'), 'Venice', '12-Jan']
list7 = [9, None, None, '20-Oct']
data = [list1,list2,list3,list4,list5,list6,list7]
df = pd.DataFrame(data, columns=['flight_id','from_location','to_location','schedule'])

violation_checker = service.Violation()

#get all the columns which violated the unique constraints
uc_violations = list(map(functools.partial(violation_checker.fetch_violation_records_uniqueness, df=df), uc_cols))
print("UC_Violations",uc_violations)
# get all the columns which violated the primary key constraints
pk_violations = list(map(functools.partial(violation_checker.fetch_violation_records_uniqueness, df=df), pk_cols))
print("PK Violations:", pk_violations)
nul_cols = [col.name for col in Flight.__table__.columns if not col.nullable]
# print("Nullable Cols:",nul_cols)
nul_violations = violation_checker.fetch_violation_records_nullable(df=df,cols=nul_cols)
print("Nullable Violations:", nul_violations)
app = App(routes=routes, settings=settings)


if __name__ == '__main__':
    app.main()
