# AIEnterpriseWF
Capstone Project for IBM AI Enterprise Workflow

## Usage Notes

All commands are from main directory (ie "AIEnterpriseWF")

Test the Flask App (app.py)
--------------------------

~$ python app.py

or to start the flask app in debug mode
   
~$ python app.py -d

Go to http://127.0.0.1:8080/ and you will see a basic website that can be customtized for a project.


Run the unittests
-------------------

Before running the unit tests launch the `app.py`.

To run only the api tests (if app.py is not launched, then all tests will be skipped)

~$ python unittests/ApiTests.py


To run only the model tests

~$ python unittests/ModelTests.py


To run only the model tests

~$ python unittests/LoggerTests.py


To run all of the tests

~$ python run-tests.py


To build the docker container
--------------------------------

~$ docker build -t ai-capstone .

Check that the image is there.

~$ docker image ls

If there are images that you no longer use, You may delete them with

~$ docker image rm IMAGE_ID_OR_NAME

And every once and a while if you want clean up you can

~$ docker system prune


Run the container to test that it is working
----------------------------------------------

~$ docker run -p 4000:8080 ai-capstone

Go to http://127.0.0.1:8080/ and you will see a basic website that can be customised for a project.


Test the running application
------------------------------

First go to [http://127.0.0.1:8080/](http://0.0.0.0:4000/) to ensure the app is running and accessible.

For training the model: [http://127.0.0.1:8080/train](http://0.0.0.0:4000/train)

For making predictions using the model: [http://127.0.0.1:8080/predict](http://0.0.0.0:4000/predict)


## Evaluation Criteria Input

Are there unit tests for the API?
/unittests/ApiTests.py

Are there unit tests for the model?
/unittests/ModelTests.py

Are there unit tests for the logging?
/unittests/LoggerTests.py

Can all of the unit tests be run with a single script and do all of the unit tests pass?
/run-tests.py

Is there a mechanism to monitor performance?
/unittests/logger.py

Was there an attempt to isolate the read/write unit tests From production models and logs?
Yes. Using sl as prefix for production models and logs. For test no prefix is usedv
/unittests/*
/model/*

Does the API work as expected? For example, can you get predictions for a specific country as well as for all countries combined?
/app.py
 
Does the data ingestion exists as a function or script to facilitate automation?
/model/cslib.py

Where multiple models compared?
/notebooks/Capstone_Comparison.py

Did the EDA investigation use visualizations?
/notebooks/Capstone_EDA.ipynb

Is everything containerized within a working Docker image?
/Dockerfile

Did they use a visualization to compare their model to the baseline model?
/notebooks/*
