from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import os

class BaseCamera(ABC):
    def __init__(self, camera_id: str, zone_id: str):
        self.camera_id = camera_id
        self.zone_id = zone_id
        self.is_connected = True

    @abstractmethod
    async def capture(self, output_dir: str, batch_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Captura una fotografía y retorna metadatos del archivo creado"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado operativo de la cámara"""
        pass

class VirtualCamera(BaseCamera):
    """
    Cámara virtual inicial para pruebas de arquitectura.
    Permite asociar capturas con metadatos y simulación de conectividad.
    """
    def __init__(self, camera_id: str = "CAM-LAR-001", zone_id: str = "ZONE-LAR"):
        super().__init__(camera_id=camera_id, zone_id=zone_id)
        self.resolution = "1920x1080"
        self.mode = "VIRTUAL"

    def get_status(self) -> Dict[str, Any]:
        return {
            "camera_id": self.camera_id,
            "zone_id": self.zone_id,
            "status": "ONLINE" if self.is_connected else "OFFLINE",
            "resolution": self.resolution,
            "mode": self.mode
        }

    async def capture(self, output_dir: str, batch_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if not self.is_connected:
            return None

        os.makedirs(output_dir, exist_ok=True)
        now = datetime.now(timezone.utc)
        filename = f"capture_{self.zone_id}_{int(now.timestamp())}.jpg"
        filepath = os.path.join(output_dir, filename)

        # Crear marcador de archivo o imagen virtual
        if not os.path.exists(filepath):
            with open(filepath, "wb") as f:
                # Cabecera básica simulada
                f.write(b"SIMULATED_IMAGE_DATA_" + now.isoformat().encode())

        return {
            "filename": filename,
            "filepath": filepath,
            "media_type": "IMAGE",
            "zone_id": self.zone_id,
            "batch_id": batch_id,
            "file_size_bytes": os.path.getsize(filepath),
            "resolution": self.resolution,
            "source": "simulation",
            "captured_at": now.isoformat()
        }
