from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socketio

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
app.mount("/socket.io", socketio.ASGIApp(sio))
app.mount("/", StaticFiles(directory="public", html=True), name="public")

ROOM = "private-room"

@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")
    await sio.enter_room(sid, ROOM)

@sio.event
async def disconnect(sid):
    print(f"User disconnected: {sid}")

@sio.event
async def offer(sid, data):
    await sio.emit('offer', data, room=ROOM, skip_sid=sid)

@sio.event
async def answer(sid, data):
    await sio.emit('answer', data, room=ROOM, skip_sid=sid)

@sio.event
async def ice_candidate(sid, data):
    await sio.emit('ice-candidate', data, room=ROOM, skip_sid=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
