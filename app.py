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
    from_location = Column(String)
    to_location = Column(String)
    schedule = Column(String)
    __table_args__ = (UniqueConstraint('flight_id', 'schedule', name='flight_schedule'),)

# Flight Component


class FlightComponent(typesystem.Object):
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
fine_grained_inspector = reflection.Inspector.from_engine(engine)
#get all the table names. Apistar implicityly encodes the below list_of_unicoded_tablenames
list_of_unicoded_tablenames = fine_grained_inspector.get_table_names()
#table names are unicoded. so encode to normal strings
#list_of_tablenames = [table_name.encode("utf-8") for table_name in list_of_unicoded_tablenames]
print(list_of_unicoded_tablenames)
ins = inspect(Flight)
for x in ins.primary_key:
    print(x.key)
app = App(routes=routes, settings=settings)

if __name__ == '__main__':
    app.main()
