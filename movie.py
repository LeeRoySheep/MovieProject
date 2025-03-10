import movie_storage
import random
import statistics

# Basic color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'
THIS_YEAR = 2025


def get_title(prompt):
    """
    function to check if title is not empty
    """
    title_input = input(prompt)
    if title_input == "":
        raise NameError("Title must not be empty!")
    else:
        return title_input


def get_year(prompt):
    """
    function to get a 4 digit number and returns it as int
    raises ValueError for wrong input
    """
    input_year = int(input(prompt))
    if input_year < 1900 or input_year > THIS_YEAR:
        raise ValueError("Year must be in between 1900 and {THIS_YEAR}")
    else:
        return input_year


def get_rating(prompt):
    """
    function that gets input from user and returns rating as
    float between 0 and 10 or raises ValueError
    """
    input_rating = float(input(prompt))
    if 0.0 > input_rating or input_rating > 10.0:
        raise ValueError(f"{RED}Ratings must be float number within 0 and 10{RESET}")
    else:
        return input_rating


def list_movies():
    """
    prints a list of all movies in the given database
    """
    movies = movie_storage.get_movies()



def add_movie(title='', year='', rating=''):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = movie_storage.get_movies()
    while True:
        try:
            if title == '':
                title = get_title('Enter new movie name: ')
            if type(year) != int:
                year = get_year('Enter new movie year: ')
            rating = get_rating('Enter new movie rating: ')
            break
        except ValueError as e:
            print(e)
        except NameError as empty_title:
            print(f'{RED}', empty_title, f'{RESET}')
    if title not in movies:
        movies[title] = {"rating": rating, "year": year}
        movie_storage.set_movies(movies)
        print(f'Movie {title} successfully added')
    else:
        print(f'Sorry the movie {title} already exists!')


def delete_movie(title=''):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    while True:
        try:
            title = get_title('Enter movie name to delete: ')
            break
        except NameError as empty_title:
            print(f'{RED}{empty_title}{RESET}')
    movies = movie_storage.get_movies()
    if title in movies:
        del movies[title]
        movie_storage.set_movies(movies)
        print(f'Movie {title} successfully deleted')
    else:
        print(f"The movie {title} doesn't exist!")


def update_movie(title='', rating=''):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = movie_storage.get_movies()
    title = input("Enter movie name: ")
    if title in movies:
        while True:
            try:
                rating = get_rating('Enter new movie rating: ')
                break
            except ValueError as value_exception:
                print(value_exception)
        movies[title]["rating"] = rating
        movie_storage.set_movies(movies)
        print(f"Movie {title} successfully updated")
    else:
        print(f"Movie {title} doesn't exist!")


def calc_avrg(movies_dict):
    """
    method to calculate avarage value
    """
    avrg_rate = 0
    for value_dictionary in movies_dict.values():
        avrg_rate += value_dictionary["rating"]
    return avrg_rate / len(movies_dict)


def similar_val(val, movies_dict):
    """
    method to create list of movies with similar values
    """
    similars = {}
    for key in movies_dict:
        if movies_dict[key]["rating"] == val:
            similars[key] = val
    return similars


def movie_stats():
    """
    method to create stats of the movie list
    """
    movies = movie_storage.get_movies()
    avrg_rate = calc_avrg(movies)
    median_rate = statistics.median([value_dictionary["rating"] for value_dictionary in movies.values()])
    best = max([value_dictionary["rating"] for value_dictionary in movies.values()])
    best_movies = similar_val(best, movies)
    worst = min([value_dictionary["rating"] for value_dictionary in movies.values()])
    worst_movies = similar_val(worst, movies)
    print(f'Avarage rating: {"%.1f" % avrg_rate}')
    print(f'Median rating: {"%.1f" % median_rate}')
    if len(best_movies) > 1:
        print(f'The best movies with a rating of {best} are:')
        for key in best_movies:
            print(key)
    else:
        for title, rating in best_movies.items():
            print(f'Best movie: {title}, {rating}')
    if len(worst_movies) > 1:
        print(f'The worst movies with a rating of {worst} are:')
        for key in worst_movies:
            print(key)
    else:
        for title, rating in worst_movies.items():
            print(f'Worst movie: {title}, {rating}')


def rand_movie():
    """
    method to cal a random movie from Dictionary
    """
    movies = movie_storage.get_movies()
    key_list = []
    for key in movies:
        key_list.append(key)
    rand_num = random.randrange(len(movies) - 1)
    print(f"Your movie for tonight: {key_list[rand_num]}, it's rated {movies[key_list[rand_num]]['rating']}")


