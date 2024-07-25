import streamlit as st
import asyncio
import websockets
import threading

async def websocket_handler(websocket, path):
    async for message in websocket:
        st.session_state["websocket_message"] = message

async def run_websocket_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8765)
    await server.wait_closed()

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_websocket_server())

if 'websocket_server_started' not in st.session_state:
    st.session_state['websocket_server_started'] = True
    threading.Thread(target=start_websocket_server, daemon=True).start()

async def send_command(command):
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            await websocket.send(command)
            print(f"Sent command : {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

def send_command_async(command):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_command(command))

st.title("Remote Control for HoloLens")

if st.button("Increase Distance"):
    send_command_async("increase_distance")

if st.button("Decrease Distance"):
    send_command_async("decrease_distance")

if 'websocket_message' in st.session_state:
    st.write(f"Received message: {st.session_state['websocket_message']}")