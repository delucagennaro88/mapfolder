from file_manager import save_info
import json, os
import datetime, time

directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_directory = "C:\\Users\\Utente\\Desktop\\HD"

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

def open_json():
    movie_json= json.load(open('cinema.json'))

    for i in movie_json.values():
        for x in i:
            home_path = x['Home Directory']
            file_name = x['File Name']
            id = x['Id'] #nome del File senza Directory
            ext = x['Extension']
            atime = x['Atime']
            ctime = x['Ctime']
            size = x['Size']
            #folder_class = Folder(home_path, file_name, id, atime, ctime, size, ext)
            movie_id = x['Movie Id']
            movie_title = x['Movie Title']
            movie_url = x['Movie Url']
            movie_year = x['Movie Year']
            movie_plot = x['Movie plot']

            '''
            for y in x['Movie Director']:
                print(y['Name'])
                print(y['Id'])
                print('\n')
    
            for z in x['Movie Actor']:
                print(z['Name'])
                print(z['Id'])
                print('\n')
            '''
            #movie_class = Movie(folder_class, movie_id, movie_url, movie_title, movie_year, movie_plot, movie_director, movie_cast)
