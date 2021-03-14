from flask import Flask, render_template
import save_load
app = Flask(__name__)
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')
#
# This should set the server name. I had some issues getting this to work
app.config['SERVER_NAME'] = 'localhost:5000'

@app.route('/')
def index():
    return render_template('index.html', result=all_items)
    
if __name__ == '__main__':

#adding the host='0.0.0.0' line makes flask run on all ip addresses currently on the computer.
    app.run(host='0.0.0.0', debug=True)
