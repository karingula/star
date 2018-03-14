from apistar import Include, Route, reverse_url
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import http
import typing

def get_players():
    player_list = ['apple','mango','banana','carrot','radish']

    return player_list

def get_player_details(player_name):
    return {'name': player_name}


def get_all_players():
    players = get_players()
    player_list = [{'name': player, 'url': reverse_url(
        'get_player_details', player_name=player)} for player in players]

    return {'players': player_list}


routes = [
    Route(path='/players/', method='GET', view=get_all_players),
    Route(path='/players/{player_name}/', method='GET', view=get_player_details),
    Include('/docs', docs_urls),
]
app = App(routes=routes)

if __name__ == '__main__':
    app.main()
