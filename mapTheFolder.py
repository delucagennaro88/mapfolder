from file_manager import save_info
import json, os, datetime
from flask import Flask, flash, url_for, redirect, render_template
from json_manager import open_json

directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_directory = "C:\\Users\\Utente\\Dropbox\\Map the Movie"

json_file = "cinema.json"
json_dir = os.path.join(json_directory, json_file)

def start():
    if not os.path.exists(json_dir):
        update = False
        print('Il file non esiste!')
        last_update = datetime.datetime.now()
        save_info(directory, last_update, update, json_dir)

    else:
        update = True
        print('Il file esiste!')

        file_modified = os.stat(json_dir).st_mtime
        save_info(directory, file_modified, update, json_dir)

# Qui comincia il programma

app = Flask(__name__)

start()

data_collection = open_json(json_dir)

data = data_collection.values()

@app.route('/')
def show_all():
    return render_template('show_all.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)


