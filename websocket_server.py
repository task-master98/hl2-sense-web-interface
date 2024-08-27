import os
import asyncio
import websockets
import signal

CONNECTED_CLIENTS = set()
UPLOAD_FOLDER = "frames/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

async def handler(websocket, path):
    CONNECTED_CLIENTS.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    
    async for message in websocket:
        print(f"Received message: {message}")

        if isinstance(message, bytes):
            with open(os.path.join(UPLOAD_FOLDER, "captured_frame.png"), "wb") as f:
                f.write(message)
            print(f"Frame received and saved")
        for client in CONNECTED_CLIENTS:
            if client != websocket and client.open:
                await client.send(message)
    

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        print(f"WebSocket server started on :{port}")
        await stop

if __name__ == "__main__":
    asyncio.run(main())