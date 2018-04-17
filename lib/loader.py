""" Module for loading all classes as submodules """

import os
import pathlib
import importlib
import inspect

from .output import Color, Log

class Loader(object):
    """ A module for imports all the submodules and classes and exposing them at root of calling module."""

    class_functions = {} # Dictionary of classes and function names
    expose = [] # Classes that are not part of this module but we still want to expose
    scope = {} # The global scope of the calling module
    source = '' # The source directory to walk through and find submodules
    name = '' # The name of this module
    package = '' # The name of this package
    location = '' # The directory location where this module resides
    path = '' # Path to the module may differ from location
    file = '' # The fill path to the init file for this module


    def __init__(self, scope=None, source=None, expose=None):
        """ Constructor for the loader module
        Note:
            This is the entrypoint to the functionality. Pass the global scope from the calling object.
        Args:
            scope (dict): The globals from the calling function
            source (str): The source to begin inspection from. Will walk recursively
        """

        if __debug__:
            import time
            start_time = time.time()

        # Gets the scope from arguments or calling function
        self._get_scope_variables(scope)

        if __debug__:
            Log.debug(Color.CYAN, 'Loading', self.name)

        # Gets the class names to expose from arguments or calling function
        self._get_expose_classes(expose)

        # Forceing to clear on init
        self.class_functions = {}
        self.scope['__all__'] = []

        # Get the scope and library from arguments or global
        self._get_source_location(source)

        # Iterate over the files in this module and add the classes in them
        if self.source is not None:
            self.location = os.path.join(self.location, self.source)

        # Walk through the directories finding modules and classes
        self.walk_directory_structure(self.location)

        if __debug__:
            seconds = time.time() - start_time
            Log.debug(Color.GREEN, 'Loaded', self.name, seconds=seconds)

    def _get_scope_variables(self, scope):
        """ Gets the scope from argument or callstack
        Args:
            scope (dict): The global scope for the base module
        """

        if scope is None:
            self.scope = inspect.stack(0)[2][0].f_globals
        else:
            self.scope = scope

        self.name = self.scope.get('__name__')
        self.package = self.scope.get('__package__')
        self.file = self.scope.get('__file__')
        self.location = os.path.split(str(pathlib.Path(os.path.abspath(self.file))))[0]
        self.path = self.scope.get('__path__')[0]

    def _get_source_location(self, source):
        """ Gets the source location
        Note:
            If the source is not passed as argument get it from the global scope
        Args:
            source (str): The source directory to iterate through for modules
        """

        if source is None:
            self.source = self.scope.get('__source__')
        else:
            self.source = source

    def _get_expose_classes(self, expose):
        """ Gets from the scope or the parameters the names of classes to expose
        Args:
            expose (list): List of class names to expose to this module
        """

        if expose is None:
            self.expose = self.scope.get('__expose__')
            if self.expose is None:
                self.expose = []
        else:
            self.expose = expose

    def walk_directory_structure(self, directory):
        """ Walks through the directories finding modules and classes
        Args:
            directory (str): The directory to begin inspection from. Will walk recursively
        """
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)

            # Only import py files not this file
            if os.path.isfile(file_path) and file_name.endswith(".py") and not file_name.startswith('_'):
                # Get the relative path to the module from the package root
                # Example => IntelliaLIMS\lib\IntelliaLIMSModels\__init__.py -> IntelliaLIMS\lib\IntelliaLIMSModels
                module_root_path = os.path.split(self.file)[0]
                # Splits the file path with the module root
                # Example => C:\Users\andrew.carretta\Development\IntelliaLIMS\lib\IntelliaLIMSModels\src\access.py -> \src\access.py
                file_path = file_path.split(module_root_path)[1]
                # Sanitizes the forward and back slashes into dot notation
                # Example => \src\access.py -> .src.access.py
                file_path = file_path.replace('/', '.').replace('\\', '.')
                # Strips the extension
                # Example => .src.access.py -> .src.access
                module_path = os.path.splitext(file_path)[0]
                # Import the module
                module = importlib.import_module(module_path, self.package)
                # Iterate over the members of this module
                for class_name, class_obj in inspect.getmembers(module):
                    # If the member is a class
                    if inspect.isclass(class_obj):
                        # And that class is part of this package
                        if self.package in class_obj.__module__ or class_name in self.expose:
                            # Append to __all__
                            self.scope[class_name] = class_obj
                            if class_name not in self.scope.get('__all__'):
                                self.scope['__all__'].append(class_name)
                                self.walk_class_and_functions(class_name, class_obj)
                    elif inspect.ismodule(class_obj):
                        # We dont want submodules to be loaded like this
                        pass
                    elif inspect.isfunction(class_obj):
                        # We dont want functions exposed at module level to be loaded like this
                        pass
                    else:
                        if not class_name.startswith('_'):
                            # The object is not a class probally a member variable
                            # Append to __all__
                            self.scope[class_name] = class_obj
                            if class_name not in self.scope.get('__all__'):
                                self.scope['__all__'].append(class_name)

            elif os.path.isdir(file_path) and not file_name.startswith('_'):
                self.walk_directory_structure(file_path)

    def walk_class_and_functions(self, class_name, class_obj):
        """Walks through the class structure and appends the class and function names to a dictionary
        Args:
            class_name (str): The name of the class
            class_obj (class): The class object
        """
        self.class_functions[class_name] = {}
        if __debug__:
            Log.debug(Color.MAGENTA, 'Class', class_name, Color.GREEN)

        for func_name, func_obj in inspect.getmembers(class_obj):
            if not func_name.startswith('_'):
                if callable(func_obj):
                    if hasattr(func_obj,'__module__') and func_obj.__module__:
                        if hasattr(func_obj,'__name__') and func_obj.__name__:
                            func_path = func_obj.__module__ + '.' + func_obj.__name__
                            self.class_functions[class_name][func_name] = func_obj
                            if class_obj.__module__ in func_path:
                                if __debug__:
                                    Log.debug(Color.LIGHTMAGENTA, 'Function', ' > {}'.format(func_name), Color.LIGHTCYAN)
