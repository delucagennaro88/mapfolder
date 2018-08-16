from file_manager import save_info
import csv

directory = "C:\\Users\\Utente\\Desktop\\FILM"

# Qui comincia il programma

collection = save_info(directory)

with open('thefile.csv', 'w') as f:

    fnames = ['home_path', 'name', 'dir', 'atime', 'ctime', 'size', 'ext', 'id', 'url', 'title', 'plot', 'director_name', 'director_id', 'actor_name', 'actor_id']  # qui vanno i nomi delle colonne
    writer = csv.DictWriter(f, fieldnames=fnames)

    writer.writeheader()

    for i in collection:
        d = i.director_box
        writer.writerow({'home_path': i.home_path, 'name': i.name, 'dir': i.dir, 'atime': str(i.atime), 'ctime': str(i.ctime), 'id': str(i.id), 'url': i.url, 'title': i.title, 'plot': i.plot, 'director_name': ([y.name for y in i.director_box]), 'director_id': ([y.id for y in i.director_box]), 'actor_name': ([x.name for x in i.actor_box]), 'actor_id': ([x.id for x in i.actor_box]),})

'''
        for y in i.director_box:
            writer.writerow({'director_id': str(y.id), 'director_name': y.name})
        for x in i.actor_box:
            writer.writerow({'actor_id': str(x.id), 'actor_name': x.name})
'''