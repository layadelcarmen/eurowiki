==============
EuroWiki Media
==============

The application sets a producer and a consumer using RabbitMQ to process the wikipedia updates.
Global updates count, and german updates are aggregated every minute and stored in a PostgresSQL database.

The consumer is based in the asyncio_consumer_example from pika library, to ensure on-time processing.

#Steps:

Clone the repo and run the following command in you terminal:


Set environment variables

```
CSV_FILE_PATH
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
```

Start RabbitMQ and PostgresSQL server with docker compose or create manually two databases in your server(dainmedians, daintests)

```
docker-compose up
```

Create a python environment and run:

```
pip3 install -r requirements.txt
```

## Running the script:


Start the producer in your terminal .

```
python producer.py
```

Open a second terminal. Start the consumer.

```
python consumer.py
```


Run the application tests:

```
Pending...
```


## Considerations about the solution:

##Data design

Multi-measure records

In this case, the application emit multiple metrics or events at the same timestamp. In such cases, could be store all 
the metrics emitted at the same timestamp in the same multi-measure record. All the measures stored in the same 
multi-measure record appear as different columns in the same row of data.

A possible extention is to add a 'measure' column, to consider other Wikipedia updates not just type='edit'


##Database considerations:


- How long must be keept the saved data?
- Needs near realtime processing?
- Cost considerations

In this case was used PostgresSQL as database, due to its high performance and the posibilty to use partitioning.
A weekly partition was choosed(sql/setup.sql), but this could be adjusted accordingly the analysis(daily? monthly?)

Another choice to consider is Amazon Timestream using customer-defined partition keys. This may be a better choice 
considering the actual throughput, future needs and scalability.


##Exchange type

Selected: Topic

Although a `direct` type would satisfy the current task, wider possibilities are open for distributing data 
relevant to other geographic location, not only for the german wikipedia.


##Process improvements

The field added_date  of type timestamp, was set to the current time. This choice considers a 'real time' connection 
to the Wiki Recent API, to use the current date during the aggregation.
The sample data file contains a `meta_dt` this may be the exact moment the change was registered. However all the 
aggregated data would not have the same timestamp.



Author:
[Laya Rabasa](https://github.com/layadelcarmen)


Sources:

[1] 
https://github.com/pika/pika/blob/main/examples/asyncio_consumer_example.py

[2]
https://docs.aws.amazon.com/timestream/latest/developerguide/data-modeling.html

[3]
https://www.rabbitmq.com/tutorials/amqp-concepts.html
