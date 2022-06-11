# Copyright (c) victor su. All rights reserved.
from dummy_train import DummyTrain as MLTrain
from dummy_predict import DummyPredict as MLPredict
from ml_db import MLDataBase
import threading

class MLWorker(object):
    """
    Workers for the prediction and training using threads
    """
    def __init__(self, predict_queue, train_queue, db_path, model_dir):
        """
        Init the variables
        """
        self._predict_queue = predict_queue
        self._train_queue = train_queue
        self._db_path = db_path
        self._model_dir = model_dir
    
    def start(self):
        """
        Start the prediction and training workers
        """
        def predict_worker(idx, q, db_path):
            """
            The prediction worker
            """
            info = None
            # initialize the prediction from the latest trained model
            with MLDataBase(db_path) as db:
                info = db.query_latest_model_info()
                # make sure idx won't exceed the size of info
                info = info[min(idx, len(info[idx]))]
            latest_version = info['model_version']
            latest_path = info['model_path']
            predictor = MLPredict(latest_path)
            while True:
                # thread blocked if queue empty
                image_path = q.get()['image_path']
                print('predict queue size: ', q.qsize())
                with MLDataBase(db_path) as db:
                    info = db.query_latest_model_info()
                    # make sure idx won't exceed the size of info
                    info = info[min(idx, len(info[idx]))]
                # if there is newly trained model, reinitialize the prediction
                if info['model_path'] != predictor.model_path():
                    predictor = MLPredict(info['model_path'])
                result = predictor.run(image_path)
                # insert the prediction input and output into database
                with MLDataBase(db_path) as db:
                    db.insert_history(str(info['model_version']), image_path, str(result))
        
        def train_worker(q, db_path, model_dir):
            """
            The training worker
            """
            while True:
                # thread blocked if queue empty
                image_paths = q.get()
                info = None
                with MLDataBase(db_path) as db:
                    info = db.query_latest_model_info()[0]
                latest_ver = int(info['model_version'])
                # increment the latest version read from database
                latest_ver = latest_ver + 1
                # train the model with the new dataset
                trainner = MLTrain(model_dir, latest_ver)
                trained_model_path = trainner.run(image_paths)
                # insert the newly trained model metadata into database
                with MLDataBase(db_path) as db:
                    db.insert_metadata(str(latest_ver), trained_model_path)
        
        # Thread pools for prediction
        self._predict_pool = []
        predict_pool_size = 2
        for idx in range(predict_pool_size):
            self._predict_pool.append(threading.Thread(
                target=predict_worker, args=(idx, self._predict_queue, self._db_path)))
        for idx in range(predict_pool_size):
            self._predict_pool[idx].start()
        # Thread for training
        self._train_thread = threading.Thread(
            target=train_worker, args=(self._train_queue, self._db_path, self._model_dir))
        self._train_thread.start()

import queue
if __name__ == "__main__":
    work_dir = '/Users/ssc/Desktop/workspace/git_repos/MLService/'
    db_path = work_dir + 'db/ml.db'
    predict_queue = queue.Queue(maxsize=20)
    train_queue = queue.Queue(maxsize=20)
    ml_worker = MLWorker(predict_queue, train_queue, db_path, work_dir + 'models/')
    ml_worker.start()