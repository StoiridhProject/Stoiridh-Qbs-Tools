# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2016 William McKIE                                                    ##
##                                                                                                ##
##            This program is free software: you can redistribute it and/or modify                ##
##            it under the terms of the GNU General Public License as published by                ##
##            the Free Software Foundation, either version 3 of the License, or                   ##
##            (at your option) any later version.                                                 ##
##                                                                                                ##
##            This program is distributed in the hope that it will be useful,                     ##
##            but WITHOUT ANY WARRANTY; without even the implied warranty of                      ##
##            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       ##
##            GNU General Public License for more details.                                        ##
##                                                                                                ##
##            You should have received a copy of the GNU General Public License                   ##
##            along with this program.  If not, see <http://www.gnu.org/licenses/>.               ##
##                                                                                                ##
####################################################################################################
"""
The :py:mod:`stoiridhtools.logging` module is a proxy for the standard module, :py:mod:`logging`. It
appends a coloured output support for the different severity levels known by the :py:mod:`logging`
standard module and use two handlers, a file handler and a stream handler.

In order to use this module, a call to the :py:func:`init` function is necessary to initialise the
logging API and allows you to create the log file in another location. As for the :py:func:`deinit`
function will close the handlers.

The file handler has the responsibility to catch all events during application execution and write
them into a log file which is setting up at the initialisation of this module using the
:py:func:`init` function.

The stream handler shall only print out the events from a certain severity level. You can change
this by using the :py:func:`set_level` function or if you want to know the current severity level
for the current context, use the :py:func:`get_level` function.

:py:mod:`stoiridhtools.logging` supports the standard severity levels setting up by
:py:mod:`logging`, :py:func:`critical`, :py:func:`debug`, :py:func:`error`, :py:func:`info`, and
:py:func:`warning`. In order to track simple events, a new *(severity)* level has been added into
this module, :py:func:`message`. This level shall print out an event without displaying its level
in the stream handler but also write this event into the file handler.

Below, a resume of the different severity levels available from the standard API:

+----------------+---------------+
| Severity level | Numeric value |
+================+===============+
| ``CRITICAL``   | 50            |
+----------------+---------------+
| ``ERROR``      | 40            |
+----------------+---------------+
| ``WARNING``    | 30            |
+----------------+---------------+
| ``INFO``       | 20            |
+----------------+---------------+
| ``DEBUG``      | 10            |
+----------------+---------------+
| ``NOTSET``     | 0             |
+----------------+---------------+

.. seealso:: :py:ref:`levels` (logging)

The :py:func:`get_logger` function returns an instance of the :py:class:`Logger` proxy class.
Loggers are identifying by name and allow to generate log messages under the form of categories
that facilitates the tracing of the events while the application is running.

Using the different logging functions such as :py:func:`info` shall refer to the default logger,
``root``.

A good practice to use for instanciating your loggers in order to trace the events of your module
is to initialise like below::

   LOG = stoiridhtools.logging.get_logger(__name__)

.. seealso:: :py:ref:`logger` (logging)
"""
import locale
import logging
import re
import sys
from datetime import date
from pathlib import Path

import colorama

__all__ = [
    'critical', 'CRITICAL', 'debug', 'DEBUG', 'deinit', 'error', 'ERROR', 'get_level',
    'get_logger', 'info', 'INFO', 'init', 'Logger', 'message', 'NOTSET', 'set_level', 'warning',
    'WARNING'
]


# bind the severity levels supported by the logging API
CRITICAL = logging.CRITICAL
DEBUG = logging.DEBUG
ERROR = logging.ERROR
INFO = logging.INFO
NOTSET = logging.NOTSET
WARNING = logging.WARNING

# register severity level 'MESSAGE' to logging
_MESSAGE = logging.CRITICAL + 100
logging.addLevelName(int(_MESSAGE), 'MESSAGE')


_SEVERITY_LEVELS = {
    CRITICAL: colorama.Style.BRIGHT + colorama.Fore.RED + 'CRITICAL',
    DEBUG: colorama.Style.BRIGHT + colorama.Fore.GREEN + 'DEBUG',
    ERROR: colorama.Style.BRIGHT + colorama.Fore.RED + 'ERROR',
    INFO: colorama.Style.BRIGHT + colorama.Fore.BLUE + 'INFO',
    _MESSAGE: '',
    WARNING: colorama.Style.BRIGHT + colorama.Fore.YELLOW + 'WARNING'
}


