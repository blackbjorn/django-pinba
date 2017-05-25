# -*- coding: utf-8 -*-

import traceback

from pinba.defaults import (
    PINBA_SERVER, PINBA_PORT, PINBA_ENABLED, PINBA_DISABLE_ADMIN
)
from pinba.monitor import Monitor

class PinbaMiddleware(object):
    def __init__(self, get_response=None):
        super(PinbaMiddleware, self).__init__(get_response)
        self.monitor = Monitor((PINBA_SERVER, PINBA_PORT))

    def __call__(self, request):

        try:
            if self.report_is_enabled(request):
                self.monitor.start(request)
        except Exception as err:
            print(err, traceback.format_exc())

        response = self.get_response(request)

        try:
            if self.report_is_enabled(request):
                return self.monitor.stop(response)
        except Exception as err:
            print(err, traceback.format_exc())

        return response

    @staticmethod
    def report_is_enabled(request):
        if not PINBA_ENABLED:
            return False

        if PINBA_DISABLE_ADMIN is True:
            if hasattr(request, 'user') and hasattr(request.user, 'is_staff'):
                if request.user.is_staff:
                    return False
        return True
