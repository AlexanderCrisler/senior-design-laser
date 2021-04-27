import save_load
from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
from maestro_controller import LaserSystem
import time
import os

try:
    if 'phidgets_ctlr' not in globals():
        phidgets_ctlr = LaserSystem()
except:
    print("No phidget detected, will run headless")

app = Flask(__name__)
AppPath=os.path.dirname(os.path.abspath(__file__))
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name=AppPath +'/master_save_file')
current_selection = ""
blank_item = {'name': ''}
# This should set the server name. I had some issues getting this to work
#app.config['SERVER_NAME'] = 'localhost:5000'

@app.route('/')
def index():
    return render_template('index.html', result=all_items.keys())

@app.route('/add')
def add_items():
    return render_template('add_item.html')

@app.route('/selected_index', methods=["POST"])
def selected_index():
    req = request.get_json()
    current_selection = req['name'].strip()
    current_selection = all_items[current_selection]

    phidgets_ctlr.set_position(current_selection['horizontal'], current_selection['vertical'])
    response = jsonify(current_selection)
    return response

@app.route('/add/submit', methods=['POST'])
def submit_add_item():
    req = request.get_json()
    current_angle = phidgets_ctlr.get_target_position()
    temp_dictionary = {"horizontal": current_angle[0], "vertical": current_angle[1]}
    temp_dictionary['description'] = request.form['itemDescription']
    try:
        image_filename = request.files['image_upload'].filename
    except Exception as e:
        print(e)
        file_path = "static\images\default.jpg"
    else:
        file_path = os.path.join('static', 'images', image_filename)
        if os.path.exists(file_path):
            i = 1
            extension_loc = file_path.find('.')
            while os.path.exists(f"{file_path[:extension_loc]}_{i}{file_path[extension_loc:]}"):
                i = i + 1
            file_path = f"{file_path[:extension_loc]}_{i}{file_path[extension_loc:]}"
        request.files['image_upload'].save(file_path)
    temp_dictionary['image_file'] = file_path
    all_items[request.form['itemName']] = temp_dictionary
    start_menu.save(items=all_items, file_name=AppPath +'/master_save_file')
    return redirect(url_for('add_items'))

@app.route('/add/key_press', methods=["POST"])
def key_press():
    req = request.get_json()
    print(req, flush=True)
    if (req == 39):
        phidgets_ctlr.right_button_click()
    elif (req == 40):
        phidgets_ctlr.down_button_click()
    elif (req == 37):
        phidgets_ctlr.left_button_click()
    elif (req == 38):
        phidgets_ctlr.up_button_click()
    response = req
    return jsonify(response)

@app.route('/delete', methods=['POST'])
def delete_item():
    req = request.get_json()
    #print(req, flush=True)
    #print(all_items[req['name']].strip())
    popped = all_items.pop(req['name'].strip(), None)
    os.remove(popped['image_file'])
    response = make_response(jsonify({'return': None}), 200 if popped == 1 else 100)
    start_menu.save(items=all_items, file_name=AppPath +'/master_save_file')
    return response

@app.route('/get_all_items', methods=['GET'])
def return_all_items():
    response = make_response(jsonify(list(all_items.keys()), 200))
    #response = make_response(jsonify([1,2,3,4,5]), 200)
    return response

if __name__ == '__main__':
    #adding the host='0.0.0.0' line makes flask run on all ip addresses currently on the computer.
    app.run(host='0.0.0.0', debug=True)
