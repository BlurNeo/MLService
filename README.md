# MLService
## Introduction
### MLService is a light-weight machine learning service backed with SQLite using HTTP.
### It provides request handling which includes:
- metadata query
  - metadata describes the trained models available for the client to use and the local path of them
- history query
  - history describes the prediction record which includes the model path and the input image path
- predict request
  - this request the service predict for the requested image
- train request
  - this request the service train a new model using the requested images
### Code Structure
- MLService/http/ml_client.py
  - The client for test
- MLService/http/ml_server.py
  - The handler provides ml service
- MLService/http/ml_web_server.py
  - The handler provides web service to display history on web
- MLService/ml
  - The machine learning workers, http handler, wrapper for database and wrappers for prediction and training

### Protocol
- /metadata
  - RequestData: None
  - Return:[
      {"model_version": "0", "model_path": "/Users/ssc/Desktop/models/trained_0.model"}
      {"model_version": "1", "model_path": "/Users/ssc/Desktop/models/trained_1.model"}
    ]
- /train
  - RequestData: {
      "positive_images": ["/Users/ssc/Desktop/OK/20.jpg", "/Users/ssc/Desktop/OK/21.jpg"],
      "negative_images": ["/Users/ssc/Desktop/NG/50.jpg", "/Users/ssc/Desktop/NG/51.jpg"]
    }
  - Return: None
- /predict
  - RequestData: {"image_path": "/Users/ssc/Desktop/20.jpg"}
  - Return: None
- /history
  - RequestData: None
  - Return: [
      {"model_version": "0", "picture_path": "/Users/ssc/Desktop/20.jpg", "result": "NG"},
      {"model_version": "1", "picture_path": "/Users/ssc/Desktop/21.jpg", "result": "NG"}
    ]


## Running
'''python
#### Start the ml server:
python3 http/ml_server.py
#### Start the ml web server:
python3 http/ml_web_server.py
#### Start the ml client for testing:
python3 http/ml_client.py
'''
