import redis, json
from ib_insync import *
import asyncio, time, random

# connect to Interactive Brokers 
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# connect to Redis and subscribe to tradingview messages
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
print(r)