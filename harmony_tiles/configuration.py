# -*- coding: utf-8 -*-


"""Paste INI configuration"""


import logging
import os

from biryani1 import strings
from biryani1.baseconv import (check, default, function, guess_bool, not_none, pipe, struct)


def load_configuration(global_conf, app_conf):
    """Build the application configuration dict."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {}
    conf.update(strings.deep_decode(global_conf))
    conf.update(strings.deep_decode(app_conf))
    conf.update(check(struct(
        {
            'app_conf': default(app_conf),
            'app_dir': default(app_dir),
            'app_name': default('Harmony Tiles'),
            'debug': pipe(guess_bool, default(False)),
            'global_conf': default(global_conf),
            'log_level': pipe(
                default('WARNING'),
                function(lambda log_level: getattr(logging, log_level.upper())),
                ),
            'package_name': default('harmony-tiles'),
            'projects_base_dir': pipe(
                function(lambda value: os.path.abspath(value)),
                not_none,
                ),
        },
        default='drop',
        drop_none_values=False,
    ))(conf))
    return conf
