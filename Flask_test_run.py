from flask import Flask, render_template
import save_load
app = Flask(__name__)
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')


@app.route('/')
def index():
    return render_template('index.html', result=all_items)
    
if __name__ == '__main__':
    app.run(debug=True)
