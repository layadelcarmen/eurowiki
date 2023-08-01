==============
Europace Media
==============


## Prerequisite Steps:

Unpack the solution, and run the following command in you terminal:

```
pip3 install -r requirements.txt
```

Set environment variables

```
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
POSTGRES_TEST_DB
```

Start RabbitMQ and PostgresSQL server with docker compose or create manually two databases in your server(dainmedians, daintests)

```
docker-compose up
```


Install the solution in developer mode

```
python -m pip install -e . 
```


## Running the script:
After installing all the requirements, datapipe command will be ready to use:


Start producer in your terminal to load the input sensor data.

```
python producer.py
```

Start consumer in your terminal to load the input sensor data.

```
python consumer.py
```



Run the application tests:

```
cd tests
pytest test.py
```


Author:
[Laya Rabasa](https://github.com/layadelcarmen)
