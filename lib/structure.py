""" Module for the defining the structure of a python package """

import types
import os
import sys
import pathlib
import importlib
import inspect
import re

from .output import Color, Log

class Structure(object):
    """ A module for structuring a logical namespace system for a package. """

    scope = {} # The global scope of the calling module
    submodules = {} # Dictionary of submodules key is alias and value is relative path
    source = '' # The source directory to walk through and find submodules
    library = '' # The location to library modules will be added to sys path
    name = '' # The name of this module
    package = '' # The name of this package
    location = '' # The directory location where this module resides
    path = '' # Path to the module may differ from location
    file = '' # The fill path to the init file for this module

    def __init__(self, scope=None, source=None, library=None):
        """ Constructor for the structure module
        Note:
            This is the entrypoint to the functionality. Pass the global scope from the calling object.
        Args:
            scope (dict): The global scope for the base module
            source (str): The source directory to iterate through for modules
            library (str): The library directory this will be added to sys path
        """

        if __debug__:
            import time
            start_time = time.time()

        # Gets the scope from arguments or calling function
        self._get_scope_variables(scope)

        if __debug__:
            Log.debug(Color.CYAN, 'Constructing', self.name)

        # Get the scope and library from arguments or global
        self._get_source_location(source)
        self._get_library_location(library)

        # List all the submodules and create a dictionary of submodules
        self._list_submodules()

        # Register the main module
        self._register_ondemand_module(self.submodules)

        # Register all the submodules
        for submodule_name, submodule_path in self.submodules.items():
            self._register_pointer_module(submodule_name)

        if __debug__:
            seconds = (time.time() - start_time)
            Log.debug(Color.GREEN, 'Constructed', self.name, seconds=seconds)

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

    def _get_library_location(self, library):
        """ Gets and adds the library location to the sys path
        Note:
            If the library is not passed as argument get it from the global scope
            Library is not mandatory and does not need to be added
        Args:
            library (str): The library directory this will be added to sys path
        """

        if library is None:
            self.library = self.scope.get('__library__')
        else:
            self.library = library

        # Add the library to the sys path for discovery
        if self.library is not None:
            sys.path.append(os.path.join(self.location, self.library))

    def _register_ondemand_module(self, submodules):
        """ Register the on demand lazy load module to the sys modules dictionary
        Args:
            submodules (dict): Dictionary of the submodules key is alias and value is path
        """

        ondemand_module = OnDemandModule(self.name)
        ondemand_module.module_name = self.name
        ondemand_module.package_name = self.package
        ondemand_module.submodules = submodules
        ondemand_module.__dict__.update(self.scope)
        ondemand_module.__all__ = list(submodules.keys())

        if __debug__:
            Log.debug(Color.BLUE, 'On Demand Module', self.name)

        # Register this module as the fully qualified path from package root
        # SomeProject.lib.ThisProject
        sys.modules[self.name] = ondemand_module

        # Register this module as the non fully qualified path
        # ThisProject
        module_name = self.name.split('.')[-1:][0]
        if module_name not in sys.modules:
            if __debug__:
                Log.debug(Color.BLUE, 'On Demand Module', module_name)
            sys.modules[module_name] = ondemand_module

    def _register_pointer_module(self, submodule_name):
        """ Register the pointer module to the sys modules dictionary
        Args:
            submodule_name (str): The name of the submodule
        """
        submodule_path = '{}.{}'.format(self.name, submodule_name)

        pointer_module = PointerModule(submodule_path)
        pointer_module.__dict__.update(self.scope)
        pointer_module.module_name = self.name
        pointer_module.package_name = self.package
        pointer_module.submodule_name = submodule_name

        if __debug__:
            Log.debug(Color.BLUE, 'Pointer Module', submodule_path)

        # Register this module as the fully qualified path from package root
        sys.modules[submodule_path] = pointer_module

    def _get_module_alias(self, file_path):
        """Reads through the file and looks for __alias__
        Args:
            file_path (str): Path to the file for inspection
        Returns:
            Return str or list of alias
        """
        return self._get_module_variable(file_path, '__alias__')

    def _get_module_variable(self, file_path, variable_name):
        """Reads through the file and looks for variable name
        Args:
            file_path (str): Path to the file for inspection
            variable_name (str): Name of the variable to find the value for
        Returns:
            Return str or list of variables
        """
        regex = r"(?<=" + variable_name + r"\s=\s)\S+(?=\n)"
        with open(file_path) as init_file:
            for line in init_file:
                match = re.search(regex, line)
                if match:
                    return eval(match.group()) # eval turns the results into a string or a list

    def _get_module_aliases(self, file_path, module_name):
        """ Reads the init file and gets the module aliases from the code without instantiation.
        Args:
            file_path (str): The absolute path to the file for inspection.
            module_name (str): The name of the module. Used as a default if we could not find the alias.
        """

        alias = self._get_module_alias(file_path)
        aliases = []
        # The alias could be a string, list, or not found.
        if isinstance(alias, str):
            aliases.append(alias)
        elif isinstance(alias, list):
            aliases.extend(alias)
        else:
            aliases.append(module_name)
        return aliases

    def _get_submodule_by_name(self, name):
        """ Get the submodule by name from the submodule list.
        Args:
            name (str): The name or alias of the module looking for
        Returns:
            return the path to the submodule from the submodule dictionary
        """
        if __debug__:
            Log.debug(Color.LIGHTBLUE, 'Lookup Module', name)
        return self.submodules[name]

    def _list_submodule_recursive(self, directory):
        """ Recursively lists all of the submodules under the source folder for the current project
        Args:
            directory (str): The directory to begin listing submodules. Used recursively for walking directories.
        Returns:
            Dictionary of modules by name and path
        """
        for directory_item in os.listdir(directory):
            directory_item_path = os.path.join(directory, directory_item)
            if os.path.isdir(directory_item_path):
                self._list_submodule_recursive(directory_item_path)
            else:
                if directory_item == '__init__.py':
                    module_name = os.path.basename(directory)

                    # Does some path magic to turn absolute to relative path
                    mod_dir_dot = directory.replace('/', '.').replace('\\', '.')
                    start_src = mod_dir_dot.find(self.package) + len(self.package)
                    module_path = mod_dir_dot[start_src:]

                    # Get the aliases for the modules
                    aliases = self._get_module_aliases(directory_item_path, module_name)
                    for alias in aliases:
                        if __debug__:
                            Log.debug(Color.CYAN, 'Module Alias', '{} for {}'.format(alias, module_path))
                        self.submodules[alias] = module_path

    def _list_submodules(self):
        """ Lists all of the submodules under the source folder for the current project
        Returns:
            Dictionary of modules by name and path
        """
        if bool(self.submodules) == False:
            source_location = os.path.join(self.location, self.source)
            if os.path.exists(source_location):
                self._list_submodule_recursive(source_location)
        return self.submodules


