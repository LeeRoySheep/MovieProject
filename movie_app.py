import statistics
import re

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
    def storage(self, storage):
        """ setter for class variable _storage"""
        self._storage = storage


    def _command_list_movies(self):
        movies = self.storage.list_movies()

        print(f"A list of {len(movies)} in the given storage.")
        for movie_name, movie_dict in movies:
            print(f"{movie_name} ({movie_dict["year"]}): {movie_dict["rating"]}")


    def calc_avrg(movies_dict):
        """
        method to calculate avarage value by rating
        """
        avrg_rate = 0
        for value_dictionary in movies_dict.values():
            avrg_rate += value_dictionary["rating"] / len(movies_dict)
        return avrg_rate


    def similar_val(val, movies_dict):
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
        movies = self._storage.list_movies
        rating_lst = [value_dictionary["rating"] for value_dictionary in movies.values()]
        avrg_rate = self.calc_avrg(movies)
        median_rate = statistics.median(rating_lst)
        best = max(rating_lst)
        best_movies = self.similar_val(best, movies)
        worst = min(rating_lst)
        worst_movies = self.similar_val(worst, movies)
        self.print_movie_stats(avrg_rate, median_rate, best_movies, worst_movies)


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
        :param html_file_path:
        :return:
        """
        with open("webFiles/index.html", "w", encoding="utf8") as writer:
            writer.write(html_string)


    def html_creator(self, original_string):
        """
        creating a html code to insert in other html code
        """
        movies = self.storage.list_movies()
        new_html_string = ""
        for movie in movies:
            new_html_string = "        <li>\n"
            new_html_string += "            <div class=\"movie\">\n"
            new_html_string += "                <img class=\"movie-poster\" "
            new_html_string += f"src={movie["poster"]} title=\"\" / >\n"
            new_html_string += f"            <div class=\"movie-title\"> {movie['title']} </div>"
            new_html_string += f"            <div class=\"movie-year\'> {movie["year"]} </div>"
            new_html_string += "            </div>"
            new_html_string += "</li>"
        return original_string.replace("__TEMPLATE_MOVIE_GRID__", new_html_string)



    def _generate_website(self):
        """generate a website of the given storage"""
        html_string = self.html_creator(self.html_template_string)
        self.html_template_string = html_string


    def run(self):
      # Print menu
      # Get use command
      # Execute command