import save_load
from flask import Flask, render_template, request, make_response, jsonify
from gpio_controller import LaserSystem

app = Flask(__name__)
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')
current_selection = ""
blank_item = {'name': ''}

try:
    phidgets_ctlr = LaserSystem()
except:
    print("No phidget detected, will run headless")

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

@app.route('/key_press', methods=["POST"])
def key_press():
    req = request.get_json()

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


if __name__ == '__main__':
    app.run(debug=True)