# Copyright (c) victor su. All rights reserved.
import http.client as httplib
import time
import json
import os

class MLClient(object):
    """
    The client sending ml requests
    """
    def __init__(self, bind_id = 8010):
        """
        Setup http
        """
        self.bind_id = bind_id
        self.headers = {"Conetent-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.server_ip = "127.0.0.1"
        self.httpClient = httplib.HTTPConnection(self.server_ip, self.bind_id, timeout = 3000)
        self.frame_id = 0

    def request_metadata(self):
        """
        Send metadata request
        """
        try:
            self.httpClient.request("GET", "/metadata")#, ''.encode('utf-8'), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)
            exit(-1)

    def request_train(self, positive_sample_paths, negative_sample_paths):
        """
        Send train request
        """
        try:
            datadic = {"positive_images": positive_sample_paths, "negative_images": negative_sample_paths}
            self.httpClient.request("POST", "/train", json.dumps(datadic), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)
            exit(-1)

    def request_predict(self, image_path):
        """
        Send predict request
        """
        try:
            datadic = {"image_path": image_path}
            self.httpClient.request("POST", "/predict", json.dumps(datadic), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)
            exit(-1)

    def request_history(self):
        """
        Send history request
        """
        try:
            self.httpClient.request("GET", "/history")#, ''.encode('utf-8'), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)
            exit(-1)

if __name__ == "__main__":
    client = MLClient()
    work_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
    training_dataset1_positive = [
        work_dir + 'dataset/OK/00.jpg',
        work_dir + 'dataset/OK/01.jpg',
        work_dir + 'dataset/OK/02.jpg',
        work_dir + 'dataset/OK/03.jpg',
        work_dir + 'dataset/OK/04.jpg'
    ]
    training_dataset1_negative = [
        work_dir + 'dataset/NG/03.jpg',
        work_dir + 'dataset/NG/07.jpg',
        work_dir + 'dataset/NG/15.jpg',
        work_dir + 'dataset/NG/16.jpg',
        work_dir + 'dataset/NG/39.jpg'
    ]
    predict_dataset = [
        work_dir + 'dataset/OK/20.jpg',
        work_dir + 'dataset/OK/21.jpg',
        work_dir + 'dataset/OK/22.jpg',
        work_dir + 'dataset/OK/23.jpg'
    ]
    client.request_history()
    client.request_metadata()
    while True:
        client.request_train(training_dataset1_positive, training_dataset1_negative)
        client.request_metadata()
        for i in range(len(predict_dataset)):
            client.request_predict(predict_dataset[i])
            client.request_history()
        time.sleep(1)