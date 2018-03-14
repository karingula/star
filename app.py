from apistar import Include, Route, reverse_url
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import http
import typing

def get_players():
    player_list = ['apple','mango','banana','carrot','radish']

    return player_list

def example(player_name):
    return "this is just an example"

def get_player_details(player_name):
    return {'name': player_name}


def get_all_players(request: http.Request):
    players = get_players()
    player_list = [{'name': player, 'url': reverse_url(
        'example', player_name=player)} for player in players]

    data = {'players': player_list}
    # print(type(data))
    # return data
    headers = {'this_is_my_url':request.url}
    return http.Response(data, headers=headers, status=200)


routes = [
    Route(path='/players/', method='GET', view=get_all_players),
    Route(path='/players/{player_name}/', method='GET', view=get_player_details),
    Route('/loli/{player_name}/', 'GET', example),
    Include('/docs', docs_urls),
]
app = App(routes=routes)

if __name__ == '__main__':
    app.main()
