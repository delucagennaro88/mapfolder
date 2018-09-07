import json
import os
import time

from bytes_converter import bytes_converter
from json_manager import createJsonFile, read_saved_files, updateJsonFile
from movie_manager import movie_name

collection = {}


def check_updates(dir, last_update):
    dir_box = []

    for i in os.listdir(dir):
        directory = os.path.join(dir, i)
        if last_update < os.stat(directory).st_mtime:
            dir_box.append(directory)
    return dir_box


def save_info(directory, last_update, update, json_dir):
    if os.path.exists(directory):
        num = 0
        if update == False:

            for i in os.listdir(directory):

                filename, file_extension = os.path.splitext(i)
                film = movie_name(filename)

                dir = os.path.join(directory, i)

                if os.path.isfile(dir):
                    ext = os.path.splitext(dir)[1]
                    size = bytes_converter(os.path.getsize(dir))

                elif os.path.isdir(dir):
                    ext = 'directory'  # qui andrebbe messa una funzione che apre la cartella e analizza i file interni
                    size = 0  # qui andrebbe messa una funzione che quantifica i file nella cartella

                else:
                    ext = 'unknown'
                    size = 0

                a = os.stat(os.path.join(directory, i))
                collection[filename] = []
                collection[filename].append(
                    {'Home Directory': directory, 'Id': i, 'File Name': dir, 'Atime': time.ctime(a.st_atime),
                     'Ctime': time.ctime(a.st_ctime), 'Size': size, 'Extension': ext, 'Movie Id': film['Id'],
                     'Movie Url': film['Url'], 'Movie Title': film['Title'], 'Movie Year': film['Year'],
                     'Movie plot': film['Plot'], 'Movie Director': film['DirectorBox'],
                     'Movie Actor': film['ActorBox']})
                num += 1

            with open(json_dir, 'w') as outfile:
                json.dump(collection, outfile, sort_keys=True, indent=4, ensure_ascii=False)

            createJsonFile(num)

        else:
            updated_folder = check_updates(directory, last_update)

            if not updated_folder:
                print('Lista vuota. Non ci sono aggiornamenti')
                return

            else:
                num = int(read_saved_files())

                for i in updated_folder:

                    dir = os.path.join(directory, i)

                    if os.path.isfile(dir):
                        ext = os.path.splitext(dir)[1]
                        size = bytes_converter(os.path.getsize(dir))

                    elif os.path.isdir(dir):
                        ext = 'directory'  # qui andrebbe messa una funzione che apre la cartella e analizza i file interni
                        size = 0  # qui andrebbe messa una funzione che quantifica i file nella cartella

                    else:
                        ext = 'unknown'
                        size = 0

                    a = os.stat(os.path.join(directory, i))

                    name_file = os.path.basename(i)
                    filename, file_extension = os.path.splitext(name_file)
                    film = movie_name(filename)

                    collection[filename] = []
                    collection[filename].append(
                        {'Home Directory': directory, 'Id': filename, 'File Name': i, 'Atime': time.ctime(a.st_atime),
                         'Ctime': time.ctime(a.st_ctime), 'Size': size, 'Extension': ext, 'Movie Id': film['Id'],
                         'Movie Url': film['Url'], 'Movie Title': film['Title'], 'Movie Year': film['Year'],
                         'Movie plot': film['Plot'], 'Movie Director': film['DirectorBox'],
                         'Movie Actor': film['ActorBox']})
                    num += 1

                with open(json_dir, 'r') as outfile:
                    data = json.load(outfile)

                data_str = str(data)
                no_brackets = data_str[
                              data_str.find("{") + 1:data_str.rfind("}")]  # ora non è un dizionario, ma una stringa

                # facciamo lo stesso con collection
                collection_str = str(collection)
                no_brackets_coll = collection_str[collection_str.find("{") + 1:collection_str.rfind("}")]

                # ora concateniamo le due stringhe
                new_str = '{' + no_brackets + ', ' + no_brackets_coll + '}'

                # qui ritorna dictionary
                dict1 = eval(new_str)

                with open(json_dir, 'w') as outfile:
                    json.dump(dict1, outfile, indent=4, ensure_ascii=False)

                updateJsonFile(num)

    else:
        print('Mi dispiace! La Directory non esiste...riprova')
