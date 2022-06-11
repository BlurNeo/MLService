# Copyright (c) victor su. All rights reserved.
import queue
import threading
from http.server import HTTPServer
from functools import partial
import sys
sys.path.append("ml")
from ml_db import MLDataBase
from ml_worker import MLWorker
from ml_handler import MLHandler
import os

class MLServer(object):
    """
    Serve the ml request through http
    """
    def __init__(self, host, work_dir):
        """
        Set up the http handler, data base and ml worker
        """
        self._host = host
        self._work_dir = work_dir
        self._db_path = self._work_dir + 'db/ml.db'
        self._predict_queue = queue.Queue(maxsize=20)
        self._train_queue = queue.Queue(maxsize=20)
        MLHandlerPartial = partial(MLHandler, self._predict_queue, self._train_queue, self._db_path)
        self._httpd = HTTPServer(self._host, MLHandlerPartial)
        # delete the database file if restarted
        if os.path.exists(self._db_path):
            os.system('rm ' + self._db_path)
        # add the pre-trained model into database
        with MLDataBase(self._db_path) as db:
            db.insert_metadata('0', self._work_dir + 'models/trained_0.model')
        # start the ml workers for prediction and training
        self._ml_worker = MLWorker(self._predict_queue, self._train_queue,
            self._db_path, self._work_dir + 'models/')
        self._ml_worker.start()

    def run(self):
        """
        Run the service
        """
        print('Starting ML Service...')
        self._httpd.serve_forever()

if __name__ == '__main__':
    work_dir = '/Users/ssc/Desktop/workspace/git_repos/MLService/'
    host = ('localhost', 8010)
    mlserver = MLServer(host, work_dir)
    mlserver.run()