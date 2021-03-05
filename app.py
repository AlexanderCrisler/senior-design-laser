from flask import Flask, render_template, flash
import save_load

app = Flask(__name__)
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello_world():
    return render_template('start.html', result=all_items.keys())


@app.route('/add')
def adD_items():
    return render_template('add_item.html')

if __name__ == '___main___':
    app.run(debug=True)
