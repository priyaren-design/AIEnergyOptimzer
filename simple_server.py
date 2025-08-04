#!/usr/bin/env python3
"""
Simple AI Energy Optimizer Server
Works with basic Python libraries to avoid dependency issues
"""

import json
import random
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

# Global device storage
DEVICES = [
    {
        "device_id": "thermostat_001",
        "device_name": "Living Room Thermostat",
        "device_type": "thermostat",
        "current_power": 2.5,
        "location": "living_room",
        "is_active": True
    },
    {
        "device_id": "lighting_001",
        "device_name": "Kitchen Lighting",
        "device_type": "lighting",
        "current_power": 0.8,
        "location": "kitchen",
        "is_active": True
    },
    {
        "device_id": "hvac_001",
        "device_name": "HVAC System",
        "device_type": "hvac",
        "current_power": 4.2,
        "location": "basement",
        "is_active": True
    },
    {
        "device_id": "appliance_001",
        "device_name": "Kitchen Appliance",
        "device_type": "appliances",
        "current_power": 1.5,
        "location": "kitchen",
        "is_active": True
    }
]

def generate_device_id(device_name):
    """Generate a unique device ID from device name"""
    import re
    # Convert to lowercase and replace spaces with underscores
    device_id = re.sub(r'[^a-zA-Z0-9]', '_', device_name.lower())
    # Remove multiple underscores
    device_id = re.sub(r'_+', '_', device_id)
    # Remove leading/trailing underscores
    device_id = device_id.strip('_')
    # Add timestamp to ensure uniqueness
    timestamp = str(int(time.time()))[-6:]
    return f"{device_id}_{timestamp}"

class EnergyOptimizerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the AI Energy Optimizer"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "AI Energy Optimizer API",
                "status": "running",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/predictions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generate energy predictions
            predictions = []
            current_time = datetime.now()
            
            for i in range(24):
                future_time = current_time + timedelta(hours=i)
                predicted_usage = 2.5 + random.uniform(-0.5, 0.5)
                confidence = 0.85 + random.uniform(-0.05, 0.05)
                
                predictions.append({
                    'timestamp': future_time.isoformat(),
                    'predicted_usage': round(predicted_usage, 2),
                    'confidence': round(confidence, 2)
                })
            
            total_usage = sum(p['predicted_usage'] for p in predictions)
            avg_confidence = sum(p['confidence'] for p in predictions) / len(predictions)
            
            response = {
                "predictions": predictions,
                "total_predicted_usage": round(total_usage, 2),
                "average_confidence": round(avg_confidence, 2)
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/devices/sample':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"devices": DEVICES}
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/analytics/summary':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            analytics = {
                "average_daily_usage": round(random.uniform(50, 80), 2),
                "peak_usage": round(random.uniform(4, 6), 2),
                "min_usage": round(random.uniform(1, 2), 2),
                "peak_hours_count": random.randint(4, 8),
                "efficiency_score": round(random.uniform(70, 90), 1),
                "prediction_confidence": round(random.uniform(0.8, 0.95), 2)
            }
            
            self.wfile.write(json.dumps(analytics).encode())
            
        elif path == '/frontend/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read the frontend HTML file
            try:
                with open('frontend/index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write(b"Frontend file not found")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/optimize':
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generate optimization recommendations
            recommendations = []
            current_usage = 3.0
            
            device_types = ['thermostat', 'lighting', 'hvac', 'appliances']
            actions = {
                'thermostat': ['lower_temp', 'schedule_optimization', 'eco_mode'],
                'lighting': ['dim_lights', 'motion_sensors', 'led_upgrade'],
                'hvac': ['zone_control', 'maintenance', 'smart_scheduling'],
                'appliances': ['delay_operation', 'eco_mode', 'power_management']
            }
            
            for device_type in device_types:
                for action in actions[device_type]:
                    savings = random.uniform(0.1, 0.5)
                    recommendations.append({
                        'device_id': f"{device_type}_001",
                        'recommended_action': action,
                        'expected_savings': round(savings, 2),
                        'priority': 'high' if savings > 0.3 else 'medium'
                    })
            
            total_savings = sum(r['expected_savings'] for r in recommendations)
            savings_percentage = (total_savings / current_usage) * 100
            
            response = {
                "recommendations": recommendations,
                "total_potential_savings": round(total_savings, 2),
                "savings_percentage": round(savings_percentage, 1),
                "current_usage": round(current_usage, 2)
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/devices/add':
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            device_data = json.loads(post_data.decode('utf-8'))
            
            # Generate unique device ID
            device_id = generate_device_id(device_data.get('device_name', 'new_device'))
            
            # Create new device
            new_device = {
                "device_id": device_id,
                "device_name": device_data.get('device_name', 'New Device'),
                "device_type": device_data.get('device_type', 'other'),
                "current_power": float(device_data.get('power_rating', 1.0)),
                "location": device_data.get('location', 'unknown'),
                "is_active": device_data.get('is_active', True)
            }
            
            # Add to global storage
            DEVICES.append(new_device)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "message": "Device added successfully",
                "device": new_device
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/devices/delete':
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            delete_data = json.loads(post_data.decode('utf-8'))
            
            device_id = delete_data.get('device_id')
            
            # Find and remove device
            original_length = len(DEVICES)
            DEVICES[:] = [device for device in DEVICES if device['device_id'] != device_id]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if len(DEVICES) < original_length:
                response = {
                    "success": True,
                    "message": "Device deleted successfully"
                }
            else:
                response = {
                    "success": False,
                    "message": "Device not found"
                }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/devices/toggle':
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            toggle_data = json.loads(post_data.decode('utf-8'))
            
            device_id = toggle_data.get('device_id')
            
            # Find and toggle device
            for device in DEVICES:
                if device['device_id'] == device_id:
                    device['is_active'] = not device['is_active']
                    break
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "message": "Device toggled successfully"
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def open_browser():
    """Open the frontend in a web browser"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8000/frontend/index.html')
        print("🌐 Frontend opened in browser")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("Please open: http://localhost:8000/frontend/index.html")

def main():
    """Main function to start the server"""
    print("=" * 60)
    print("🔋 AI Energy Optimizer - Simple Server")
    print("=" * 60)
    print()
    
    # Start browser thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, EnergyOptimizerHandler)
    
    print("🚀 Starting AI Energy Optimizer Server...")
    print("📍 Server running on: http://localhost:8000")
    print("🌐 Frontend: http://localhost:8000/frontend/index.html")
    print("📊 API Health: http://localhost:8000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    main() 