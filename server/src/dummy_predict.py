import time

class DummyPredict(object):
    def __init__(self, model_path):
        self._model_path = model_path
        # self._version = version
        self._flag = 1

    def model_path(self):
        return self._model_path

    def run(self, image):
        # mock the prediction
        time.sleep(1)
        if self._flag % 3 == 1:
            res = "NG"
        else:
            res = "OK"
        self._flag = self._flag + 1
        return res