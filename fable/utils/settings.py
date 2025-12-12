"""
Settings management for FABLE.
Handles persistence of user preferences and window state.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from PyQt6.QtCore import QByteArray


class Settings:
    """Manages application settings with JSON persistence."""
    
    # Default settings
    DEFAULTS: Dict[str, Any] = {
        'window': {
            'geometry': None,
            'state': None,
            'splitter_main': None,
            'splitter_center': None,
        },
        'panels': {
            'file_browser_visible': True,
            'repl_visible': True,
        },
        'editor': {
            'font_family': 'Source Code Pro',
            'font_size': 14,
            'tab_width': 4,
            'show_line_numbers': True,
        },
        'stack': {
            'animation_speed': 1.0,
            'preview_enabled': True,
        },
        'repl': {
            'history': [],
            'history_max': 500,
        },
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize settings manager.
        
        Args:
            config_dir: Directory for config files. Defaults to ~/.config/fable/
        """
        if config_dir is None:
            config_dir = Path.home() / '.config' / 'fable'
        
        self.config_dir = config_dir
        self.config_file = config_dir / 'settings.json'
        self._settings: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Load settings from disk, creating defaults if needed."""
        self._settings = self._deep_copy(self.DEFAULTS)
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                self._merge(self._settings, saved)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings: {e}")
    
    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy a nested dict/list structure."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(v) for v in obj]
        return obj
    
    def _merge(self, base: Dict, overlay: Dict) -> None:
        """Merge overlay dict into base dict recursively."""
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge(base[key], value)
            else:
                base[key] = value
    
    def save(self) -> None:
        """Save settings to disk."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a setting value.
        
        Args:
            section: Settings section (e.g., 'window', 'editor')
            key: Setting key within section
            default: Default value if not found
        
        Returns:
            The setting value or default
        """
        return self._settings.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set a setting value.
        
        Args:
            section: Settings section
            key: Setting key within section
            value: Value to store
        """
        if section not in self._settings:
            self._settings[section] = {}
        self._settings[section][key] = value
    
    def get_bytes(self, section: str, key: str) -> Optional[QByteArray]:
        """Get a QByteArray setting (for window geometry/state).
        
        Args:
            section: Settings section
            key: Setting key
        
        Returns:
            QByteArray or None
        """
        value = self.get(section, key)
        if value:
            return QByteArray.fromHex(value.encode())
        return None
    
    def set_bytes(self, section: str, key: str, value: QByteArray) -> None:
        """Set a QByteArray setting.
        
        Args:
            section: Settings section
            key: Setting key
            value: QByteArray to store
        """
        self.set(section, key, bytes(value.toHex()).decode())


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
