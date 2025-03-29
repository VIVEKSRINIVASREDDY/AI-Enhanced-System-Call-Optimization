from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time
import psutil
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store syscall data
current_syscall = "read"
syscall_count = 0
optimized_count = 0
performance_gain = 0.0
is_running = True  # Control flag for simulation

def get_random_syscall():
    """Generate a random system call for demonstration"""
    syscalls = [
        "read", "write", "open", "close", "fork", "execve", "waitpid",
        "socket", "connect", "accept", "bind", "listen", "mmap", "munmap",
        "brk", "ioctl", "fcntl", "stat", "fstat", "lstat", "access"
    ]
    return random.choice(syscalls)

def simulate_syscall_optimization():
    """Simulate syscall optimization in the background"""
    global current_syscall, syscall_count, optimized_count, performance_gain, is_running
    
    while True:
        if not is_running:
            time.sleep(1)
            continue
            
        # Simulate new syscall
        current_syscall = get_random_syscall()
        syscall_count += 1
        
        # Simulate optimization (random chance)
        if random.random() < 0.7:  # 70% chance of optimization
            optimized_count += 1
            performance_gain = random.uniform(10.0, 35.0)
        
        time.sleep(1)  # Update every second

@app.route('/get_syscall')
def get_syscall():
    """Endpoint to get current syscall data"""
    return jsonify({
        'syscall': current_syscall,
        'total_syscalls': syscall_count,
        'optimized_count': optimized_count,
        'performance_gain': round(performance_gain, 1),
        'is_running': is_running
    })

@app.route('/control', methods=['POST'])
def control_simulation():
    """Endpoint to control the simulation"""
    global is_running
    data = request.get_json()
    action = data.get('action')
    
    if action == 'stop':
        is_running = False
    elif action == 'start':
        is_running = True
    
    return jsonify({'status': 'success', 'is_running': is_running})

@app.route('/system_stats')
def get_system_stats():
    """Endpoint to get system statistics"""
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        'cpu_usage': cpu_percent,
        'memory_usage': memory.percent,
        'disk_usage': disk.percent
    })

if __name__ == '__main__':
    # Start the background thread for syscall simulation
    simulation_thread = threading.Thread(target=simulate_syscall_optimization, daemon=True)
    simulation_thread.start()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000) 