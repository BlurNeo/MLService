# Copyright (c) victor su. All rights reserved.
from http.server import HTTPServer
from functools import partial
from ml_handler import MLWebHandler
import os

class MLWebServer(object):
    """
    Serve the ml web request through http
    """
    def __init__(self, host, web_host, work_dir):
        """
        Set up the http handler, data base
        """
        self._host = host
        self._web_host = web_host
        self._work_dir = work_dir
        self._db_path = self._work_dir + 'db/ml.db'
        MLWebHandlerPartial = partial(MLWebHandler, self._db_path)
        self._httpd = HTTPServer(self._web_host, MLWebHandlerPartial)

    def run(self):
        """
        Run the web service
        """
        print('Starting ML Web Service...')
        self._httpd.serve_forever()

if __name__ == '__main__':
    work_dir = '/Users/ssc/Desktop/workspace/git_repos/MLService/'
    web_host = ('localhost', 8080)
    ml_webserver = MLWebServer(web_host, web_host, work_dir)
    ml_webserver.run()