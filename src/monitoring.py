import psutil
import logging
from typing import Dict, List
from datetime import datetime
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.metrics_history = {
            'cpu': [],
            'memory': [],
            'disk': [],
            'network': []
        }
        self.max_history = 100  # Keep last 100 measurements

    def get_system_metrics(self) -> Dict:
        """Get current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network metrics
            net_io = psutil.net_io_counters()
            
            # Process metrics
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'frequency': {
                        'current': cpu_freq.current,
                        'min': cpu_freq.min,
                        'max': cpu_freq.max
                    },
                    'cores': cpu_count
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percent': memory.percent,
                    'swap': {
                        'total': swap.total,
                        'used': swap.used,
                        'percent': swap.percent
                    }
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent,
                    'io': {
                        'read_bytes': disk_io.read_bytes,
                        'write_bytes': disk_io.write_bytes,
                        'read_count': disk_io.read_count,
                        'write_count': disk_io.write_count
                    }
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                },
                'processes': processes
            }
            
            # Update history
            self._update_history(metrics)
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting system metrics: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def _update_history(self, metrics: Dict) -> None:
        """Update metrics history."""
        timestamp = metrics['timestamp']
        
        # CPU history
        self.metrics_history['cpu'].append({
            'timestamp': timestamp,
            'percent': metrics['cpu']['percent']
        })
        
        # Memory history
        self.metrics_history['memory'].append({
            'timestamp': timestamp,
            'used_percent': metrics['memory']['percent'],
            'swap_percent': metrics['memory']['swap']['percent']
        })
        
        # Disk history
        self.metrics_history['disk'].append({
            'timestamp': timestamp,
            'used_percent': metrics['disk']['percent']
        })
        
        # Network history
        self.metrics_history['network'].append({
            'timestamp': timestamp,
            'bytes_sent': metrics['network']['bytes_sent'],
            'bytes_recv': metrics['network']['bytes_recv']
        })
        
        # Trim history to max_history
        for key in self.metrics_history:
            if len(self.metrics_history[key]) > self.max_history:
                self.metrics_history[key] = self.metrics_history[key][-self.max_history:]

    def get_metrics_history(self) -> Dict:
        """Get metrics history."""
        return self.metrics_history

    def get_alerts(self) -> List[Dict]:
        """Get system alerts based on thresholds."""
        alerts = []
        metrics = self.get_system_metrics()
        
        # CPU alert
        if metrics['cpu']['percent'] > 90:
            alerts.append({
                'type': 'cpu',
                'level': 'warning',
                'message': f"High CPU usage: {metrics['cpu']['percent']}%"
            })
        
        # Memory alert
        if metrics['memory']['percent'] > 90:
            alerts.append({
                'type': 'memory',
                'level': 'warning',
                'message': f"High memory usage: {metrics['memory']['percent']}%"
            })
        
        # Disk alert
        if metrics['disk']['percent'] > 90:
            alerts.append({
                'type': 'disk',
                'level': 'warning',
                'message': f"High disk usage: {metrics['disk']['percent']}%"
            })
        
        return alerts

system_monitor = SystemMonitor() 