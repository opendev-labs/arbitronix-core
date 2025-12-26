from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import List, Dict
from trading_system.core.telemetry import logger

app = FastAPI(title="Arbitronix Core Dashboard")

# Shared state (in real system, use Redis)
dashboard_state = {
    "engine_status": "Starting...",
    "symbols": {},
    "recent_trades": [],
    "equity": 10000.0,
    "pnl": 0.0
}

@app.get("/")
async def get():
    with open("trading_system/web/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send state updates every second
            await websocket.send_json(dashboard_state)
            await asyncio.sleep(1)
    except Exception as e:
        logger.warning(f"Dashboard WS disconnected: {e}")

def update_dashboard_state(key: str, value: any):
    if key in dashboard_state:
        dashboard_state[key] = value
    elif key == "symbol_update":
        symbol = value['s']
        dashboard_state['symbols'][symbol] = value

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
