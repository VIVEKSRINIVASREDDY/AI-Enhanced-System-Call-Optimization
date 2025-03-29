from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Simulated system calls
syscalls = ["open", "read", "write", "close", "execve"]

def generate_syscall():
    return random.choice(syscalls)

@app.route("/get_syscall", methods=["GET"])
def get_syscall():
    return jsonify({"syscall": generate_syscall()})

if __name__ == "__main__":
    app.run(debug=True)
