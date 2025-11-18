import requests
import xml.etree.ElementTree as ET

class BluOSClient:
    def __init__(self, host: str, port: int = 11000, timeout: int = 10):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.timeout = timeout
        self.volume = None

    def _make_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def set_volume(self, level: int):
        """Set volume level (0-100)"""
        if not 0 <= level <= 100:
            raise ValueError("Volume must be between 0 and 100")
        
        response = self.session.get(self._make_url('/Volume'), 
                                    params={'level': level})
        response.raise_for_status()
        self.volume = level
    
    def increase_volume(self, increment: int = 5):
        """Increments the volume by increment value."""
        if self.volume is None:
            self.volume = self.get_volume_level()
        
        new_volume = min(100, self.volume + increment)
        self.set_volume(new_volume)
    
    def decrease_volume(self, decrement: int = 5):
        """Decrements the volume by decrement value."""
        if self.volume is None:
            self.volume = self.get_volume_level()
        
        new_volume = max(0, self.volume - decrement)
        self.set_volume(new_volume)

    def get_volume_level(self) -> int:
        """Get the current volume level of the player."""
        response = self.session.get(self._make_url('/Status'))
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        volume_elem = root.find('.//volume')
        if volume_elem is not None:
            return int(volume_elem.text)
        return 0
    
    def play(self):
        """Start playback"""
        response = self.session.get(self._make_url('/Play'))
        response.raise_for_status()
    
    def pause(self):
        """Pause playback"""
        response = self.session.get(self._make_url('/Pause'))
        response.raise_for_status()
    
    def next_track(self):
        """Skip to next track"""
        response = self.session.get(self._make_url('/Skip'))
        response.raise_for_status()
    
    def previous_track(self):
        """Go to previous track"""
        response = self.session.get(self._make_url('/Back'))
        response.raise_for_status()
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
