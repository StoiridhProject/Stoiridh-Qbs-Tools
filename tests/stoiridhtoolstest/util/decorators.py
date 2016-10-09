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
import asyncio
import functools

import stoiridhtools.logging

stoiridhtools.logging.set_level(stoiridhtools.logging.WARNING)


class asyncio_loop:
    """Class decorator to get or start - a new one - the asynchronous event loop and finally close
    it.

    .. Examples::
        import unittest

        from util.decorators import asyncio_loop

        @asyncio_loop
        class TestClass(unittest.TestCase):
            def test_async_method(self):
                TestClass.run_until_complete(...)
    """
    def __init__(self, cls):
        self.wrapped = cls

        cls.loop = asyncio.get_event_loop()

        # sanity check
        if cls.loop.is_closed():
            cls.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls.loop)

        functools.update_wrapper(self, cls)

    def __del__(self):
        self.wrapped.loop.close()

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.wrapped, name)
