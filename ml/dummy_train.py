# Copyright (c) victor su. All rights reserved.
import time, os

class DummyTrain(object):
    """
    The Dummy Training Wrapper
    """
    def __init__(self, model_dir, version):
        """
        Init
        """
        self._model_dir = model_dir
        self._version = version

    def run(self, images):
        """
        Run the training
        """
        # mock the training
        time.sleep(10)
        trained_model_path = self._model_dir + 'trained_' + str(self._version) + '.model'
        return trained_model_path

if __name__ == "__main__":
    work_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
    model_dir = work_dir + 'models/'
    version = 1
    images = [
        work_dir + 'dataset/OK/00.jpg',
        work_dir + 'dataset/OK/01.jpg',
        work_dir + 'dataset/OK/02.jpg',
        work_dir + 'dataset/OK/03.jpg',
        work_dir + 'dataset/OK/04.jpg'
    ]
    train = DummyTrain(model_dir, version)
    trained_model_path = train.run(images)
    print('trained_model_path:', trained_model_path)