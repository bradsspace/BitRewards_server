import asyncio
import websockets
import ssl
from typing import Any
from dataclasses import dataclass
import json



ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')


clients = []

async def handler(websocket, path):
    clients.append(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            response = message
            await asyncio.wait([client.send(response) for client in clients])
    finally:
        clients.remove(websocket)


start_server = websockets.serve(handler, "0.0.0.0", 8000, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print("complete")





# Data Class for incomming transations 
@dataclass
class Cost:
    amount: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Cost':
        _amount = str(obj.get("amount"))
        _type = str(obj.get("type"))
        return Cost(_amount, _type)

@dataclass
class Product:
    sku: str
    displayName: str
    cost: Cost

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        _sku = str(obj.get("sku"))
        _displayName = str(obj.get("displayName"))
        _cost = Cost.from_dict(obj.get("cost"))
        return Product(_sku, _displayName, _cost)

@dataclass
class Root:
    transactionId: str
    product: Product
    userId: str
    displayName: str
    initiator: str

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _transactionId = str(obj.get("transactionId"))
        _product = Product.from_dict(obj.get("product"))
        _userId = str(obj.get("userId"))
        _displayName = str(obj.get("displayName"))
        _initiator = str(obj.get("initiator"))
        return Root(_transactionId, _product, _userId, _displayName, _initiator)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)