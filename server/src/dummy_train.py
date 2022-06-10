import time

class DummyTrain(object):
    def __init__(self, model_dir, version):
        self._model_dir = model_dir
        self._version = version

    def run(self, images):
        time.sleep(10)
        trained_model_path = self._model_dir + 'trained_' + str(self._version) + '.model'
        return trained_model_path