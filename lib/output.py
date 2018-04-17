""" Functions for building console applications """

import logging
constructure_logger = logging.getLogger('constructure')

from enum import Enum

class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39
    LIGHTBLACK = 90
    LIGHTRED = 91
    LIGHTGREEN = 92
    LIGHTYELLOW = 93
    LIGHTBLUE = 94
    LIGHTMAGENTA = 95
    LIGHTCYAN = 96
    LIGHTWHITE = 97

class Format(object):
    """ Methods for helping to make easy to use console applications """

    @staticmethod
    def message(color, title, message, justify=24, logger=constructure_logger, log_level=logging.DEBUG):
        """ """
        return Format.message_color(colora=color, title=title, colorb=Color.WHITE, message=message, justify=justify, logger=logger, log_level=log_level)

    @staticmethod
    def message_color(colora, title, colorb, message, justify=24, logger=constructure_logger, log_level=logging.DEBUG):
        """ """
        messages = [{colora:title.ljust(justify)}, {colorb:message}]
        return Format.expression(messages=messages, logger=logger, log_level=log_level)

    @staticmethod
    def message_time(color, title, message, seconds, justify=24, logger=constructure_logger, log_level=logging.DEBUG):
        """ """
        messages = [{color:title.ljust(justify)}, {Color.WHITE:message}, {Color.MAGENTA:' in '}, {Color.GREEN:str(round(seconds, 2))}, {Color.GREEN:' seconds'}]
        return Format.expression(messages=messages, logger=logger, log_level=log_level)

    @staticmethod
    def message_json(color, title, json_message, justify=24, logger=constructure_logger, log_level=logging.DEBUG):
        """ [{'Magenta':'Action Happening!'}, {'White':SOME JSON STRING}] """
        try:
            from pygments import highlight, lexers, formatters
            from colorama import Fore, Back, Style
            colored_json_message = highlight(json_message, lexers.JsonLexer(), formatters.TerminalFormatter()).strip()
            messages = [{Color.WHITE:'\n'}, {color:title.ljust(justify)}, {Color.WHITE:colored_json_message}]
        except (ImportError, AttributeError):
            messages = [{Color.WHITE:'\n'}, {color:title.ljust(justify)}, {Color.WHITE:json_message}]
        return Format.expression(messages=messages, logger=logger, log_level=log_level)

    @staticmethod
    def expression(messages, logger=constructure_logger, log_level=logging.DEBUG):
        """ Formats a dictionary of key:value == color:message to a string"""
        uncolored_string, colored_string = Format.convert_messages(messages)
        Format.handle_logger(uncolored_string=uncolored_string, colored_string=colored_string, logger=logger, log_level=log_level)
        return colored_string

    @staticmethod
    def convert_messages(messages):
        """Converts messages into their string and colored string representations
        Args:
            parameter (dict): messages in dict format [{'Magenta':'Action Happening!'}, {'White':SOME JSON STRING}]
        Returns:
            return tuple of string and colored string
        """

        string = ""
        colored_string = ""

        # Create the uncolored string representation.
        for message in messages:
            for color, text in message.items():
                string += text

        # Attempt to make the colored version and if the packages do not exist default to uncolored representation.
        try:
            from colorama import Fore, Back, Style
            for message in messages:
                for color, text in message.items():
                    converted_color = Format.convert_color(color)
                    colored_string += (converted_color + str(text))
            colored_string += Style.RESET_ALL
        except (ImportError, AttributeError):
            # The colorization packages are not installed so lets just default to the non colored string
            colored_string = string

        # Return a tuple of uncolored and colored string
        return (string, colored_string)

    @staticmethod
    def convert_color(color):
        """ Converts from string or Color to colorama Fore style
        Args:
            color (str, Color): String or Color object
        Returns:
            return Ansi color Fore from colorama
        """

        from colorama import Fore, Back, Style

        # If Color get the name we want to work like its a string
        if isinstance(color, Color):
            color = color.name

        # Light colors have an EX at the end
        if color.upper().startswith('LIGHT'):
            color = color + '_EX'

        # Get the color matching the name
        return getattr(Fore, color.upper())

    @staticmethod
    def handle_logger(uncolored_string, colored_string, logger=constructure_logger, log_level=logging.DEBUG):
        # Log colorization for the supported log level
        # This is an override of the basic log handler
        # This is how we get colors in the console but not in the log file
        console_handler = next((handler for handler in logger.handlers if handler.name == 'colored_console'), None)
        if console_handler:
            if log_level >= console_handler.level:
                print(colored_string)

        # Log the string without colorization
        logger.log(log_level, uncolored_string)


class Log(object):
    """ Methods for helping to make colored log entries """

    @staticmethod
    def debug(title_color, title, message, message_color=Color.WHITE, seconds=None):
        if seconds:
            message = Format.message_time(color=title_color, title=title, message=message, seconds=seconds)
        else:
            message = Format.message_color(colora=title_color, title=title, colorb=message_color, message=message)
