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
from db import session
import pandas as pd

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

@annotate(renderers=[HTMLRenderer()])
def add_flight(data:http.RequestData):

    #---------Getting the data from form and constructing the Dataframe
    # flight_data = data.to_dict(flat=False)
    # print(flight_data)
    # df = pd.DataFrame.from_dict(flight_data, orient='columns')

    #----------- Creating a dummy dataframe for testing purposes
    list1 = ['Halmstad', 'Athens', '2018-01-21']
    list2 = ['Johannesburg', 'Venice', '2018-01-12']
    list3 = ['Boston', 'Amsterdam', '2018-08-21']
    data = [list1, list2,list3]
    df = pd.DataFrame(data,columns=['from_location','to_location','schedule'])
    # getting all primary keys
    pk_list = []
    pk_list = [x for x in inspect(Flight).primary_key]
    uc_cols = []
    pk_cols = []
    nul_cols = []
    # get all the columns involved in UniqueConstraints and PrimaryKeyConstraint separately
    uc_cols, pk_cols = service.lisftify_columns(Flight)
    pk_cols+=pk_list
    #get all the records of df which are already in database
    rtn_df = service.get_specific_records(df, Flight, uc_cols, session)

    message = "DataFrame created!"

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
