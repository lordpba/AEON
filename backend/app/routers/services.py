"""
Public Services API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.simulator import simulator_manager

router = APIRouter()


@router.get("/status")
async def get_services_status() -> Dict[str, Any]:
    """Get current status of all public services"""
    detailed = simulator_manager.get_detailed_status()
    
    if "error" in detailed:
        raise HTTPException(status_code=500, detail=detailed["error"])
    
    return detailed.get("public_services", {})


@router.get("/{service_name}")
async def get_service_detail(service_name: str) -> Dict[str, Any]:
    """Get details for a specific service"""
    services_module = simulator_manager.get_module("public_services")
    
    if not services_module:
        raise HTTPException(status_code=503, detail="Simulator not running")
    
    status = services_module.get_status()
    services = status.get("services", {})
    
    if service_name not in services:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    return {
        "service": service_name,
        "data": services[service_name]
    }


@router.post("/{service_name}/allocate")
async def allocate_service(service_name: str, amount: float) -> Dict[str, Any]:
    """Allocate resources to a service"""
    services_module = simulator_manager.get_module("public_services")
    
    if not services_module:
        raise HTTPException(status_code=503, detail="Simulator not running")
    
    try:
        success = services_module.allocate_service(service_name, amount)
        return {
            "success": success,
            "service": service_name,
            "amount": amount
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
