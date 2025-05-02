import os
import psutil
import logging
import subprocess
from typing import List, Dict, Optional
from pathlib import Path
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class SystemOperations:
    def __init__(self):
        self.allowed_directories = {
            "home": str(Path.home()),
            "desktop": str(Path.home() / "Desktop"),
            "documents": str(Path.home() / "Documents"),
            "downloads": str(Path.home() / "Downloads")
        }

    def list_directory(self, path: str) -> Dict:
        """List contents of a directory with safety checks."""
        try:
            # Convert to absolute path and check if it's in allowed directories
            abs_path = os.path.abspath(path)
            if not any(abs_path.startswith(allowed) for allowed in self.allowed_directories.values()):
                raise HTTPException(status_code=403, detail="Access to this directory is not allowed")

            items = os.listdir(abs_path)
            result = {
                "files": [],
                "directories": []
            }
            
            for item in items:
                full_path = os.path.join(abs_path, item)
                if os.path.isfile(full_path):
                    result["files"].append({
                        "name": item,
                        "size": os.path.getsize(full_path),
                        "modified": os.path.getmtime(full_path)
                    })
                elif os.path.isdir(full_path):
                    result["directories"].append({
                        "name": item,
                        "modified": os.path.getmtime(full_path)
                    })
            
            return result
        except Exception as e:
            logger.error(f"Error listing directory {path}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def read_file(self, path: str) -> str:
        """Read contents of a file with safety checks."""
        try:
            abs_path = os.path.abspath(path)
            if not any(abs_path.startswith(allowed) for allowed in self.allowed_directories.values()):
                raise HTTPException(status_code=403, detail="Access to this file is not allowed")

            with open(abs_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading file {path}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def write_file(self, path: str, content: str) -> Dict:
        """Write content to a file with safety checks."""
        try:
            abs_path = os.path.abspath(path)
            if not any(abs_path.startswith(allowed) for allowed in self.allowed_directories.values()):
                raise HTTPException(status_code=403, detail="Access to this location is not allowed")

            with open(abs_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return {"status": "success", "path": abs_path}
        except Exception as e:
            logger.error(f"Error writing file {path}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def list_processes(self) -> List[Dict]:
        """List all running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return processes
        except Exception as e:
            logger.error(f"Error listing processes: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_process_info(self, pid: int) -> Dict:
        """Get detailed information about a specific process."""
        try:
            process = psutil.Process(pid)
            return {
                "pid": process.pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "create_time": process.create_time(),
                "cmdline": process.cmdline()
            }
        except psutil.NoSuchProcess:
            raise HTTPException(status_code=404, detail="Process not found")
        except Exception as e:
            logger.error(f"Error getting process info for PID {pid}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def terminate_process(self, pid: int) -> Dict:
        """Terminate a process with safety checks."""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return {"status": "success", "pid": pid}
        except psutil.NoSuchProcess:
            raise HTTPException(status_code=404, detail="Process not found")
        except psutil.AccessDenied:
            raise HTTPException(status_code=403, detail="Permission denied")
        except Exception as e:
            logger.error(f"Error terminating process {pid}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

system_ops = SystemOperations() 