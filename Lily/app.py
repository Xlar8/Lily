from flask import Flask, render_template, request, jsonify
import subprocess
import webbrowser
import threading
import time

app = Flask(__name__)

# Initialize global variables to store conversation history and process state
conversation_history = []

def run_lily(query):
    try:
        # Start the Lily model process
        process = subprocess.Popen(
            ['ollama', 'run', 'lily', query],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Communicate with the process
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return {'error': 'Error occurred during subprocess execution.'}
        
        return {'response': stdout}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html', history=conversation_history)

@app.route('/query', methods=['POST'])
def query():
    global conversation_history
    user_input = request.form['input']
    conversation_history.append({'user': user_input})
    
    result = run_lily(user_input)
    if 'response' in result:
        conversation_history.append({'bot': result['response']})
    
    return jsonify({'response': result.get('response', 'Error occurred.')})

@app.route('/stop', methods=['POST'])
def stop():
    # No process to stop as subprocess is handled synchronously
    return jsonify({'response': 'No process to stop. Lily processes run synchronously.'})

def open_browser():
    time.sleep(1)  # Sleep for a second to ensure the server has started
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start a thread to open the browser
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
