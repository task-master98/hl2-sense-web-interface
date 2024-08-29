import os
import asyncio
import websockets
import signal

CONNECTED_CLIENTS = {}

async def handler(websocket, path):
    try:
        # Wait for client to send its identifier (e.g., "device_name: hololens" or "device_name: web_app")
        identifier_message = await websocket.recv()
        device_name = identifier_message.split(":")[1].strip()
        CONNECTED_CLIENTS[websocket] = device_name
        print(f"Client connected: {device_name} ({websocket.remote_address})")

        async for message in websocket:
            if isinstance(message, bytes):  # Binary data (frame)
                # Only send the frame to web application clients
                for client, device in CONNECTED_CLIENTS.items():
                    if device == "web_app" and client.open:
                        await client.send(message)
            else:
                print(f"Received command from {device_name}: {message}")

    finally:
        del CONNECTED_CLIENTS[websocket]
        print(f"Client {device_name} disconnected.")
    

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