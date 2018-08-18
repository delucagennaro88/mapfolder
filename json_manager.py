import os, json

json_directory = "C:\\Users\\Utente\\Desktop\\HD"
json_data = "data.json"
json_data_dir = os.path.join(json_directory, json_data)

# create Json File for NR. of saved files
def createJsonFile(data_saved):
    json_dic = {'Directory': json_data_dir, 'Saved Files': data_saved}
    with open(json_data_dir, 'a') as outfile:
        json.dump(json_dic, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print('Creato il file')

# read Json File with NR. of saved files
def read_saved_files():
    jsonFile = open(json_data_dir, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    tmp = data["Saved Files"]
    print('Letto il file')

    return tmp

# update Json File with NR. of saved files
def updateJsonFile(num):
    jsonFile = open(json_data_dir, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    ## Working with buffered content
    tmp = data["Saved Files"]
    data["Saved Files"] = num

    ## Save our changes to JSON file
    jsonFile = open(json_data_dir, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

    print("Aggiornato il file")