# celery-flask-example

Template for Python3 Flask and Celery projects.

### How to install and run
You need to install a celery broker/backend (like rabbitmq) to proceed:
```bash
apt install rabbitmq-server
```
Then you can setup the proyect:
```python
pip install gevent
python setup.py install
python run.py
```
Then you run the celery workers (explained in next sections) and proceed to use the api.
 
 ### How to test the application
 You can find a file called test.postma_collection with the tests of the endpoints, but there are some examples.
```bash
# GET /v1/sum
curl --location --request GET 'http://localhost:8000/v1/sum?num1=1&num2=2'
 
# POST /v1/sum
curl --location --request POST 'http://localhost:8000/v1/sum' \
--header 'Content-Type: multipart/form-data; \
--form 'num1=1' \
--form 'num2=2'
```

### How to run a celery worker
```bash
 celery -A path_to_application worker --pool=pool_type --concurrency=num_threads -l log_level
```
 - path_to_application: if you are positioned on the folder where celery object is declared, only write file.celery (with file the file.py).
   Otherwise, its better to execute a command like ./folder1/folder2/.../foldern/file.celery, but it usually doesn't work.
 - pool_type: there are a lot of celery pools, but the most compatible in all operating systems and linux distributions is gevent.
 - num_thread: the number of threads that the pool is permitted to create. Its not recommended to creeate more than 2*(numProcessors-1) threads 
    unless you are developing tasks with a lot of sleep or blocking time slots (like scraping or syncrhornizing).
 - log_level: its recommended to write a log level of info, because debug is too much information to understand what your tasks are doing.
 
 As example, if you are in the repository folder, you can write
```python
 celery -A app.celery worker --pool=gevent --concurrency=14 -l info
```
