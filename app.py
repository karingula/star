from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import http



def welcome(request: http.Request, query_params: http.QueryParams, user_agent: http.Headers):
    return {
    'method': request.method,
    'url': request.url,
    'headers': dict(request.headers),
    'params': dict(query_params),
    'user_agent': dict(user_agent),#here request.headers & http.Headers both are same

    }


routes = [
    Route('/', 'GET', welcome),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
