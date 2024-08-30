from fastapi.middleware.cors import CORSMiddleware
import math
import asyncio
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import RPi.GPIO as GPIO
from fastapi import FastAPI
import uvicorn
from datetime import datetime
from dataclasses import dataclass
import tm1637

#Color helpers
E = (0,0,0) #Empty
W = (255,255,255) #White
R = (255,0,0) #Red
O = (255,78,30) #Orange
G = (0,255,0)


#Message struct
@dataclass
class Message:
    text: str 
    timestamp: datetime

#Instantiate FastAPI
app = FastAPI()
sense = SenseHat()

#Config for CORS
origins = ['ADD YOUR CORS HERE']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

#Initialize a base message
latest = Message("NO MESSAGES", datetime.now())

#Initialize tasks for asyncio so we can reference them globally throughout
loop_task = None

#Infinite loop to display message constantly
async def infinite_loop():
    while True:
        #This is a blocking function. We don't want anything to manipulate the SenseHAT while this is in effect 
        sense.show_message(latest.text,0.1,O,E) #Text, speed, color, bg color
        sense.show_message(datetime.strftime(latest.timestamp,'%a %H:%M'),0.1,G,E)         
        await asyncio.sleep(5) #Async sleep ensures other functions (i.e. shutdown handler or message handler) can run just fine during this time

#Start our tasks
@app.on_event("startup")
async def startup_event():
    global loop_task
    loop_task = asyncio.create_task(infinite_loop())

#Handler for shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    global loop_task
    global sense
    if loop_task:
        loop_task.cancel()
        sense.clear(E) #Clears the SenseHAT display by setting everything to blank
        await loop_task

#Handle a message
@app.get("/messageSend")
async def SetMessage(message = "EMPTY"):
    global latest
    global sense #reference to senseHAT
    latest = Message(message[:100], datetime.now()) #Limit to only 100 chars, cannot always trust the frontend
    #Flash white, flash green, three times
    for n in range(3): 
        sense.clear(W) #All to white
        time.sleep(0.5)
        sense.clear()
        time.sleep(0.5)
        sense.clear(G) #All to green
        time.sleep(0.5)
        sense.clear()
        time.sleep(0.5)
    return{"Message sent!"}


#Instantiate uvicorn 
if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8900, log_level="info")
        
#Play a message as it comes in
#Keep playing it until a new message comes in
