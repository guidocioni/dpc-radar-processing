import asyncio
import websockets as ws
from datetime import datetime
import json
import csv

file_path = 'dump.txt'  # choose your file path
server = 'wss://7ju75f7wai.execute-api.eu-south-1.amazonaws.com/Prod/'

async def receiver():
    async with ws.connect(server) as websocket:
        response = await websocket.recv()
        data = json.loads(response)
        data['datetime'] = datetime.utcfromtimestamp(int(data['time']) / 1000.).strftime("%c")
        data['datetime_now'] = datetime.utcnow().strftime("%c")
        print(data)

        with open(file_path, 'a') as f:
            if f.tell() == 0:
                # file is empty or new file
                csv_writer = csv.writer(f)
                header = data.keys()
                csv_writer.writerow(header)
                csv_writer.writerow(data.values())
            else:
                # file exists, appending
                csv_writer = csv.writer(f)
                csv_writer.writerow(data.values())


async def forever():
    while True:
        await receiver()

loop = asyncio.get_event_loop()
loop.run_until_complete(forever())
