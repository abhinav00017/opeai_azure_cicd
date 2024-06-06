from flask import Flask, request, jsonify, render_template
from datetime import datetime
import time

from utils.settings import Settings
from utils.authenticate import Authenticate
from utils.assistant import Assistant

from utils.assistant_utils import Assistant_utils
from utils.function_utils import Function_utils

from db.records import Records


auth = Authenticate()
client = auth.get_client()
assistant = Assistant(client, Settings.ASSISTANT_ID)
assistant_utils = Assistant_utils(client, Settings.ASSISTANT_ID)
function_utils = Function_utils()
assistant_details = assistant.retrive_assistant()
records  = Records()

app = Flask(__name__)

emailid = "abhinavch53@gmail.com"

def first_thread():
    query = "hello"
    run, thread = assistant_utils.create_message_and_run(assistant_details, query)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(run.status)
    while run.status == "in_progress" or run.status == "queued":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return  thread.id,messages, query
    
    
# thread_id,messages,query = first_thread()
# latest_message = messages.data[0]
# text = latest_message.content[0].text.value

# # In-memory storage for simplicity
# threads = [{
#     'id': thread_id, 
#     'title': thread_id, 
#     'messages': [{'sender': 'User', 'content': query}, 
#                 {'sender': 'AI', 'content': text}]
#     }]
# print(threads)
global threads
threads = []
print(threads)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_threads', methods=['GET'])
def start_threads():
    global emailid
    user_thread_ids = records.retrieve_record(emailid)
    user_threads = []
    for i in user_thread_ids:
        user_threads.append({
            'id': i,
            'title': i,
        })
    return jsonify(user_threads)
    

@app.route('/threads', methods=['GET'])
def get_threads():
    return jsonify(threads)

# @app.route('/load_chat', methods=['GET','POST'])
def load_chat(thread_id):
    # thread_id = request.json.get('threadId')
    thread = client.beta.threads.messages.list(thread_id)
    print(thread)
    messages = []
    for message in thread.data:
        for content_block in message.content:
            messages.append({
                'id': message.id,
                'sender': message.role,
                'content': content_block.text.value
            })
    messages = messages[::-1]
    history = {
        'id': thread_id,
        'title': thread_id,
        'messages': messages
    }
    threads.append(history)
    print(threads)
    return jsonify(threads)

@app.route('/threads/<string:thread_id>', methods=['GET'])
def get_thread(thread_id):
    global threads
    thread = None
    print("one ",threads)
    if threads != []:
        thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread == None:
        load_chat(thread_id)
        print("two ",threads)
        thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread:
        return jsonify(thread)
    return jsonify({'error': 'Thread not found'}), 404

@app.route('/add_thread', methods=['POST','GET'])
def add_thread():
    thread_id,messages,query = first_thread()
    latest_message = messages.data[0]
    text = latest_message.content[0].text.value
    
    thread = {
    'id': thread_id, 
    'title': thread_id, 
    'messages': [{'sender': 'User', 'content': query}, 
                {'sender': 'assistant', 'content': text}]
    }
    
    user_data = records.retrieve_record(emailid)
    user_data.append(thread_id)
    records.create_record({emailid: user_data})
    
    # thread = {
    #     'id': len(threads) + 1,
    #     'title': 'Thread ' + str(len(threads) + 1) + ' - ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #     'messages': [
    #         {'sender': 'User', 'content': 'Hello'+ str(len(threads) + 1)},
    #         {'sender': 'AI', 'content': 'Hi there! How can I help you today?'+ str(len(threads) + 1)}
    #     ]
    # }
    threads.append(thread)
    print(threads)
    return jsonify(threads)

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    thread_id = request.json.get('threadId')
    response = generate_response(message, thread_id)
    for i in threads:
        if i['id'] == thread_id:
            i['messages'].append({'sender': 'User', 'content': message})
            i['messages'].append({'sender': 'assistant', 'content': response})
    # threads[thread_id]['messages'].append({'sender': 'User', 'content': message})
    # threads[thread_id]['messages'].append({'sender': 'AI', 'content': response})
    return jsonify({'response': response, 'threadId': thread_id})
            

def generate_response(message,thread_id):
    # Placeholder AI response logic
    
    thread = client.beta.threads.retrieve(thread_id) 
    
    run, thread = assistant_utils.create_message_and_run(assistant_details, message, thread)
    
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    print(run.status)
    while run.status == "in_progress" or run.status == "queued":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
    if run.status=="completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]
        text = latest_message.content[0].text.value
        print("User : ",message)
        print("assistant: ", text)
        user_input = message
        time.sleep(1)
        return text
    print(run.status)
    
    
    if run.status == "requires_action":
        function_name, arguments, function_id = assistant_utils.get_function_details(run)
        print(function_name, arguments, function_id)
        function_response = function_utils.execute_function_call(function_name, arguments)
        run = assistant_utils.submit_tool_outputs(run, thread, function_id, function_response)
        print(run.status)
        while run.status == "queued" or run.status == "in_progress" or run.status == "requires_action":
            if run.status == "requires_action":
                function_name, arguments, function_id = assistant_utils.get_function_details(run)
                print(function_name, arguments, function_id)
                function_response = function_utils.execute_function_call(function_name, arguments)
                run = assistant_utils.submit_tool_outputs(run, thread, function_id, function_response)
            print(run.status)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run.status)
        if run.status=="completed":
            print(run.status)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            print("User : ",message)
            print("assistant: ", text)
            user_input = message
            time.sleep(1)
            return text
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]
        text = latest_message.content[0].text.value
        print("User : ",message)
        print("assistant: ", text)
        user_input = message
        time.sleep(1)
        return text
    return f"You said: {message}"

if __name__ == '__main__':
    app.run(port=5000,debug=False)
