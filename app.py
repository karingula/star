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
from sqlalchemy import inspect, exists, and_, or_
import service
from models import Flight
from components import FlightComponent
from db import session, Base
import pandas as pd
from sqlalchemy.sql.elements import BinaryExpression, BindParameter
from sqlalchemy.sql.annotation import AnnotatedColumn


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

@annotate(renderers=[HTMLRenderer()])
def get_flight_details(request: http.Request) -> typing.List[Flight]:
    #form=FlightForm()
    print(request.method)
    data = [FlightComponent(instance)
            for instance in session.query(Flight).all()]
    return render_template('flights.html', data=data)

def get_specific_records(df, Model:Base, cols, session):
        """Execute bulk SQL SELECT on database
        Args:
            df (pandas.DataFrame): dataframe
            select_cols (list): columns to select
            and_cols (list): columns used to compose SQL query AND clauses
            session (sqlalchemy.orm.Session): handles commit/rollback behavior
        Returns:
            A pandas.DataFrame with the added translated column, if not already present in the pandas.DataFrame.
        """

        for x in cols:
            print(x)

        return "The Sun"

        or_clauses = df.apply(
            lambda r: and_(ac.__eq__(r[ac.name]) for ac in and_cols),
            axis=1
        ).tolist()

        s = session.query(
            Model
        ).filter(
            or_(*or_clauses)
        ).statement

        rtn_df = pd.read_sql(s, session.bind)

        return rtn_df

@annotate(renderers=[HTMLRenderer()])
def add_flight(data:http.RequestData):
    print("Inside the add flight details")
    print(type(data))
    print(type(Flight))
    flight_data = data.to_dict(flat=False)
    print(flight_data)
    df = pd.DataFrame.from_dict(flight_data, orient='columns')
    print(df)
    # getting all primary keys
    pk_list = []
    pk_list = [x for x in inspect(Flight).primary_key]
    uc_cols = []
    pk_cols = []
    nul_cols = []
    # #getting all the columns involved in UniqueConstraints and PrimaryKeyConstraint separately
    uc_cols, pk_cols = service.lisftify_columns(Flight)
    pk_cols+=pk_list
    rtn_df = get_specific_records(df, Flight, uc_cols, session)
    message = "DataFrame created!"
    return rtn_df
    return render_template('index.html', message=message)

routes = [
    Route('/players', 'GET', get_all_players),
    Route('/players/{player_name}', 'GET', get_player_details),
    Route('/flights', 'GET', get_flight_details),
    Route('/flight/add', 'POST' , add_flight),
]
engine_string = 'mysql+pymysql://root:@localhost/star'
settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',
        'PACKAGE_DIRS': ['apistar']  # Built-in apistar templates
    }
}

app = App(routes=routes, settings=settings)

if __name__ == '__main__':
    app.main()
