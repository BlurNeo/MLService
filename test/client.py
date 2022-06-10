import http.client as httplib
import time
import json

class MLClient(object):
    def __init__(self, bind_id = 8010):
        self.bind_id = bind_id
        self.headers = {"Conetent-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.server_ip = "127.0.0.1"
        self.httpClient = httplib.HTTPConnection(self.server_ip, self.bind_id, timeout = 3000)
        self.frame_id = 0

    def request_metadata(self):
        try:
            self.httpClient.request("GET", "/metadata")#, ''.encode('utf-8'), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)

    def request_train(self, positive_sample_paths, negative_sample_paths):
        try:
            datadic = {"positive_images": positive_sample_paths, "negative_images": negative_sample_paths}
            self.httpClient.request("POST", "/train", json.dumps(datadic), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)

    def request_predict(self, image_path):
        try:
            datadic = {"image_path": image_path}
            self.httpClient.request("POST", "/predict", json.dumps(datadic), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)

    def request_history(self):
        try:
            self.httpClient.request("GET", "/history")#, ''.encode('utf-8'), self.headers)
            response = self.httpClient.getresponse()
            result = response.read()
            print(result)
        except Exception as e:
            print("Send Request or Recevied with error: ", e.args)

if __name__ == "__main__":
    data_list = [n for n in range(1,428)]
    client = MLClient()
    dataset1_positive = [
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/OK/00.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/OK/01.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/OK/02.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/OK/03.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/OK/04.jpg'
    ]
    dataset1_negative = [
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/NG/03.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/NG/07.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/NG/15.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/NG/16.jpg'
        '/Users/ssc/Desktop/workspace/git_repos/MLService/dataset/NG/39.jpg'
    ]
    while True:
        # client.send(data_list)
        # client.request_train(dataset1_positive, dataset1_negative)
        # client.request_predict('~/Desktop/test.txt')
        client.request_metadata()
        # client.request_history()
        time.sleep(1)