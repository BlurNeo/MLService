from http.server import BaseHTTPRequestHandler, HTTPServer
import json, threading, queue
from functools import partial
from dummy_train import DummyTrain as MLTrain
from dummy_predict import DummyPredict as MLPredict
from ml_db import MLDataBase

class MLHandler(BaseHTTPRequestHandler):
    def __init__(self, predict_queue, train_queue, db, *args, **kwargs):
        self._predict_queue = predict_queue
        self._train_queue = train_queue
        self._db = db
        super().__init__(*args, **kwargs)

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.send_header("Accept", "text/plain")
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            self._set_headers()
            datas = self.rfile.read(int(self.headers['Content-Length']))
            # print(self.headers)
            # print(datas)
            # print(json.loads(datas))
            # TODO: from base64 to image
            # TODO: what to do if the queue is full?
            self._predict_queue.put(1)
            print('post predict queue size: ', self._predict_queue.qsize())
            print('predict')
        elif self.path == '/train':
            self._set_headers()
            print('train')

    def do_GET(self):
        if self.path == '/metadata':
            try:
                self._set_headers()
                self.wfile.write("dummy metadata".encode("utf-8"))
                print('metadata')
            except Exception as e:
                print("Handle get error: ", e.args)
        elif self.path == '/history':
            try:
                self._set_headers()
                self.wfile.write("dummy history".encode("utf-8"))
                print('history')
            except Exception as e:
                print("Handle get error: ", e.args)

class MLServer(object):
    def __init__(self):
        self._host = ('localhost', 8010)
        self._work_dir = '/Users/ssc/Desktop/workspace/git_repos/MLService/'
        self._db_path = self._work_dir + 'db/ml.db'
        self._predict_queue = queue.Queue(maxsize=10)
        self._train_queue = queue.Queue(maxsize=10)
        MLHandlerPartial = partial(MLHandler, self._predict_queue, self._train_queue, self._db_path)
        self._httpd = HTTPServer(self._host, MLHandlerPartial)
        # TODO: add the pre-trained model into database
        with MLDataBase(self._db_path) as db:
            db.insert_metadata('0', self._work_dir + 'models/trained_0.model')

        def predict_worker(q, db_path, model_dir):
            info = None
            with MLDataBase(db_path) as db:
                info = db.query_latest_model_info()
            latest_version = info.model_version
            latest_path = info.model_path
            predictor = MLPredict(latest_path)
            while True:
                # should be blocked if queue empty
                # image = q.get()
                image_path = None
                print('predict queue size: ', q.qsize())
                with MLDataBase(db_path) as db:
                    info = db.query_latest_model_info()
                    if info.model_path != predictor.model_path():
                        predictor = MLPredict(info.model_path)
                result = predictor.run(image_path)
                with MLDataBase(db_path) as db:
                    db.insert_history(str(info.model_version), image_path, result)
        
        def train_worker(q, db_path, model_dir):
            while True:
                # TODO: should be blocked if queue empty
                # image_paths = q.get()
                image_paths = None
                info = None
                with MLDataBase(db_path) as db:
                    info = db.query_latest_model_info()
                latest_ver = info.model_version
                latest_ver = latest_ver + 1
                trainner = MLTrain(model_dir, latest_ver)
                trained_model_path = trainner.run(image_paths)
                with MLDataBase(db_path) as db:
                    db.insert_metadata(str(latest_ver), trained_model_path)
        
        # TODO: use thread pools?
        self._predict_thread = threading.Thread(
            target=predict_worker, args=(self._predict_queue, self._db_path, self._work_dir + 'models/'))
        self._train_thread = threading.Thread(
            target=train_worker, args=(self._train_queue, self._db_path, self._work_dir + 'models/'))
        
        self._predict_thread.start()
        self._train_thread.start()
    
    def run(self):
        print('Starting http...')
        self._httpd.serve_forever()

if __name__ == '__main__':
    mlserver = MLServer()
    mlserver.run()