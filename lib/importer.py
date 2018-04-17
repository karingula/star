""" Module for loading all classes as submodules """

import sys, os, pathlib, inspect, importlib

class Importer(object):
    """ Imports the current module from anywhere in the module"""

    scope = {} # The global scope of the calling module
    file = '' # The fill path to the init file for this module

    def __init__(self, scope=None, level=0):
        """summary
        Args:
            scope (dict): The globals from the calling function
            level (int): The number of directories to relatively walk up to the root module
        """

        # Gets the scope from arguments or calling function
        self._get_scope_variables(scope)

        modulepath = str(pathlib.Path(os.path.abspath(self.file)).parents[level])
        modulelocation, modulename = os.path.split(modulepath)
        if modulelocation not in sys.path:
            sys.path.append(modulelocation)
        __import__(modulename)

    def _get_scope_variables(self, scope):
        """ Gets the scope from argument or callstack
        Args:
            scope (dict): The global scope for the base module
        """

        if scope is None:
            self.scope = inspect.stack(0)[2][0].f_globals
        else:
            self.scope = scope

        self.file = self.scope.get('__file__')
