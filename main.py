#from src.reader import reader
import Worker

worker = Worker()
worker.connect()
worker.publish({"asdf":1})
