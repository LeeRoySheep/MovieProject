from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson
from sys import argv
import os
import json


def main():
    """
    starting program with database file given in sys.argv
    :return:
    """
    if len(argv) == 2:
        file = argv[1].split(".")
        if file[1]:
            if file[1] == 'json':
                file_path = f"storageFiles/{argv[1]}"
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf8") as file_writer:
                        json.dump({}, file_writer, indent=4)
                this_app = MovieApp(StorageJson(file_path))
                this_app.run()
            elif file[1] == 'csv':
                file_path = f"storageFiles/{argv[1]}"
                if not os.path.exists(file_path):
                    open(file_path, 'w', encoding="utf8").close()
                this_app = MovieApp(StorageCsv(file_path))
                this_app.run()
            else:
                print("Wrong file format! Please try again")
        else:
            print("Input Error! Please try again.")
    else:
        print("No argument passed! Please add argument for movie data.")

if __name__ == "__main__":
    main()