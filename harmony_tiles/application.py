# -*- coding: utf-8 -*-


"""Middleware initialization"""


import logging
import sys

from weberror.errormiddleware import ErrorMiddleware

from . import configuration, router


def make_app(global_conf, **app_conf):
    """Create a WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    conf = configuration.load_configuration(global_conf, app_conf)
    logging.basicConfig(level=conf['log_level'], stream=sys.stdout)
    app = router.make_router(conf)
    if not conf['debug']:
        app = ErrorMiddleware(
            app,
            error_email=conf['email_to'],
            error_log=conf.get('error_log', None),
            error_message=conf.get('error_message', 'An internal server error occurred'),
            error_subject_prefix=conf.get('error_subject_prefix', 'Web application error: '),
            from_address=conf['from_address'],
            smtp_server=conf.get('smtp_server', 'localhost'),
        )
    return app
