"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - HexDictionary
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Content-addressable storage for UBP 3.5.

**Paradigm Shift in 3.5**:
Storage itself is coherence preservation. Content addressing is coherence
verification. Persistence is coherence continuity.

**Zero Dependencies**: Only Python stdlib + coherence_substrate
"""

import hashlib
import json
import os
import gzip
from typing import Any, Dict, Optional

from coherence_substrate import CoherenceState


# ============================================================================
# HEX DICTIONARY
# ============================================================================

DEFAULT_STORAGE_DIR = "./persistent_state/hex_dictionary_storage/"
DEFAULT_METADATA_FILE = os.path.join(DEFAULT_STORAGE_DIR, "hex_dict_metadata.json")


class HexDictionary:
    """
    Content-addressable storage for UBP 3.5.
    
    Keys are SHA256 hashes. Data is compressed with gzip.
    """
    
    def __init__(self, storage_dir: str = DEFAULT_STORAGE_DIR, 
                 metadata_file: str = DEFAULT_METADATA_FILE):
        """
        Initialize HexDictionary.
        
        Args:
            storage_dir: Directory for persistent storage
            metadata_file: Path to metadata JSON file
        """
        self.storage_dir = storage_dir
        self.metadata_file = metadata_file
        self.entries: Dict[str, Dict[str, Any]] = {}
        self._ensure_storage_dir()
        self._load_metadata()
    
    def _ensure_storage_dir(self):
        """Ensure storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def _load_metadata(self):
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    self.entries = json.load(f)
            except Exception:
                self.entries = {}
        else:
            self.entries = {}
    
    def _save_metadata(self):
        """Save metadata to file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def _compute_hash(self, data: bytes) -> str:
        """Compute SHA256 hash of data."""
        return hashlib.sha256(data).hexdigest()
    
    def _serialize(self, value: Any, data_type: str = 'auto') -> bytes:
        """
        Serialize value to bytes.
        
        Args:
            value: Value to serialize
            data_type: Type hint ('str', 'json', 'bytes', 'auto')
            
        Returns:
            Serialized bytes
        """
        if data_type == 'bytes' or isinstance(value, bytes):
            return value
        elif data_type == 'str' or isinstance(value, str):
            return value.encode('utf-8')
        elif data_type == 'json' or isinstance(value, (dict, list)):
            return json.dumps(value).encode('utf-8')
        else:
            # Default: JSON
            return json.dumps(str(value)).encode('utf-8')
    
    def _deserialize(self, data: bytes, data_type: str) -> Any:
        """
        Deserialize bytes to value.
        
        Args:
            data: Serialized data
            data_type: Type hint
            
        Returns:
            Deserialized value
        """
        if data_type == 'bytes':
            return data
        elif data_type == 'str':
            return data.decode('utf-8')
        elif data_type == 'json':
            return json.loads(data.decode('utf-8'))
        else:
            return data.decode('utf-8')
    
    def store(self, value: Any, data_type: str = 'auto', 
              metadata: Optional[Dict] = None) -> str:
        """
        Store value and return its hash.
        
        Args:
            value: Value to store
            data_type: Type hint
            metadata: Optional metadata
            
        Returns:
            SHA256 hash of the value
        """
        # Serialize
        serialized = self._serialize(value, data_type)
        
        # Compute hash
        content_hash = self._compute_hash(serialized)
        
        # File path
        file_path = os.path.join(self.storage_dir, f"{content_hash}.gz")
        
        # Write compressed data
        with gzip.open(file_path, 'wb') as f:
            f.write(serialized)
        
        # Store metadata
        self.entries[content_hash] = {
            'path': file_path,
            'type': data_type,
            'meta': metadata or {}
        }
        self._save_metadata()
        
        return content_hash
    
    def retrieve(self, content_hash: str) -> Optional[Any]:
        """
        Retrieve value by hash.
        
        Args:
            content_hash: SHA256 hash
            
        Returns:
            Deserialized value or None
        """
        if content_hash not in self.entries:
            return None
        
        entry = self.entries[content_hash]
        file_path = entry['path']
        data_type = entry['type']
        
        if not os.path.exists(file_path):
            return None
        
        # Read compressed data
        with gzip.open(file_path, 'rb') as f:
            serialized = f.read()
        
        # Deserialize
        return self._deserialize(serialized, data_type)
    
    def exists(self, content_hash: str) -> bool:
        """Check if hash exists."""
        return content_hash in self.entries
    
    def get_metadata(self, content_hash: str) -> Optional[Dict]:
        """Get metadata for hash."""
        if content_hash not in self.entries:
            return None
        return self.entries[content_hash].get('meta', {})
    
    def list_all(self) -> list:
        """List all stored hashes."""
        return list(self.entries.keys())


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 HEX DICTIONARY - Content-Addressable Storage")
    print("=" * 80)
    
    # Create dictionary
    hex_dict = HexDictionary()
    
    # Store some data
    print("\n1. Storing Data:")
    
    # String
    hash1 = hex_dict.store("Hello, UBP 3.5!", data_type='str', 
                           metadata={'type': 'greeting'})
    print(f"   Stored string: {hash1[:16]}...")
    
    # JSON
    data = {'energy': 1e10, 'nrci': 0.999997, 'realm': 'quantum'}
    hash2 = hex_dict.store(data, data_type='json',
                           metadata={'type': 'energy_result'})
    print(f"   Stored JSON: {hash2[:16]}...")
    
    # Retrieve
    print("\n2. Retrieving Data:")
    retrieved1 = hex_dict.retrieve(hash1)
    print(f"   Retrieved string: {retrieved1}")
    
    retrieved2 = hex_dict.retrieve(hash2)
    print(f"   Retrieved JSON: {retrieved2}")
    
    # List all
    print("\n3. All Stored Hashes:")
    all_hashes = hex_dict.list_all()
    print(f"   Total entries: {len(all_hashes)}")
    for h in all_hashes[:5]:  # Show first 5
        meta = hex_dict.get_metadata(h)
        print(f"   {h[:16]}... - {meta.get('type', 'unknown')}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Storage is Coherence Preservation")
    print("=" * 80)
