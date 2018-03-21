from apistar import Include, Route, reverse_url, Response, http, typesystem, annotate, render_template
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.renderers import HTMLRenderer
import datetime
import typing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, create_engine, Integer, String, Date, Column, ForeignKey, UniqueConstraint
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
from apistar.exceptions import TypeSystemError
import pandas as pd
from collections import defaultdict
import json
from sqlalchemy.sql.base import ColumnCollection
from sqlalchemy.schema import Column

Base = declarative_base()

# custom typesystem type


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

# Flight model


class Flight(Base):
    __tablename__ = 'flight'

    flight_id = Column(Integer, primary_key=True)
    from_location = Column(String, unique=True)
    to_location = Column(String)
    schedule = Column(String)
    __table_args__ = (UniqueConstraint('flight_id', 'schedule', name='flight_schedule'),
                      UniqueConstraint('to_location', name='to'))

# Flight Component


class FlightComponent(object):
    properties = {
        'flight_id': typesystem.integer(),
        'from_location': typesystem.string(max_length=100),
        'to_location': typesystem.string(max_length=100),
        'schedule': date(),
    }


# create db connection
engine_string = 'mysql+pymysql://root:@localhost/star'
engine = create_engine(engine_string)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


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
    return json.dumps(output, default=myconverter)


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
#One way of getting all primary keys
fine_grained_inspector = reflection.Inspector.from_engine(engine)
print("PK:",fine_grained_inspector.get_pk_constraint("flight"))

#Second way of getting all primary keys
ins = inspect(Flight)
for x in ins.primary_key:
    print(x.key)

#get all the table names. Apistar implicityly encodes the below list_of_unicoded_tablenames
list_of_unicoded_tablenames = fine_grained_inspector.get_table_names()

#Away from Apistar, we need to explicitly encode
#table names are unicoded. so encode to normal strings
#list_of_tablenames = [table_name.encode("utf-8") for table_name in list_of_unicoded_tablenames]

#--------------
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
    print(col_list)

# print("UNIQUE: %r" % fine_grained_inspector.__table_args__)

app = App(routes=routes, settings=settings)

if __name__ == '__main__':
    app.main()