class _FileFormatter(logging.Formatter):
    """File formatter internally used by the stoiridhtools.logging API."""
    FORMAT = '[%(asctime)s | %(name)s | %(levelname)s] %(message)s'
    DATE_FORMAT = locale.nl_langinfo(locale.D_T_FMT)

    # ANSI escape code: https://en.wikipedia.org/wiki/ANSI_escape_code
    ANSI_CSI_RE = re.compile(r'\033\[\d+(?:;\d)*m')

    def __init__(self):
        super().__init__(self.FORMAT, self.DATE_FORMAT)

    def format(self, record):
        msg = super().format(record)
        return self.ANSI_CSI_RE.sub('', msg)


class _FileHandler(logging.FileHandler):
    """File handler internally used by the stoiridhtools.logging API."""
    def __init__(self, filename):
        super().__init__(str(filename))
        self.setFormatter(_FileFormatter())
        self.setLevel(NOTSET)


class _StreamFormatter(logging.Formatter):
    """Stream formatter internally used by the stoiridhtools.logging API."""
    FORMAT = '%(message)s'

    def __init__(self):
        super().__init__(self.FORMAT)

    def format(self, record):
        msg = super().format(record)
        level = ''

        if hasattr(record, 'levelno'):
            level = _SEVERITY_LEVELS.get(getattr(record, 'levelno'))

            if level is not None and len(level) > 0:
                level = level + colorama.Style.RESET_ALL + ' '
            else:
                level = ''

        return level + msg


class _LoggingHandlers:
    """The _LoggingHandlers class manages the file and the stream handlers."""
    def __init__(self, file=None, stream=None):
        self._file = file
        self._stream = stream

        if self._stream is not None:
            self._stream.setLevel(WARNING)
            self._stream.setFormatter(_StreamFormatter())

    @property
    def file(self):
        """Hold the file handler."""
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def stream(self):
        """Hold the stream handler."""
        return self._stream

    @stream.setter
    def stream(self, value):
        self._stream = value

    def attach_file_to_logger(self, logger):
        """Attach the file handler to `logger`."""
        if self.file is not None:
            logger.add_handler(self.file)

    def attach_stream_to_logger(self, logger):
        """Attach the stream handler to `logger`."""
        if self.stream is not None:
            logger.add_handler(self.stream)

    def attach(self, logger):
        """Attach the file and the stream handlers to `logger`."""
        self.attach_file_to_logger(logger)
        self.attach_stream_to_logger(logger)

    def detach_file_to_logger(self, logger):
        """Detach the file handler from `logger`."""
        if self.file is not None:
            logger.remove_handler(self.file)

    def detach_stream_to_logger(self, logger):
        """Detach the stream handler from `logger`."""
        if self.stream is not None:
            logger.remove_handler(self.stream)

    def detach(self, logger):
        """Detach the file and the stream handlers from `logger`."""
        self.detach_file_to_logger(logger)
        self.detach_stream_to_logger(logger)

    def close(self):
        """Close the file and stream handlers."""
        if self.file is not None:
            self.file.close()
            self.file = None

        if self.stream is not None:
            self.stream.close()
            self.stream = None