class PointerFunction():
    """ A pointer to a function which when called instantantes a module and calls a function. """
    package_name = ''
    module_name = ''
    class_name = ''
    function_name = ''

    def call(self):
        module_path = '{}.{}'.format(self.package_name, self.module_name)
        if __debug__:
            Log.debug(Color.LIGHTBLUE, 'Returning Pointer Function', module_path)
        module = importlib.import_module(module_path, self.package_name)
        function = getattr(getattr(module, self.class_name), self.function_name)
        function()


class PointerModule(types.ModuleType):
    """ A pointer to a module which when called instantiations and replaces itself with a module """
    module_name = ''
    package_name = ''
    submodule_name = ''

    def __getattr__(self, name):
        module_class_name = '{}.{}.{}'.format(
            self.module_name, self.submodule_name, name)
        if __debug__:
            Log.debug(Color.LIGHTBLUE, 'Returning Pointer Class', module_class_name)
        main_module = sys.modules[self.module_name]
        submodule = getattr(main_module, self.submodule_name)
        submodule_class = getattr(submodule, name)
        return submodule_class


class OnDemandModule(types.ModuleType):
    """ A lazy loading on module which when accessed with instantiate and replace itself with a real module. """
    module_name = ''
    package_name = ''
    submodules = {}

    def __getattr__(self, name):
        if __debug__:
            Log.debug(Color.LIGHTYELLOW, 'Lookup Module', name)
        if name in self.submodules.keys():
            module_name = self.submodules[name]
            full_module_name = self.package_name + module_name
            if full_module_name in sys.modules:
                if __debug__:
                    Log.debug(Color.LIGHTBLUE, 'Module Found', full_module_name)
            else:
                if __debug__:
                    Log.debug(Color.BLUE, 'Importing Module', full_module_name)
            # This seems to be smart enough to grab the module if it exists
            module = importlib.import_module(module_name, self.package_name)
            return module
        else:
            raise AttributeError('No attribute %s' % name)
