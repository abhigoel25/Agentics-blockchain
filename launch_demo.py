#!/usr/bin/env python3
"""
Auto-launcher for chatbot API and demo
Starts the Flask API server and opens demo.html in browser
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Get the workspace root (parent of where this script is)
workspace_root = Path(__file__).parent.absolute()

# Add paths - make sure they're absolute
mcp_dir = workspace_root / "mcp"
contract_translator_dir = workspace_root / "contract-translator"
demo_file = contract_translator_dir / "demo.html"

# Debug: print the paths being checked
import sys
if '--debug' in sys.argv:
    print(f"Workspace root: {workspace_root}")
    print(f"MCP dir: {mcp_dir}")
    print(f"Contract translator dir: {contract_translator_dir}")
    print(f"Demo file: {demo_file}")
    print(f"Demo file exists: {demo_file.exists()}")

print("=" * 70)
print("IBM Agentics - Smart Contract Translator Demo")
print("=" * 70)

# Check if demo.html exists
if not demo_file.exists():
    print(f"❌ Error: demo.html not found at {demo_file}")
    sys.exit(1)

print(f"\n✓ Demo file found: {demo_file}")

# Start HTTP server for demo.html in background thread
print("\n🌐 Starting local HTTP server for demo...")

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress the default HTTP server logging
        pass

def start_http_server():
    os.chdir(str(contract_translator_dir))
    server = HTTPServer(('localhost', 8000), QuietHTTPRequestHandler)
    server.serve_forever()

http_thread = threading.Thread(daemon=True, target=start_http_server)
http_thread.start()

print("✓ HTTP server started on http://localhost:8000")

# Start the chatbot API in background
print("\n🚀 Starting Chatbot API Server...")
try:
    # Use Popen to start in FOREGROUND so we can see logs
    chatbot_process = subprocess.Popen(
        [sys.executable, str(mcp_dir / "chatbot_api.py")],
        cwd=str(workspace_root)
    )
    
    # Open demo in browser after giving server a moment
    print("\n⏳ Waiting 2 seconds for server to initialize...")
    time.sleep(2)
    
    print(f"\n📖 Opening demo in browser...")
    demo_url = "http://localhost:8000/demo.html"
    
    try:
        webbrowser.open(demo_url)
        print(f"✓ Opened: {demo_url}")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print(f"Please open this URL manually: {demo_url}")
    
    print("\n" + "=" * 70)
    print("✅ Demo is ready!")
    print("=" * 70)
    print("\nServer is running above with full logs visible.")
    print("Press Ctrl+C to stop the server and exit.\n")
    
    # Keep the process alive
    chatbot_process.wait()

except KeyboardInterrupt:
    print("\n\nShutting down...")
    chatbot_process.terminate()
    try:
        chatbot_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        chatbot_process.kill()
    print("✓ Server stopped")
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed to start chatbot API: {e}")
    sys.exit(1)
