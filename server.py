from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socketio

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app.mount("/socket.io", socketio.ASGIApp(sio))
app.mount("/", StaticFiles(directory="public", html=True), name="public")

@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"User disconnected: {sid}")

@sio.event
async def join_room(sid, data):
    room = data['room']
    sio.enter_room(sid, room)
    print(f"{sid} joined room {room}")

@sio.event
async def offer(sid, data):
    await sio.emit('offer', data, room=data['room'], skip_sid=sid)

@sio.event
async def answer(sid, data):
    await sio.emit('answer', data, room=data['room'], skip_sid=sid)

@sio.event
async def ice_candidate(sid, data):
    await sio.emit('ice-candidate', data, room=data['room'], skip_sid=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001)
