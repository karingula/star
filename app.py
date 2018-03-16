from apistar import Include, Route, reverse_url, Response, http, typesystem, annotate, render_template
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.renderers import HTMLRenderer
import typing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#Flight model
class Flight(Base):
    __tablename__ = 'flight'

    flight_id = Column(Integer, primary_key=True)
    from_location = Column(String)
    to_location = Column(String)
    schedule = Column(Date)

#create db connection
engine_string = 'mysql+pymysql://root:@localhost/star'
engine = create_engine(engine_string)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session=Session()

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

for instance in session.query(Flight).all():
    print(instance.flight_id, instance.from_location, instance.to_location, instance.schedule)

routes = [
    Route(path='/players/', method='GET', view=get_all_players),
    Route(path='/players/{player_name}/',
          method='GET', view=get_player_details),
    Include('/docs', docs_urls),
]
settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',
        'PACKAGE_DIRS': ['apistar']  # Built-in apistar templates
    }
}
app = App(routes=routes, settings=settings)

if __name__ == '__main__':
    app.main()
