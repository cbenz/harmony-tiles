# -*- coding: utf-8 -*-


"""Helpers for URLs"""


import os

import tilelite
from webob.dec import wsgify
import webob.exc


def make_router(conf):
    @wsgify
    def router(req):
        split_path_info = req.path_info.split('/', 2)
        if len(split_path_info) != 3:
            return webob.exc.status_map[404]()
        project_slug = split_path_info[1]
        project_file_path = os.path.join(conf['projects_base_dir'], project_slug, u'carto_project', u'project.xml')
        if not os.path.isfile(project_file_path):
            return webob.exc.status_map[404]()
        app = tilelite.Server(mapfile=str(project_file_path))
        req.script_name += '/' + project_slug
        req.path_info = '/' + split_path_info[2]
        return req.get_response(app)
    return router
