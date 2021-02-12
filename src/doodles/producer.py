from kafka import KafkaProducer
import logging


producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
#for x in range(200):
hello_b = 'Hello World'.encode()
for x in range(4):
    producer.send('test', hello_b)
#producer.send('hello',logging.warning("WARN"))

producer.send('test', b'This is Kafka-Python')
producer.close(100)
print('sent')
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mymessages"]
mycol = mydb["Kafka"]
for x in mycol.find():
    print(x)
