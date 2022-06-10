import time

class DummyPredict(object):
    def __init__(self, model_path):
        self._model_path = model_path
        # self._version = version

    def model_path(self):
        return self._model_path

    def run(self, image):
        time.sleep(1)
        res = "NG"
        return res