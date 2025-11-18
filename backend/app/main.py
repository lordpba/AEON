"""
AEON GovTech Platform - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from typing import List
from loguru import logger

from app.routers import services, infrastructure, governance, citizens, ai, scenarios
from app.core.config import settings
from app.core.simulator import simulator_manager


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting AEON GovTech Platform API")
    simulator_manager.start()
    
    # Background task to broadcast updates
    async def broadcast_updates():
        while True:
            try:
                status = simulator_manager.get_status()
                await manager.broadcast({
                    "type": "status_update",
                    "data": status
                })
                await asyncio.sleep(2)  # Update every 2 seconds
            except Exception as e:
                logger.error(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)
    
    task = asyncio.create_task(broadcast_updates())
    
    yield
    
    # Shutdown
    logger.info("Shutting down AEON GovTech Platform API")
    task.cancel()
    simulator_manager.stop()


# Create FastAPI app
app = FastAPI(
    title="AEON GovTech Platform API",
    description="AI-Powered Democratic Governance Platform for Smart Cities",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    return {
        "name": "AEON GovTech Platform API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# WebSocket endpoint for real-time updates
@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Include routers
app.include_router(services.router, prefix="/api/v1/services", tags=["Public Services"])
app.include_router(infrastructure.router, prefix="/api/v1/infrastructure", tags=["Infrastructure"])
app.include_router(governance.router, prefix="/api/v1/governance", tags=["Governance"])
app.include_router(citizens.router, prefix="/api/v1/citizens", tags=["Citizens"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Advisor"])
app.include_router(scenarios.router, prefix="/api/v1/scenarios", tags=["Scenarios"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
