#!/usr/bin/env python
"""Test basic API connectivity"""
import sys
import time

print("Testing API connectivity...")
time.sleep(2)

try:
    import requests
    print("✓ requests library available")
    
    r = requests.get("http://localhost:8000/")
    print(f"✓ Root endpoint: {r.status_code}")
    print(f"  Response: {r.json()}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
