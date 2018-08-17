from file_manager import save_info
import json, os
from Folder import Folder
from Movie import Movie

directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_file = 'cinema.json'

json_dir = os.path.join(directory, json_file)
# Qui comincia il programma

if not os.path.exists(directory):
    print('Il file non esiste!')
    collection = save_info(directory)

    with open('cinema.json', 'w') as outfile:
        json.dump(collection, outfile, sort_keys=True, indent=4, ensure_ascii=False)

else:
    print('Il file esiste!')
    #creare funzione save_info_lite() che verifica gli aggiornamenti rispetto all'ultima versione
    #e inserisce solo quelli
    #il file json deve essere solo aggiornato

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
