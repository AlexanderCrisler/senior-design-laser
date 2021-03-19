import save_load
from flask import Flask, render_template, request, make_response, jsonify

app = Flask(__name__)
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
current_selection = ""
blank_item = {'name': ''}



@app.route('/')
def hello_world():
    return render_template('index.html', result=all_items.keys())


@app.route('/add')
def add_items():
    return render_template('add_item.html')

@app.route('/selected_index', methods=['POST'])
def get_item():
    req = request.get_json()
    print(req, flush=True)
    current_selection = req['name'].strip()
    response = make_response(jsonify(all_items[current_selection]), 200)
    return response

@app.route('/add/submit', methods=['POST'])
def submit_add_item():
    req = request.get_json()
    temp_dictionary = {"horizontal": req['horizontal'], "vertical": req['vertical']}
    all_items[req['name']] = temp_dictionary
    response = make_response(jsonify({'return': None}), 200)
    return response

@app.route('/delete', methods=['POST'])
def delete_item():
    req = request.get_json()
    #print(req, flush=True)
    #print(all_items[req['name']].strip())
    popped = all_items.pop(req['name'].strip(), None)
    response = make_response(jsonify({'return': None}), 200 if popped == 1 else 100)
    return response

@app.route('/get_all_items', methods=['GET'])
def return_all_items():
    response = make_response(jsonify(list(all_items.keys()), 200))
    #response = make_response(jsonify([1,2,3,4,5]), 200)
    return response


if __name__ == '___main___':
    app.run(debug=True, use_reloader=True)
