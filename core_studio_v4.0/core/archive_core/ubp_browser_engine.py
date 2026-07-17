
"""
UBP Browser Engine (V3)
This script adapts your UBP Physics Engine to run directly inside the browser's 
animation loop, bypassing the need for FastAPI or WebSockets.

Instructions:
1. Ensure your engine files (ubp_space_v3.py, etc.) are uploaded to this workspace.
2. Run this script instead of ubp_server_v3.py.
3. Switch to the VISUAL tab to see the live simulation!
"""
import asyncio
import json
import js

# Try to import the user's space module, fallback to a dummy simulation if not found
try:
    from ubp_space_v3 import Space
    space = Space()
    # Add some default entities if the space is empty
    # space.add_entity(...) 
    HAS_ENGINE = True
except ImportError:
    print("[UBP BROWSER ENGINE] ubp_space_v3.py not found. Running dummy simulation.")
    HAS_ENGINE = False

async def game_loop():
    if globals().get('_ubp_loop_running'):
        print("[UBP BROWSER ENGINE] Loop already running. Stopping previous loop.")
        globals()['_ubp_loop_running'] = False
        await asyncio.sleep(0.1) # Wait for previous loop to exit
        
    globals()['_ubp_loop_running'] = True
    print("[UBP BROWSER ENGINE] Starting live simulation loop at 30 TPS...")
    tick = 0
    while globals().get('_ubp_loop_running'):
        if HAS_ENGINE:
            space.tick()
            # Assuming space.to_dict() returns the Three.js compatible scene data
            scene_data = space.to_dict()
        else:
            # Dummy simulation for demonstration
            import math
            scene_data = {
                "spheres": [
                    {"id": "1", "x": math.cos(tick*0.1)*5, "y": 0, "z": math.sin(tick*0.1)*5, "r": 1, "color": "#E31E24", "label": "Dummy Entity"}
                ],
                "points": [],
                "lines": []
            }
            
        # Send live update to React frontend
        if hasattr(js.window, 'updateScene3D'):
            js.window.updateScene3D(json.dumps(scene_data))
            
        tick += 1
        # Yield to the browser's event loop (approx 30 FPS)
        await asyncio.sleep(1/30)
    print("[UBP BROWSER ENGINE] Loop stopped.")

# Start the loop in the background
asyncio.ensure_future(game_loop())
print("[UBP BROWSER ENGINE] Loop scheduled. Switch to the VISUAL tab!")
