import statistics
import random
import storage_csv
from storage_json import StorageJson
import requests
import os
from dotenv import load_dotenv
import pycountry
import json

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Basic color codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'
# Constant variables
THIS_YEAR = 2025

class MovieApp:
    """creating a movie app class which handles the front end of the program"""
    def __init__(self, storage):
        self._storage = storage


    @property
    def storage(self):
        """
        property for class variable _storage
        :return: self._storage
        """
        return self._storage


    @storage.setter
    def storage(self, new_storage):
        """ setter for class variable _storage"""
        self._storage = new_storage


#-----------Print List of movies in stortage------------------------------
    def _command_list_movies(self):
        """
        prints all movies to terminal
        :return: None
        """
        movies = self.storage.movies
        print(f"A list of {len(movies)} in the given storage.")
        for movie_name, movie_dict in movies.items():
            print(f"{movie_name} ({movie_dict["year"]}): {movie_dict["rating"]}")


#----------------add, delete or update movie----------------
    def get_title(self, prompt):
        """
        function to check if title is not empty
        """
        title_input = input(prompt)
        if title_input == "":
            raise NameError("Title must not be empty!")
        else:
            return title_input


    def get_year(self, prompt):
        """
        function to get a 4 digit number and returns it as int
        raises ValueError for wrong input
        """
        input_year = int(input(prompt))
        if input_year < 1900 or input_year > THIS_YEAR:
            raise ValueError("Year must be in between 1900 and {THIS_YEAR}")
        else:
            return input_year


    def get_rating(self, prompt):
        """
        function that gets input from user and returns rating as
        float between 0 and 10 or raises ValueError
        """
        input_rating = float(input(prompt))
        if 0.0 > input_rating or input_rating > 10.0:
            raise ValueError(f"{RED}Ratings must be float number within 0 and 10{RESET}")
        else:
            return input_rating


    def _command_add_movie(self):
        """
        Adds a movie to the movies database.
        Loads the information from storage, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.storage.movies
        while True:
            try:
                title = self.get_title('Enter new movie name: ')
                if not title in movies.keys():
                    request = requests.get(
                        "http://www.omdbapi.com/?apikey="
                        f"{API_KEY}&t={title.replace(" ","+")}",
                        timeout=15
                    )
                    if request.json()["Response"] == "True":
                        year = request.json()["Year"]
                        rating = float(request.json()["imdbRating"])
                        poster = request.json()["Poster"]
                        self.storage.add_movie(title, year, rating, poster)
                        print(f'Movie {title} successfully added')
                    elif request.json()["Response"] == "False":
                        print(f"{RED}Movie {title} does not exist!{RESET}")
                else:
                    print(f'Sorry the movie {title} already in storage!')
                break
            except ValueError as e:
                print(e)
            except NameError as empty_title:
                print(f'{RED}', empty_title, f'{RESET}')
            except requests.exceptions.ConnectionError as conn_err:
                if "q" == input("Sorry no connection to server.To abort program enter q: "):
                    exit()



    def _command_delete_movie(self):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        while True:
            try:
                title = self.get_title('Enter movie name to delete: ')
                break
            except NameError as empty_title:
                print(f'{RED}{empty_title}{RESET}')
        try:
            self.storage.delete_movie(title)
            print(f'{title} successfully deleted')
        except ValueError as value_err:
            print(value_err)


    def _command_update_movie(self):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        while True:
            try:
                title = input("Enter movie name: ")
                note = self.get_title('Enter a note: ')
                break
            except ValueError as value_exception:
                print(value_exception)
        try:
            self.storage.update_movie(title, note)
            print(f"Movie {title} successfully updated")
        except ValueError as value_exception:
            print(value_exception)


#-------------STATISTICS handling----------------------------------
    def calc_avrg(self, movies_dict):
        """
        method to calculate avarage value by rating
        """
        avrg_rate = 0
        for value_dictionary in movies_dict.values():
            avrg_rate += value_dictionary["rating"] / len(movies_dict)
        return avrg_rate


    def similar_val(self, val, movies_dict):
        """
        method to create list of movies with similar values
        """
        similars = {}
        for key in movies_dict:
            if movies_dict[key]["rating"] == val:
                similars[key] = val
        return similars


    def print_movie_stats(self, avrg, median, best, bests, worst, worsts):
        """
        creates a prompt in Terminal showing all given values and movies
        :param avrg: average movie value
        :param median: median movie value
        :param bests: list of best movies with rating best["rating"]
        :param worsts: list of worst movies just like best
        :return:
        """
        print(f'Avarage rating: {"%.1f" % avrg}')
        print(f'Median rating: {"%.1f" % median}')
        if len(bests) > 1:
            print(f'The best movies with a rating of {best} are:')
            for key in bests:
                print(key)
        else:
            for title, rating in bests.items():
                print(f'Best movie: {title}, {rating}')
        if len(worsts) > 1:
            print(f'The worst movies with a rating of {worst} are:')
            for key in worsts:
                print(key)
        else:
            for title, rating in worsts.items():
                print(f'Worst movie: {title}, {rating}')


    def _command_movie_stats(self):
        """
        method to create stats of the movie list and prints them to screen
        """
        movies = self._storage.movies
        rating_lst = [value_dictionary["rating"] for value_dictionary in movies.values()]
        avrg_rate = self.calc_avrg(movies)
        median_rate = statistics.median(rating_lst)
        best = max(rating_lst)
        best_movies = self.similar_val(best, movies)
        worst = min(rating_lst)
        worst_movies = self.similar_val(worst, movies)
        self.print_movie_stats(avrg_rate, median_rate, best, best_movies,
                               worst, worst_movies)


#--------------random Movie-----------------------------------
    def _command_rand_movie(self):
        """
        method to cal a random movie from Dictionary
        """
        movies = self.storage.movies
        key_list = []
        for key in movies:
            key_list.append(key)
        rand_num = random.randrange(len(movies) - 1)
        print(
            f"Your movie for tonight: {key_list[rand_num]}, "
            f"it's rated {movies[key_list[rand_num]]['rating']}"
        )


#----------------search movie---------------------------------
    def levenshtein_dist(self, string1, string2):
        """
        function to calculate levenshtein distance between 2 strings
        """
        length1, length2 = len(string1), len(string2)
        # swap strings in case string2 is bigger to simplify calculations
        if length1 < length2:
            string1, string2 = string2, string1
            length1, length2 = length2, length1
        distance = [list(range(length2 + 1))] + [[i] + [0] * length2 \
                                                 for i in range(1, length1 + 1)]
        for j in range(1, length2 + 1):
            for i in range(1, length1 + 1):
                if string1[i - 1] == string2[j - 1]:
                    distance[i][j] = distance[i - 1][j - 1]
                else:
                    distance[i][j] = min(distance[i - 1][j], distance[i][j - 1],
                                         distance[i - 1][j - 1]) + 1
        return distance[length1][length2]


    def similarity(self, input_string, reference_string):
        """
        function returns distance between 2 strings with levenstein_distance
        """
        distance = self.levenshtein_dist(input_string, reference_string)
        max_length = max(len(input_string), len(reference_string))
        similarity = 1 - (distance / max_length)
        return similarity


    def _command_search_movie(self):
        """
        method to search a movie in the json file
        """
        search_string = input(f'{GREEN}Enter part of movie name: {RESET}')
        print()
        found = False
        movies = self.storage.movies
        distant_movies = []
        for key in movies:
            if search_string.lower() in (key.lower()):
                print(f'{key}, {movies[key]["rating"]}')
                found = True
            elif self.similarity(search_string.lower(), key.lower()) > 0.21:
                distant_movies.append(key)
        if not found:
            if distant_movies != []:
                print(f'The movie "{search_string}" does not exist. Did you mean: ')
                for movie in distant_movies:
                    print(movie)
            else:
                print(f'{RED}Sorry no movie found{RESET}')


#----------------get sorted movie list-------------------------
    def _command_sorted_movies(self, sorting_value, order=True):
        """
        function so print movies sorted by rating in descending order
        """
        movies_dict = self.storage.movies
        if sorting_value == "year":
            input_order = input(
                "Please enter c if you want "
                "to keep the chronological order or anything else if not: "
            )
            other_val = 'rating'
            if input_order != "c":
                order = False
        else:
            other_val = 'year'
        sorted_dict = dict(sorted(movies_dict.items(), key=lambda x: x[1][sorting_value],
                                 reverse=order))
        for key in sorted_dict:
            print(
                f'{key} with {sorting_value}: {sorted_dict[key][sorting_value]} '
                f'and {other_val}: {sorted_dict[key][other_val]}'
            )


#-----------------filter movies---------------------------------
    def _command_filter_movies(self, min_rating=0, min_year=1900, max_year=THIS_YEAR):
        """
        filter function to print filtered movie list depending on user input
        """
        try:
            min_rating = self.get_rating("Enter minimum rating (leave blank for no"
                                         " minimum rating): ")
        except ValueError as value_error:
            print("Minimum rating set to default!")
        try:
            min_year = self.get_year("Enter start year (leave blank for no start year): ")
        except ValueError as value_error:
            print("Minimum year set to default!")
        try:
            max_year = self.get_year("Enter end year (leave blank for no end year): ")
        except ValueError as value_error:
            print("Maximum year set to default")
        print()
        filtered_movies_dict = {
            key: value_dict for key, value_dict in self.storage.movies.items()
            if value_dict["rating"] >= min_rating and int(value_dict["year"]) >= min_year
                and int(value_dict["year"]) <= max_year
        }
        print("Filtered Movies:")
        for title, values in filtered_movies_dict.items():
            print(f'{title} ({values["year"]}): {values["rating"]}')


#--------------HTML handling------------------------------------
    @property
    def html_template_string(self):
        """
        getter for getting a html template file string  from local file
        "webFiles/index_template.html"
        """
        with open("webFiles/index_template.html", 'r', encoding="utf8") as reader:
            return reader.read()


    @html_template_string.setter
    def html_template_string(self, html_string):
        """
        setter method to write html to the local file "webFiles/index.html"
        :param html_string
        :return:
        """
        if self.storage.owner:
            file = f"webFiles/{self.storage.owner}.html"
        else:
            file ="webFiles/index.html"
        with open(file, "w", encoding="utf8") as writer:
            writer.write(html_string)

    def get_country_code(self, country_name: str) -> str | None:
        """
            function to generate 2 letter country code
            :return:
        """
        try:
            country = pycountry.countries.lookup(country_name)
            return country.alpha_2  # Returns the two-letter country code
        except LookupError:
            return None  # Return None if the country is not found


    def html_creator(self, original_string):
        """
        creating a html code to insert in other html code
        """
        new_html_string = "\n"
        for title, movie in self.storage.movies.items():
            imdb_link = requests.get(
                "http://www.omdbapi.com/?apikey="
                f"{API_KEY}&t={title.replace(" ", "+")}",timeout=15
            ).json()
            if imdb_link["Response"] == "True":
                imdb_url = f"https://www.imdb.com/title/{imdb_link["imdbID"]}"
                countries = imdb_link["Country"].split(", ")
                emojis = requests.get("https://api.github.com/emojis",timeout=15).json()
                flags = []
                for country in countries:
                    if country.lower() in emojis.keys():
                        flags.append(emojis[country.lower()])
                    else:
                        country_code = self.get_country_code(country)
                        if country_code.lower() in emojis.keys():
                            flags.append(emojis[country_code.lower()])
            if imdb_link["Response"] == "False":
                imdb_url=None
            new_html_string += "        <li>\n"
            new_html_string += "            <div class=\"movie\">\n"
            if "poster" in movie:
                new_html_string += f"                <a href=\"{imdb_url}\">"
                new_html_string += "<img class=\"movie-poster\" "
                if "note" in movie:
                    new_html_string += (f"src=\"{movie["poster"]}\" title=\"{movie["note"]}\" />"
                                        f"</a>\n")
                else:
                    new_html_string += f"src=\"{movie["poster"]}\" title=\"None\" /></a>\n"
            else:
                new_html_string += "                <img class=\"movie-poster\" "
                if "note" in movie:
                    new_html_string += f"src=\"EMPTY\" title=\"{movie["note"]}\" />\n"
                else:
                    new_html_string += "src=\"None\" title=\"None\" />\n"
            new_html_string += f"            <div class=\"movie-title\">{title}</div>\n"
            new_html_string += "<div class=\"movie-origin\">Country:"
            for flag in flags:
                new_html_string += "<img class=\"movie-origin\""
                new_html_string += f" src=\"{flag}\" title=\"\"/>"
            new_html_string += "</div>\n"
            new_html_string += f"            <div class=\"movie-year\">{movie["year"]}</div>\n"
            new_html_string += f"            <div class=\"movie-rating\">"
            new_html_string += f"Imdb:{movie["rating"]}</div>\n"
            new_html_string += "            </div>\n"
            new_html_string += "        </li>\n\n"
        return original_string.replace("        __TEMPLATE_MOVIE_GRID__", new_html_string)


    def _generate_website(self):
        """generate a website of the given storage"""
        if self.storage.owner:
            html_string = self.html_template_string
            html_string = html_string.replace("DEFAULT", self.storage.owner)
            html_string = self.html_creator(html_string)
            self.html_template_string = html_string
        else:
            html_string = self.html_creator(self.html_template_string)
            self.html_template_string = html_string
        print("Website generated successfully!")


    def _command_change_db(self):
        """
        Bonus function to change database
        :return:
        """
        while True:
            try:
                new_storage_path = self.get_title(
                    f"{GREEN}Please enter new file for database:{RESET} "
                )
                if new_storage_path.split(".")[1] in ["json","csv"]:
                    break
                else:
                    print(
                        f"{RED}Please enter a storage file with either"
                        f" .json or .csv as ending!{RESET}"
                    )
            except IndexError:
                print(f"{RED}Wrong Input enter a .json or .csv file please!{RESET}")
        new_file = f"storageFiles/{new_storage_path}"
        if not os.path.exists(new_file):
            if new_storage_path.split(".")[1] == "json":
                with open(
                   new_file, "w", encoding="utf8"
                ) as file_writer:
                    json.dump({}, file_writer, indent=4)
            else:
                open(new_file, "w", encoding="utf8").close()
        if new_storage_path.split(".")[1] == 'json':
            if input("Enter y if you want to add owner to storage: ") == 'y':
                owner = self.get_title("Enter owner: ")
                new_storage = StorageJson(new_file, owner)
            else:
                new_storage = StorageJson(new_file)
        if new_storage_path.split(".")[1] == 'csv':
            if input("Enter y if you want to add owner to storage: ") == 'y':
                owner = self.get_title("Enter owner: ")
                new_storage = storage_csv.StorageCsv(new_file, owner)
            else:
                new_storage = storage_csv.StorageCsv(new_file)
        self.storage = new_storage


#----------------Main Menue ---------------------------------
    def print_menu(self):
        """
        Method to print a prompt with a menu for a user to choose from
        """
        print(f"{BLUE}", end="")
        if self.storage.owner:
            print('*' * 10, f" {self.storage.owner}'s Movies Database ", '*' * 10)
        else:
            print('*' * 10, f" Default's Movies Database ", '*' * 10)
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
        print('10. Filter movies')
        print('11. Generate Website')
        print(f'12. Change Storage File{RESET}')
        print()


    def menu_choice(self, prompt):
        """
        function that checks for right user input when choosing from menu
        :return:
        """
        menu_choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        input_string = input(prompt)
        if input_string not in menu_choices:
            raise ValueError(f"{RED}Choice must be a digit within 0 and 12{RESET}")
        else:
            return input_string


    def run(self):
        """
        function to handle program usage
        :return:
        """
        function_dictionary = {
            '0': exit,
            '1': self._command_list_movies,
            '2': self._command_add_movie,
            '3': self._command_delete_movie,
            '4': self._command_update_movie,
            '5': self._command_movie_stats,
            '6': self._command_rand_movie,
            '7': self._command_search_movie,
            '8': self._command_sorted_movies,
            '9': self._command_sorted_movies,
            '10': self._command_filter_movies,
            '11': self._generate_website,
            '12': self._command_change_db
        }
        while True:
            try:
                self.print_menu()
                user_input = self.menu_choice(f'{GREEN}Enter choice (0-12): {RESET}')
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
                    self.print_menu()
                    user_input = self.menu_choice(f'{GREEN}Enter choice (0-12): {RESET}')
                    break
                except ValueError as wrongchoice:
                    print(wrongchoice)
        print('Bye!')


def main():
    """ main function to start program """
    storage = StorageJson('storageFiles/movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
