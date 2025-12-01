"""
Chatbot API Server - Bridges demo.html with chatbot.py functionality

This provides a REST API for the demo.html to communicate with the actual chatbot
and MCP servers, allowing real contract function calls.
"""

import os
import asyncio
import json
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
from fastmcp import Client
import sys
import tempfile
import shutil
import importlib.util
from queue import Queue
import threading

# Add contract-translator directory to path
contract_translator_path = Path(__file__).parent.parent / "contract-translator"
sys.path.insert(0, str(contract_translator_path))

from agentics import LLM, user_message, system_message

# Import ContractTranslator from agentic_implementation
try:
    from agentic_implementation import IBMAgenticContractTranslator
    ContractTranslator = IBMAgenticContractTranslator
except ImportError:
    # Fallback: try direct import
    import importlib.util
    spec = importlib.util.spec_from_file_location("agentic_implementation", contract_translator_path / "agentic_implementation.py")
    agentic_impl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agentic_impl)
    ContractTranslator = agentic_impl.IBMAgenticContractTranslator

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env")

llm = LLM(model="gpt-4o-mini")
app = Flask(__name__)
CORS(app)

# Global state
current_mcp_client = None
current_tools = []
current_contract_type = "sales"

# Store ongoing translation sessions for pause/resume
translation_sessions = {}


async def decide_tool_call(user_input: str, tools: list, contract_type: str) -> dict:
    """Use LLM to decide which tool to call based on user input."""
    
    tool_descriptions = []
    for t in tools:
        if hasattr(t, 'name'):
            name = t.name
            desc = t.description if hasattr(t, 'description') else 'No description'
            input_schema = t.inputSchema if hasattr(t, 'inputSchema') else {}
        else:
            name = t.get('name', 'unknown')
            desc = t.get('description', 'No description')
            input_schema = t.get('inputSchema', {})
        
        tool_descriptions.append(f"- {name}: {desc}")
    
    tool_descriptions_str = "\n".join(tool_descriptions)
    
    messages = [
        system_message(
            f"""You are an AI assistant managing a {contract_type} smart contract.
            
Your job is to understand what the user wants and decide which contract tool to call.

Available tools:
{tool_descriptions_str}

When the user makes a request, respond with ONLY valid JSON (no explanations or markdown).
Format: {{"tool": "function_name", "args": {{"param1": value1, "param2": value2}}}}

Common requests:
- "What's the status?" → call a status/view function
- "Pay rent" → call payment functions
- "Check balance" → call balance checking functions
- "Get details" → call getter functions

Always use actual function names from the available tools.
If the user's request doesn't match any tool, respond with {{"tool": "none", "explanation": "I don't see a matching function for that request"}}"""
        ),
        user_message(
            f"""User request: "{user_input}"

Respond with ONLY the JSON, no extra text or markdown."""
        )
    ]
    
    response = llm.chat(messages=messages)
    response_text = str(response).strip()
    
    # Remove markdown fences if present
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    try:
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"error": f"Invalid response format: {response_text}", "exception": str(e)}


def wait_for_approval(session_id: str, timeout: int = 600):
    """Wait for user approval before continuing translation"""
    import time
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if session_id in translation_sessions:
            session = translation_sessions[session_id]
            if 'user_approval' in session:
                approval = session['user_approval']
                del session['user_approval']  # Clear the approval flag
                return approval
        time.sleep(0.5)
    
    return False  # Timeout


