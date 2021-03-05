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

@app.route('/selected_index', methods=["POST"])
def get_item():
    req = request.get_json()
    current_selection = req['name'].strip()
    response = make_response(jsonify(all_items[current_selection]), 200)
    return response

@app.route('/add/submit', methods=['POST'])
def submit_add_item():
    req = request.get_json()
    temp_dictionary = {"horizontal": req['horizontal'], "vertical": req['vertical']}
    print(req['name'])
    all_items[req['name']] = temp_dictionary

if __name__ == '___main___':
    app.run(debug=True)
