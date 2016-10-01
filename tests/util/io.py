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
import io


class OutputStreamWrapper:
    """The :py:class:`OutputStreamWrapper` class is a wrapper that intercepts calls from the
    :py:data:`sys.stdout` and the :py:data:`sys.stderr` streams.

    When a message is written from either the output stream or the error stream or both, the
    :py:meth:`get_lines` method will return the lastest lines written from these streams.
    """
    def __init__(self, out_stream=io.StringIO(), err_stream=io.StringIO()):
        self.stdout = out_stream
        self.stderr = err_stream

    def clear(self):
        if self.stdout is not None:
            self.stdout.seek(0)
            self.stdout.truncate()

        if self.stderr is not None:
            self.stderr.seek(0)
            self.stderr.truncate()

    def get_lines(self, stream=None):
        """Return the latest lines written from the :py:data:`sys.stdout` stream and/or the
        :py:data:`sys.stderr` stream. If `stream` is specified, then the method will return the
        latest lines from this stream.

        .. note:

           If messages are written in both before a call to this one, then the method will
           concatenate the lines from the :py:data:`sys.stdout` and the :py:data:`sys.stderr`
           functions.
        """
        if stream is not None:
            message = self._get_lines(stream)
        else:
            message = self._get_lines(self.stdout)
            error_message = self._get_lines(self.stderr)

            if message is not None:
                if error_message is not None:
                    message = message + error_message
                else:
                    message = message
            elif error_message is not None:
                message = error_message

        return message and message[:-1] or None

    def _get_lines(self, stream):
        output = stream.getvalue()
        stream.seek(0)
        stream.truncate()
        return output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            pass
        else:
            return False
