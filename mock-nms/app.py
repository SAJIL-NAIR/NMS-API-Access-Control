from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Secure NMS Northbound Interface",
    description="Mock NMS API for the Secure API Gateway project",
    version="1.0.0"
)


# =========================
# DATA MODELS
# =========================

class Device(BaseModel):
    name: str
    ip: str
    status: str


class DeviceUpdate(BaseModel):
    status: str


# =========================
# MOCK NMS DATABASE
# =========================

devices = [
    {
        "id": 1,
        "name": "Router-01",
        "ip": "192.168.1.10",
        "status": "online"
    },
    {
        "id": 2,
        "name": "Switch-01",
        "ip": "192.168.1.20",
        "status": "online"
    },
    {
        "id": 3,
        "name": "Firewall-01",
        "ip": "192.168.1.30",
        "status": "online"
    }
]


alarms = [
    {
        "id": 101,
        "device": "Router-01",
        "severity": "warning",
        "message": "High CPU usage"
    },
    {
        "id": 102,
        "device": "Switch-01",
        "severity": "critical",
        "message": "Interface down"
    }
]


configuration = {
    "hostname": "NMS-Router-01",
    "location": "Network Lab",
    "management_status": "enabled"
}


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def home():
    return {
        "service": "Mock NMS Northbound Interface",
        "status": "running",
        "message": "NMS API is operational"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# DEVICE MANAGEMENT
# =========================

@app.get("/api/devices")
def get_devices():
    return {
        "count": len(devices),
        "devices": devices
    }


@app.get("/api/devices/{device_id}")
def get_device(device_id: int):

    for device in devices:
        if device["id"] == device_id:
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


@app.post("/api/devices")
def add_device(device: Device):

    new_device = {
        "id": max([d["id"] for d in devices], default=0) + 1,
        "name": device.name,
        "ip": device.ip,
        "status": device.status
    }

    devices.append(new_device)

    return {
        "message": "Device added successfully",
        "device": new_device
    }


@app.put("/api/devices/{device_id}")
def update_device(device_id: int, update: DeviceUpdate):

    for device in devices:
        if device["id"] == device_id:
            device["status"] = update.status

            return {
                "message": "Device updated successfully",
                "device": device
            }

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int):

    for device in devices:
        if device["id"] == device_id:
            devices.remove(device)

            return {
                "message": "Device deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# =========================
# ALARMS
# =========================

@app.get("/api/alarms")
def get_alarms():
    return {
        "count": len(alarms),
        "alarms": alarms
    }


# =========================
# CONFIGURATION
# =========================

@app.get("/api/configuration")
def get_configuration():
    return {
        "configuration": configuration
    }


# =========================
# NMS INFORMATION
# =========================

@app.get("/api/status")
def get_nms_status():
    return {
        "nms": "operational",
        "managed_devices": len(devices),
        "active_alarms": len(alarms),
        "management_interface": "Northbound API"
    }