#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2020

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.exceptions import osexception
from libopensesame import debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.keyboard
from libopensesame.py3compat import *
from libopensesame.item import item
from libopensesame.generic_response import generic_response
import threading


VERSION = u'2020.11-1'

class radboudbox_get_buttons_start(item, generic_response):

    """
    Class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox: starts button registration in the background.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'
        self.poll_time = 1


    def reset(self):

        """
        desc:
            Reset item and experimental variables.
        """

        self.var.timeout = u'infinite'
        self.var.flush = u'yes'
        #self.var.lights = u''
        #self.var.require_state_change = u'no'
        #self.process_feedback = True


    def init_var(self):

        """Set en check variables."""


        if hasattr(self.experiment, "radboudbox_dummy_mode"):
            self.dummy_mode = self.experiment.radboudbox_dummy_mode
            self.verbose = self.experiment.radboudbox_verbose
        else:
            raise osexception(
                    u'You should have one instance of `radboudbox_init` at the start of your experiment')

        self.allowed_responses = self.var.allowed_responses
        self.timeout = self.var.timeout
        if self.var.flush == u'no':
            self.flush = False
        else:
            self.flush = True

        self.experiment.var.radboudbox_get_buttons_start_allowed_responses = self.var.allowed_responses
        self.experiment.var.radboudbox_get_buttons_start_timeout = self.var.timeout

        self.experiment.radboudbox_get_buttons_start = 1


    def prepare(self):

        """
        desc:
            Prepare the item.
        """

        item.prepare(self)
        self.prepare_timeout()

        self.init_var()

        # Prepare the allowed responses
        self._allowed_responses = None
        if u'allowed_responses' in self.var:
            self._allowed_responses = []
            for r in safe_decode(self.allowed_responses).split(u';'):
                if r.strip() != u'':
                    self._allowed_responses.append(r)
            if not self._allowed_responses:
                self._allowed_responses = None
        self.show_message(u"allowed responses set to %s" % self._allowed_responses)

        # Prepare keyboard for dummy-mode and flushing
        self._keyboard = openexp.keyboard.keyboard(self.experiment)
        if self.dummy_mode == u'yes':
            self._resp_func = self._keyboard.get_key
        else:
            if self.timeout == u'infinite' or self.timeout == None:
                self._timeout = float("inf")
            else:
                self._timeout = float(self.timeout) / 1000

            # Prepare auto response
            if self.experiment.auto_response:
                self._resp_func = self.auto_responder
            else:
                self._resp_func = self.experiment.radboudbox.waitButtons

    def run(self):

        """
        desc:
            Runs the item.
        """

        self.set_item_onset()

        if not hasattr(self.experiment, "radboudbox_get_buttons_wait"):
            raise osexception(
                    u'Radboudbox Get Buttons Wait item is missing')

        self._keyboard.flush()
        self.set_sri(reset=True)

        if self.dummy_mode == 'yes':
            # In dummy mode, we simply take the numeric keys from the keyboard
            if self._allowed_responses is None:
                self._allowed_responses = list(range(0,10))
            resp, self.experiment.end_response_interval = self._resp_func(
                keylist=self._allowed_responses, timeout=self._timeout)
            self.set_response_time()
            
            self.show_message("Detected press on button: '%s'" % resp)
            self.experiment.var.response = resp
            generic_response.response_bookkeeping(self)
        else:
            # Get the response
            try:
                #self.experiment.radboudbox.clearEvents()
                self.stop = 1

                self.show_message(u'Starting Collecting buttons')
                while self.experiment.radboudbox_get_buttons_locked:
                    self.clock.sleep(self.poll_time)

                self.experiment.radboudbox_get_buttons_locked = 1
                self.experiment.radboudbox_get_buttons_thread = threading.Thread(target=self.start_buttons)
                self.experiment.radboudbox_get_buttons_thread.start()


            except Exception as e:
                raise osexception(
                    "An error occured in radboudbox '%s': %s." % (self.name, e))

            while self.stop:
                self.clock.sleep(self.poll_time)


    def start_buttons(self):

        self.experiment.radboudbox_get_buttons_thread_running = 1
        self.set_item_onset()
        self.stop = 0

        resp = self._resp_func(maxWait=self._timeout, buttonList=self._allowed_responses, flush=self.flush)
        self.experiment.end_response_interval   = self.clock.time()
        self.set_response_time()

        if not resp:
            resp = u'NA'
        elif isinstance(resp, list):
            resp = resp[0]

        self.show_message("Detected press on button: '%s'" % resp)
        #self.set_response(resp, detect_time, None)
        self.experiment.var.response = resp
        generic_response.response_bookkeeping(self)
        self.experiment.radboudbox_get_buttons_locked = 0

    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


    def var_info(self):

        """
        returns:
            A list of (name, description) tuples with variable descriptions.
        """

        return item.var_info(self) + \
            generic_response.var_info(self)


    def set_response_time(self, time=None):

        """
        desc:
            Set a timestamp for the onset time of the item's execution.

        keywords:
            time:    A timestamp or None to use the current time.

        returns:
            desc:    A timestamp.
        """

        if time is None:
            time = self.clock.time()
        self.experiment.var.set(u'time_response_%s' % self.name, time)
        return time


class qtradboudbox_get_buttons_start(radboudbox_get_buttons_start, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        radboudbox_get_buttons_start.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
