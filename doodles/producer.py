from kafka import KafkaProducer
import logging
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
#for x in range(200):
for x in range(4):
    producer.send('hello',b'Hello World')
#producer.send('hello',logging.warning("WARN"))

producer.send('hello', b'This is Kafka-Python')
producer.close(100)
print('sent')
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mymessages"]
mycol = mydb["Kafka"]
for x in mycol.find():
    print(x)
