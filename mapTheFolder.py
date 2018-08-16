from file_manager import save_info
import csv
import json

directory = "C:\\Users\\Utente\\Desktop\\FILM"

# Qui comincia il programma

collection = save_info(directory)

#json_collection = json.dumps(collection, sort_keys=True)

#print(json_collection)

outfile = open( 'dict.csv', 'w' )
for key, value in sorted( collection.items() ):
    outfile.write( str(key) + '\t' + str(value) + '\n' )