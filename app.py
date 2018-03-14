from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import http
import typing

def details() -> int:
    age = 25
    name = 'karingula'

    return age

def welcome(name: str, request: http.Request, data: http.RequestData):
    data = {"message": f'welcome to {name}'}
    data['age'] = details()
    print(type(name))
    print(name)
    # return{
    # 'method': request.method,
    #'url': request.url,
    # 'headers': dict(request.headers),
    # #'params': dict(query_params),
    # #'user_agent': dict(user_agent),#here request.headers & http.Headers both are same
    # 'data': data
    # }
    headers={'Location': '/greeting',
             'url': request.url
    }

    return http.Response(data, headers=headers, status=200)

routes = [
    Route(path='/greeting/{name}', method='GET', view=welcome),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
print(static_urls)

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