@app.route('/api/translate-stream', methods=['POST'])
def translate_stream():
    """Stream real-time updates during 6-phase translation pipeline using Server-Sent Events"""
    import uuid
    
    try:
        # Get the uploaded PDF file
        if 'file' not in request.files:
            print("❌ No file in request")
            return Response(f"data: {json.dumps({'error': 'No file provided', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        file = request.files['file']
        if file.filename == '':
            print("❌ Empty filename")
            return Response(f"data: {json.dumps({'error': 'No file selected', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        if not file.filename.lower().endswith('.pdf'):
            print(f"❌ Invalid file type: {file.filename}")
            return Response(f"data: {json.dumps({'error': 'Only PDF files are supported', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        print(f"📄 Processing file: {file.filename}")
        
        # Create a session ID for this translation
        session_id = str(uuid.uuid4())
        translation_sessions[session_id] = {'temp_path': None}
        print(f"📋 Created session: {session_id}")
        
        # Save to temporary location
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            file.save(tmp_file.name)
            temp_pdf_path = tmp_file.name
            translation_sessions[session_id]['temp_path'] = temp_pdf_path
            print(f"✓ Saved to temp: {temp_pdf_path}")
        
        def generate():
            """Generator for Server-Sent Events"""
            try:
                # Initialize the real translator
                print("🚀 Initializing ContractTranslator...")
                translator = ContractTranslator()
                print("✓ Translator initialized")
                
                # Run the streaming 6-phase pipeline
                print("📋 Starting 6-phase translation pipeline...")
                for phase_update in translator.translate_contract_streaming(
                    input_path=temp_pdf_path,
                    output_dir="./output",
                    require_audit_approval=False,
                    generate_mcp_server=True
                ):
                    # Send each phase update as an SSE event
                    print(f"📡 Streaming phase {phase_update['phase']}...")
                    
                    # For Phase 4 (security audit), pause and wait for approval
                    if phase_update['phase'] == 4 and phase_update['status'] == 'needs_approval':
                        print(f"⏸️  Waiting for user approval on Phase 4...")
                        # Include session_id in the event so frontend knows which session to approve
                        phase_update['session_id'] = session_id
                        yield f"data: {json.dumps(phase_update)}\n\n"
                        
                        # Wait for user approval
                        approval = wait_for_approval(session_id, timeout=600)
                        print(f"✓ User approval received: {approval}")
                        
                        if not approval:
                            print("❌ User rejected the audit or approval timed out")
                            error_event = {"error": "Security audit rejected or approval timed out", "phase": 0}
                            yield f"data: {json.dumps(error_event)}\n\n"
                            return
                        else:
                            # Continue to next phase
                            continue
                    
                    yield f"data: {json.dumps(phase_update)}\n\n"
                
                print("✓ Translation streaming completed")
                
            except Exception as e:
                print(f"❌ Translation error: {str(e)}")
                import traceback
                traceback.print_exc()
                error_event = {"error": str(e), "phase": 0}
                yield f"data: {json.dumps(error_event)}\n\n"
            
            finally:
                # Clean up temp file
                if session_id in translation_sessions and translation_sessions[session_id]['temp_path']:
                    temp_path = translation_sessions[session_id]['temp_path']
                    if Path(temp_path).exists():
                        try:
                            os.unlink(temp_path)
                            print(f"✓ Cleaned up temp file")
                        except:
                            pass
                # Clean up session
                if session_id in translation_sessions:
                    del translation_sessions[session_id]
        
        return Response(generate(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        })
    
    except Exception as e:
        print(f"❌ API error: {str(e)}")
        import traceback
        traceback.print_exc()
        error_event = {"error": str(e), "phase": 0}
        return Response(f"data: {json.dumps(error_event)}\n\n", mimetype='text/event-stream'), 500


@app.route('/api/audit-approval', methods=['POST'])
def audit_approval():
    """Handle user approval/rejection of security audit"""
    data = request.json
    session_id = data.get('session_id')
    approved = data.get('approved', False)
    
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    
    if session_id not in translation_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    # Store the approval and resume the stream
    translation_sessions[session_id]['user_approval'] = approved
    print(f"📝 User approval: {approved} (Session: {session_id})")
    
    return jsonify({"success": True, "message": f"Audit {'approved' if approved else 'rejected'}"})


@app.route('/api/translate', methods=['POST'])
def translate_contract_endpoint():
    """Legacy endpoint - redirects to stream"""
    return translate_stream()


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "mcp_connected": current_mcp_client is not None})


@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to verify API is working"""
    return jsonify({
        "status": "ok",
        "message": "API is working correctly",
        "openai_key": "✓ Set" if OPENAI_API_KEY else "❌ Not set",
        "translator_importable": True
    })


@app.route('/api/connect', methods=['POST'])
def connect_mcp():
    """Connect to MCP server"""
    global current_mcp_client, current_tools, current_contract_type
    
    data = request.json
    mcp_path = data.get('mcp_path')
    contract_type = data.get('contract_type', 'sales')
    
    if not Path(mcp_path).exists():
        return jsonify({"error": f"MCP server not found: {mcp_path}"}), 404
    
    try:
        # Create event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def connect():
            client = Client(mcp_path)
            await client.__aenter__()
            tools = await client.list_tools()
            return client, tools
        
        current_mcp_client, current_tools = loop.run_until_complete(connect())
        current_contract_type = contract_type
        
        tool_names = []
        for t in current_tools:
            if hasattr(t, 'name'):
                tool_names.append(t.name)
            else:
                tool_names.append(t.get('name', 'unknown'))
        
        return jsonify({
            "status": "connected",
            "tools": tool_names,
            "count": len(current_tools)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message and call MCP tools"""
    global current_mcp_client, current_tools, current_contract_type
    
    if not current_mcp_client:
        return jsonify({"error": "Not connected to MCP server"}), 400
    
    data = request.json
    user_input = data.get('message', '').strip()
    
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    
    try:
        # Run async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def process():
            # Decide which tool to call
            decision = await decide_tool_call(user_input, current_tools, current_contract_type)
            
            if "error" in decision or decision.get("tool") == "none":
                return {
                    "user_input": user_input,
                    "response": decision.get("explanation", decision.get("error", "Could not process request")),
                    "success": False,
                    "tool_called": None
                }
            
            tool_name = decision.get("tool")
            args = decision.get("args", {})
            
            # Call the tool
            try:
                result = await current_mcp_client.call_tool(tool_name, args)
                return {
                    "user_input": user_input,
                    "tool_called": tool_name,
                    "arguments": args,
                    "response": str(result),
                    "success": True
                }
            except Exception as e:
                return {
                    "user_input": user_input,
                    "tool_called": tool_name,
                    "arguments": args,
                    "response": f"Error calling tool: {str(e)}",
                    "success": False
                }
        
        result = loop.run_until_complete(process())
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Get list of available tools"""
    if not current_mcp_client:
        return jsonify({"tools": [], "error": "Not connected"}), 400
    
    tool_info = []
    for t in current_tools:
        if hasattr(t, 'name'):
            name = t.name
            desc = t.description if hasattr(t, 'description') else ''
        else:
            name = t.get('name', 'unknown')
            desc = t.get('description', '')
        
        tool_info.append({"name": name, "description": desc})
    
    return jsonify({"tools": tool_info})


if __name__ == '__main__':
    import threading
    import time
    from werkzeug.serving import run_simple
    
    print("Starting Chatbot API Server...")
    print("Available endpoints:")
    print("  GET  /api/health          - Health check")
    print("  GET  /api/test            - Test endpoint")
    print("  POST /api/translate       - Translate contract PDF")
    print("  POST /api/connect         - Connect to MCP server")
    print("  POST /api/chat            - Send chat message")
    print("  GET  /api/tools           - List available tools")
    print("\nServer running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Set Flask to log output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    
    # Run server with logging enabled (blocking, so logs show)
    try:
        app.run(debug=False, port=5000, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        exit(0)
