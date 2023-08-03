import pika, os, logging, time, random
import csv, json
logging.basicConfig()

url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='wiki_updates') # Declare a queue
channel.exchange_declare(exchange='message',
                         exchange_type='topic')

CSV_FILE_PATH = os.environ.get("CSV_FILE_PATH", "./data/de_challenge_sample_data.csv")


data = {}
with open(CSV_FILE_PATH) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for rows in csv_reader:
        id = rows['id']
        data[id] = rows
        bodys = json.dumps(data[id])
        channel.basic_publish(exchange='message', routing_key='wiki_updates', body=bodys)
        print ("[i] Message sent to consumer = "+bodys)
        send_time = random.random()
        time.sleep(send_time)

connection.close()