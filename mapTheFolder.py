from file_manager import save_info
import json, os, datetime

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

start()

