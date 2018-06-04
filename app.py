#apistar
from apistar import App, Route, Include, exceptions, http
from apistar.server.components import Component

#project modules
import components

#stdlib
import inspect, sys
from lib.importer import Importer
Importer(globals())
import os
import star as ModuleAPI

component_classes = inspect.getmembers(
    sys.modules[components.__name__],
    lambda member: inspect.isclass(member) and 
    issubclass(member, Component) and 
    member.__module__ == components.__name__
)
components = []
for component in component_classes:
    components.append(component[1]())

routes = []
BASE_PATH = ''
for submodule_name in ModuleAPI.__all__:
    m = getattr(ModuleAPI, submodule_name)
    if hasattr(m, "__routes__"):
        routes.append(Include(BASE_PATH, name=m.__route_name__, routes=m.__routes__))


app = App(routes=routes, components=components)

if __name__ == '__main__':
    app.serve('127.0.0.1', 8888, debug=True)