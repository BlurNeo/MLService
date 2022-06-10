import json
from http.server import BaseHTTPRequestHandler
from ml_db import MLDataBase

class MLHandler(BaseHTTPRequestHandler):
    def __init__(self, predict_queue, train_queue, db_path, *args, **kwargs):
        self._predict_queue = predict_queue
        self._train_queue = train_queue
        self._db_path = db_path
        super().__init__(*args, **kwargs)

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.send_header("Accept", "text/plain")
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            try:
                print('Handling /predict request')
                self._set_headers()
                datas = self.rfile.read(int(self.headers['Content-Length']))
                print(datas)
                predict_req = json.loads(datas)
                # TODO: what to do if the queue is full?
                self._predict_queue.put(predict_req)
            except Exception as e:
                print("Handle get error: ", e.args)
        elif self.path == '/train':
            try:
                print('Handling /train request')
                self._set_headers()
                datas = self.rfile.read(int(self.headers['Content-Length']))
                train_images_dict = json.loads(datas)
                # TODO: what to do if the queue is full?
                self._train_queue.put(train_images_dict)
            except Exception as e:
                print("Handle get error: ", e.args)

    def do_GET(self):
        if self.path == '/metadata':
            try:
                print('Handling /metadata request')
                self._set_headers()
                metadata = None
                with MLDataBase(self._db_path) as db:
                    metadata = db.query_metadata()
                self.wfile.write(json.dumps(metadata).encode('utf-8'))
            except Exception as e:
                print("Handle get error: ", e.args)
        elif self.path == '/history':
            try:
                print('Handling /history request')
                self._set_headers()
                history = None
                with MLDataBase(self._db_path) as db:
                    history = db.query_history()
                self.wfile.write(json.dumps(history).encode('utf-8'))
            except Exception as e:
                print("Handle get error: ", e.args)