def levenshtein_dist(string1, string2):
    """
    function to calculate levenshtein distance between 2 strings
    """
    length1, length2 = len(string1), len(string2)
    # swap strings in case string2 is bigger to simplify calculations
    if length1 < length2:
        string1, string2 = string2, string1
        length1, length2 = length2, length1
    distance = [list(range(length2 + 1))] + [[i] + [0] * length2 for i in range(1, length1 + 1)]
    for j in range(1, length2 + 1):
        for i in range(1, length1 + 1):
            if string1[i - 1] == string2[j - 1]:
                distance[i][j] = distance[i - 1][j - 1]
            else:
                distance[i][j] = min(distance[i - 1][j], distance[i][j - 1], distance[i - 1][j - 1]) + 1
    return distance[length1][length2]


def similarity(input_string, reference_string):
    """
    function returns distance between 2 strings with levenstein_distance
    """
    distance = levenshtein_dist(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity


def search_movie():
    """
    method to search a movie in the json file
    """
    search_string = input(f'{GREEN}Enter part of movie name: {RESET}')
    print()
    found = False
    movies = movie_storage.get_movies()
    distant_movies = []
    for key in movies:
        if search_string.lower() == key.lower():
            print(f'{key}, {movies[key]["rating"]}')
            found = True
        elif similarity(search_string.lower(), key.lower()) > 0.21:
            distant_movies.append(key)
    if not found:
        if distant_movies != []:
            print(f'The movie "{search_string}" does not exist. Did you mean: ')
            for movie in distant_movies:
                print(movie)
        else:
            print(f'{RED}Sorry no movie found{RESET}')


def sorted_movies(sorting_value, order=True, movies_dict=movie_storage.get_movies()):
    """
    function so print movies sorted by rating in descending order
    """
    if sorting_value == "year":
        input_order = input("Please enter if c if you want to keep the chronological order or anything else if not: ")
        other_val = 'rating'
        if input_order != "c":
            order = False
    else:
        other_val = 'year'
    sortedDict = dict(sorted(movies_dict.items(), key=lambda x: x[1][sorting_value], reverse=order))
    for key in sortedDict:
        print(
            f'{key} with {sorting_value}: {sortedDict[key][sorting_value]} and {other_val}: {sortedDict[key][other_val]}')


def filter_movies(min_rating=0, min_year=1900, max_year=THIS_YEAR):
    """
    filter function to print filtered movie list depending on user input
    """
    try:
        min_rating = get_rating("Enter minimum rating (leave blank for no minimum rating): ")
    except ValueError as value_error:
        print("Minimum rating set to default!")
    try:
        min_year = get_year("Enter start year (leave blank for no start year): ")
    except ValueError as value_error:
        print("Minimum year set to default!")
    try:
        max_year = get_year("Enter end year (leave blank for no end year): ")
    except ValueError as value_error:
        print("Maximum year set to default")
    print()
    filtered_movies_dict = {
        key: value_dict for key, value_dict in movie_storage.get_movies().items()
        if value_dict["rating"] >= min_rating and value_dict["year"] >= min_year
           and value_dict["year"] <= max_year}
    print("Filtered Movies:")
    for title, values in filtered_movies_dict.items():
        print(f'{title} ({values["year"]}): {values["rating"]}')


def menu_choice(prompt):
    menu_choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    input_string = input(prompt)
    if input_string not in menu_choices:
        raise ValueError(f"{RED}Choice must be a digit within 0 and 10{RESET}")
    else:
        return input_string


def print_menu():
    """
    Method to print a prompt with a menu for a user to choose from
    """
    print(f"{BLUE}", end="")
    print('*' * 10, " Lee-Roy's Movies Database ", '*' * 10)
    print()
    print('Menu:')
    print('0. Exit')
    print('1. List movies')
    print('2. Add movie')
    print('3. Delete movie')
    print('4. Update movie')
    print('5. Stats')
    print('6. Random movie')
    print('7. Search movie')
    print('8. Movies sorted by rating')
    print('9. Movies sorted by year')
    print(f'10. Filter movies{RESET}')
    print()


def main():
    """
    main function to use all functions via input prompt form user
    """
    function_dictionary = {
        '0': exit,
        '1': list_movies,
        '2': add_movie,
        '3': delete_movie,
        '4': update_movie,
        '5': movie_stats,
        '6': rand_movie,
        '7': search_movie,
        '8': sorted_movies,
        '9': sorted_movies,
        '10': filter_movies
    }
    while True:
        try:
            print_menu()
            user_input = menu_choice(f'{GREEN}Enter choice (0-10): {RESET}')
            break
        except ValueError as wrongchoice:
            print(wrongchoice)
    print()
    while user_input != '0':
        if user_input == '8':
            function_dictionary[user_input]('rating')
        elif user_input == '9':
            function_dictionary[user_input]('year')
        else:
            function_dictionary[user_input]()
        print()
        input("Hit any key to continue! ")
        print()
        while True:
            try:
                print_menu()
                user_input = menu_choice(f'{GREEN}Enter choice (0-10): {RESET}')
                break
            except ValueError as wrongchoice:
                print(wrongchoice)
    print('Bye!')


if __name__ == '__main__':
    main()