class Logger:
    """The :py:class:`Logger` class allows to log event messages under a category ``name``.
    By default, the severity level is :py:data:`NOTSET`.

    Note also that this class should not be instancied directly. Prefer to use the
    :py:func:`get_logger` function which is more appropriate.

    .. seealso::

       :py:ref:`logger` (logging)
    """
    def __init__(self, name=None, level=NOTSET, **kwargs):
        self._logger = logging.getLogger(name)
        self._root_proxy = kwargs.pop('root_proxy', None)
        self.level = level

        if self._root_proxy is not None and name not in self._root_proxy.loggers:
            self._root_proxy.loggers[name] = self

    @property
    def name(self):
        """Return the logger's name."""
        return self._logger.name

    @property
    def level(self):
        """Hold the logger's level."""
        if self._root_proxy is not None:
            level = NOTSET
            if hasattr(self._root_proxy.stream, 'level'):
                level = getattr(self._root_proxy.stream, 'level')
            return level
        else:
            return self._logger.getEffectiveLevel()

    @level.setter
    def level(self, level):
        if self._root_proxy is not None:
            self._root_proxy.stream.setLevel(level)
        else:
            self._logger.setLevel(level)

    def add_handler(self, handler):
        """Add a handler to this logger."""
        self._logger.addHandler(handler)

    def remove_handler(self, handler):
        """Remove a handler from this logger."""
        self._logger.removeHandler(handler)

    def critical(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `CRITICAL`."""
        self._logger.critical(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `DEBUG`."""
        self._logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `ERROR`."""
        self._logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `INFO`."""
        self._logger.info(msg, *args, **kwargs)

    def message(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `MESSAGE`."""
        self._logger.log(_MESSAGE, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log and print out a message with severity level `WARNING`."""
        self._logger.warning(msg, *args, **kwargs)

    def __repr__(self):
        return '<%s name=%s level=%s>' % (self.__class__.__name__, self.name, self.level)


class _LoggingProxy:
    DEFAULT_FILENAME = 'stoiridhtools-%(date)s.log' % {'date': date.today()}

    def __init__(self):
        self._root_logger = Logger(level=NOTSET)
        self._handlers = _LoggingHandlers(stream=logging.StreamHandler())
        self._handlers.attach(self._root_logger)
        self._loggers = dict()

    @property
    def root(self):
        """Hold the name of the context. All logging messages according to severity level will be
        printed out on the console using this name as identifier for the file handler.
        """
        return self._root_logger

    @property
    def stream(self):
        """Hold the stream used by the stream handler."""
        return self._handlers.stream

    @stream.setter
    def stream(self, value):
        if value is None:
            value = sys.stderr

        self._handlers.stream = value

    @property
    def loggers(self):
        """Return the loggers bound to the proxy."""
        return self._loggers

    def init(self, **kwargs):
        """Initialise the logging proxy. Currently, this function only supports the following
        arguments:

        +-----------+------------------------------------------------------------------------------+
        | Arguments | Description                                                                  |
        +===========+==============================================================================+
        | filename  | Relative or absolute path to the filename.                                   |
        +-----------+------------------------------------------------------------------------------+
        | path      | Relative or absolute path where the logging file will be created.            |
        +-----------+------------------------------------------------------------------------------+
        | stream    | Stream used to printed out the logging messages. If no `stream` is set, then |
        |           | the :py:data:`sys.stderr` stream will be used.                               |
        +-----------+------------------------------------------------------------------------- ----+

        .. note::

           *path* must point to a valid location in the file system and must have the right
           permissions in order to be able to create and write the log messages into the logging
           file.

        :raise TypeError: if both *path* and *filename* are not either a :py:class:`str` or a
                          :py:class:`pathlib.Path` object.
        :raise ValueError: if both `filename` and `path` are specified.
        """
        stream = kwargs.pop('stream', sys.stderr)

        if self.stream is None:
            self.stream = logging.StreamHandler(stream)
        else:
            self.stream.stream = stream

        self._handlers.attach_stream_to_logger(self._root_logger)

        if 'filename' in kwargs and 'path' in kwargs:
            raise ValueError('both argument (filename) and argument (path) should not be specified '
                             'together')

        try:
            self._init_file_handler(**kwargs)
        except TypeError:
            raise

    def close(self):
        """Close the handlers used by the logging proxy."""
        self._handlers.detach(self._root_logger)
        self._handlers.close()

    def _init_file_handler(self, **kwargs):
        """Initialise the file handler of the logging proxy with the given `kwargs`. Currently, this
        method only supports the following arguments:

        +-----------+------------------------------------------------------------------------------+
        | Arguments | Description                                                                  |
        +===========+==============================================================================+
        | filename  | Relative or absolute path to the filename.                                   |
        +-----------+------------------------------------------------------------------------------+
        | path      | Relative or absolute path where the logging file will be created.            |
        +-----------+------------------------------------------------------------------------------+

        .. note::

           *path* must point to a valid location in the file system and must have the right
           permissions in order to be able to create and write the log messages into the logging
           file.

        :raise TypeError: if both *path* and *filename* are not either a :py:class:`str` or a
                          :py:class:`pathlib.Path` object.
        """
        # TODO remove this import-statement when the issue#43 will be done
        import stoiridhtools

        filename = kwargs.pop('filename', None)
        path = kwargs.pop('path', None)

        if filename is not None:
            if isinstance(filename, str):
                filename = Path(filename)
            elif not isinstance(filename, Path):
                raise TypeError('argument (filename) should be either a str or a pathlib.Path '
                                'object, not %r' % type(filename))

            if not filename.parent.exists():
                # TODO modify the line below when we can access to default paths
                filename = stoiridhtools.get_default_path().joinpath('logs',
                                                                     self.DEFAULT_FILENAME)

            self._reset_file_handler(filename)
        elif path is not None:
            if isinstance(path, str):
                path = Path(path)
            elif not isinstance(path, Path):
                raise TypeError('argument (path) should be either a str or a pathlib.Path '
                                'object, not %r' % type(path))

            try:
                path = path.resolve()
            except (FileNotFoundError, RuntimeError):
                # TODO modify the line below when we can access to default paths
                path = stoiridhtools.get_default_path().joinpath('logs')

            if path.is_dir():
                filename = path.joinpath(self.DEFAULT_FILENAME)
                self._reset_file_handler(filename)

    def _reset_file_handler(self, filename=None):
        """Reset the file handler with ``filename``."""
        file_handler = self._handlers.file

        if file_handler is not None:
            self._handlers.detach_file_to_logger(self._root_logger)
            file_handler.close()

        if filename is not None:
            file_handler = _FileHandler(filename)
            self._handlers.file = file_handler
            self._handlers.attach_file_to_logger(self._root_logger)
        else:
            self._handlers.file = None


_PROXY = _LoggingProxy()


def init(**kwargs):
    """Initialise `stoiridhtools.logging`. Currently, this function only supports the following
    arguments:

    +-----------+----------------------------------------------------------------------------------+
    | Arguments | Description                                                                      |
    +===========+==================================================================================+
    | filename  | Relative or absolute path to the filename.                                       |
    +-----------+----------------------------------------------------------------------------------+
    | path      | Relative or absolute path where the logging file will be created.                |
    +-----------+----------------------------------------------------------------------------------+
    | stream    | Stream used to printed out the logging messages. If no `stream` is set, then the |
    |           | :py:data:`sys.stderr` stream will be used.                                       |
    +-----------+----------------------------------------------------------------------------------+

    .. note::

       *path* must point to a valid location in the file system and must have the right permissions
       in order to be able to create and write the log messages into the logging file.

    :raise TypeError: if both *path* and *filename* are not either a :py:class:`str` or a
                      :py:class:`pathlib.Path` object.
    :raise ValueError: if both `filename` and `path` are specified.
    """
    try:
        _PROXY.init(**kwargs)
    except (TypeError, ValueError):
        raise


def deinit():
    """Deinitialise `stoiridhtools.logging`."""
    _PROXY.close()


def get_logger(name=None):
    """Return a logger with the specified `name` or, if name is :py:data:`None`, return a logger
    which is the root logger of the hierarchy.

    .. seealso:: :py:func:`logging.getLogger`
    """
    return _PROXY.loggers.get(name, Logger(name, root_proxy=_PROXY))


def get_level():
    """Get the severity level `level` of the ``root`` logger."""
    return _PROXY.root.level


def set_level(level):
    """Set the severity level `level` for the ``root`` logger."""
    _PROXY.root.level = level


def critical(msg, *args, **kwargs):
    """Log and print out a message with severity level `CRITICAL`."""
    _PROXY.root.critical(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """Log and print out a message with severity level `DEBUG`."""
    _PROXY.root.debug(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """Log and print out a message with severity level `ERROR`."""
    _PROXY.root.error(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """Log and print out a message with severity level `INFO`."""
    _PROXY.root.info(msg, *args, **kwargs)


def message(msg, *args, **kwargs):
    """Log and print out a message with severity level `MESSAGE`.

    .. note::

       The severity level is not printed out on the stream handler.
    """
    _PROXY.root.message(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """Log and print out a message with severity level `WARNING`."""
    _PROXY.root.warning(msg, *args, **kwargs)
