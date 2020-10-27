#from src.reader import reader
from setup import Worker

worker = Worker()
worker.connect()
worker.publish({"asdf":1})
