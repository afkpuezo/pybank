from kafka import KafkaConsumer
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mymessages"]
mycol = mydb["Kafka"]
consumer = KafkaConsumer('test')
for message in consumer:
    print(message.value)
    data = {"message": message.value , "time":message.timestamp}
    print()
    mycol.insert_one(data)
    if "Kafka" in str(data["message"]):
        break
print("consumer is done!")
exit(0)


    
