import asyncio
import json
import time
import websockets
import logging
from typing import List, Callable, Dict, Optional
from trading_system.core.config import Config
from trading_system.core.telemetry import logger

class BinanceWebSocketManager:
    def __init__(self, symbols: List[str], callback: Callable[[Dict], None]):
        self.symbols = [s.lower() for s in symbols]
        self.callback = callback
        self.running = False
        self.ws = None
        self.base_url = "wss://stream.binance.com:9443/ws"
        if Config.TRADING_MODE.value == "TESTNET":
            self.base_url = "wss://testnet.binance.vision/ws"
        
        self.reconnect_delay = 5
        self.last_msg_time = time.time()

    async def start(self):
        self.running = True
        while self.running:
            try:
                streams = "/".join([f"{s}@trade" for s in self.symbols])
                url = f"{self.base_url}/{streams}"
                logger.info(f"Connecting to Binance WebSocket: {url}...")
                
                async with websockets.connect(url) as ws:
                    self.ws = ws
                    logger.success("Connected to Binance WebSocket")
                    self.reconnect_delay = 5  # Reset backoff
                    
                    while self.running:
                        try:
                            msg = await asyncio.wait_for(ws.recv(), timeout=20.0)
                            data = json.loads(msg)
                            self.last_msg_time = time.time()
                            await self.callback(data)
                        except asyncio.TimeoutError:
                            logger.warning("WebSocket Keepalive Timeout. Reconnecting...")
                            break
                        except websockets.exceptions.ConnectionClosed:
                            logger.warning("WebSocket Connection Closed. Reconnecting...")
                            break
            except Exception as e:
                logger.error(f"WebSocket Error: {e}")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, 60) # Exponential backoff

    async def stop(self):
        logger.info("Stopping WebSocket Manager...")
        self.running = False
        if self.ws:
            await self.ws.close()

if __name__ == "__main__":
    # Test
    async def handler(msg):
        print(f"Update: {msg.get('s')} ${msg.get('p')}")

    ws = BinanceWebSocketManager(["btcusdt", "ethusdt"], handler)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(ws.start())
    except KeyboardInterrupt:
        loop.run_until_complete(ws.stop())
