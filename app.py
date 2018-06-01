#apistar
from apistar import App, Route, exceptions, http
from apistar.server.components import Component

#project modules
from views import eat_nicely, eat_fancy
import components

#stdlib
import inspect, sys

component_classes = inspect.getmembers(
    sys.modules[components.__name__],
    lambda member: inspect.isclass(member) and 
    issubclass(member, Component) and 
    member.__module__ == components.__name__
)
components = []
for component in component_classes:
    components.append(component[1]())

routes = [
    Route('/', method='GET', handler=eat_nicely),
    Route('/fancy/', method='GET', handler=eat_fancy)
]

app = App(routes=routes, components=components)

if __name__ == '__main__':
    app.serve('127.0.0.1', 8888, debug=True)