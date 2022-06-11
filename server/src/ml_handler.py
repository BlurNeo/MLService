# Copyright (c) victor su. All rights reserved.
import json
from http.server import BaseHTTPRequestHandler
from ml_db import MLDataBase

class MLHandler(BaseHTTPRequestHandler):
    """
    Http handler for requests of prediction and training,
    query of metadata and history
    """
    def __init__(self, predict_queue, train_queue, db_path, *args, **kwargs):
        """
        Init the task queue
        """
        self._predict_queue = predict_queue
        self._train_queue = train_queue
        self._db_path = db_path
        super().__init__(*args, **kwargs)

    def _send_headers(self, status=200):
        """
        Send the http headers
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.send_header("Accept", "text/plain")
        self.end_headers()
    
    def do_POST(self):
        """
        Handling the POST requests
        """
        if self.path == '/predict':
            try:
                print('Handling /predict request')
                self._send_headers()
                datas = self.rfile.read(int(self.headers['Content-Length']))
                predict_req = json.loads(datas)
                # TODO: what to do if the queue is full?
                self._predict_queue.put(predict_req)
            except Exception as e:
                print("Handle get error: ", e.args)
        elif self.path == '/train':
            try:
                print('Handling /train request')
                self._send_headers()
                datas = self.rfile.read(int(self.headers['Content-Length']))
                train_images_dict = json.loads(datas)
                # TODO: what to do if the queue is full?
                self._train_queue.put(train_images_dict)
            except Exception as e:
                print("Handle get error: ", e.args)

    def do_GET(self):
        """
        Handling the GET requests
        """
        if self.path == '/metadata':
            try:
                print('Handling /metadata request')
                self._send_headers()
                metadata = None
                with MLDataBase(self._db_path) as db:
                    metadata = db.query_metadata()
                self.wfile.write(json.dumps(metadata).encode('utf-8'))
            except Exception as e:
                print("Handle get error: ", e.args)
        elif self.path == '/history':
            try:
                print('Handling /history request')
                self._send_headers()
                history = None
                with MLDataBase(self._db_path) as db:
                    history = db.query_history()
                self.wfile.write(json.dumps(history).encode('utf-8'))
            except Exception as e:
                print("Handle get error: ", e.args)


class MLWebHandler(BaseHTTPRequestHandler):
    """
    Http handler for web requests
    """
    def __init__(self, db_path, *args, **kwargs):
        """
        Init
        """
        self._db_path = db_path
        super().__init__(*args, **kwargs)

    def _send_headers(self, status=200):
        """
        Send the http headers
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        # self.send_header("Accept", "text/plain")
        self.end_headers()

    def do_GET(self):
        """
        Handling the GET requests
        """
        try:
            print('Handling web request')
            self._send_headers()
            history = None
            with MLDataBase(self._db_path) as db:
                history = db.query_history()
            history_str = ''
            self.wfile.write(bytes("<html><head><title>ML History</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>History: <br></p>", "utf-8"))
            for i in (range(len(history))):
                history_str = """
                    Record %d:   model version: %s,   image_path: %s,   model_output:%s
                    """ % (i, history[i]['model_version'], history[i]['picture_path'], history[i]['result'])
                self.wfile.write(bytes("<p>%s <br></p>" % history_str, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            # self.wfile.write(json.dumps(history).encode('utf-8'))
        except Exception as e:
            print("Handle get error: ", e.args)

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
if __name__ == "__main__":        
    webServer = HTTPServer(('localhost', 8010), MLWebHandler)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")