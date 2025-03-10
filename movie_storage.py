import json

# Basic color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'
MOVIE_FILE = 'storageFiles/movies.json'

def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open(MOVIE_FILE, 'r') as movies_json:
        movies_dict = json.load(movies_json)
    return movies_dict


def set_movies(movies_dictionary):
    """
    function to override the movies.json file after change...
    """
    with open(MOVIE_FILE, 'w', encoding="utf8") as movies_json:
        json.dump(movies_dictionary, movies_json, indent=4)
