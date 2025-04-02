from istorage import IStorage
import csv

class StorageCsv(IStorage):
    """
    Storage class to handle storage in csv files
    """
    def __init__(self, file_path, owner=None):
        """
        constructor to create instance of StorageCsv class
        :param file_path:
        :param owner:
        :return:
        """
        self._file_path = file_path
        self._owner = owner


    @property
    def owner(self):
        """
        getter to return owner
        :return: self._owner
        """
        return self._owner


    @owner.setter
    def owner(self, new_owner):
        """
        setter to overwrite self._owner
        """
        self._owner = new_owner


    @property
    def file_path(self):
        """magic getter method"""
        return self._file_path


    @file_path.setter
    def file_path(self, new_file_path):
        """magic setter method"""
        self._file_path = new_file_path


    @property
    def movies(self):
        """ Create a dictionary from a csv file"""
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        movie_dict = dict()
        for movie in data:
            for key, val in movie.items():
                if movie["title"] in movie_dict:
                    if key == "rating" and key != "title":
                        movie_dict[movie["title"]][key] = float(val)
                    elif key != "title":
                        movie_dict[movie["title"]][key] = val
                else:
                    if key == "rating" and key != "title":
                        movie_dict[movie["title"]] = {key: float(val)}
                    elif key != "title":
                        movie_dict[movie["title"]] = {key: val}
        return movie_dict


    @movies.setter
    def movies(self, movie_dict):
        """function to crate dict list from nested dict and saves as csv file"""
        movie_lst = []
        for key, val in movie_dict.items():
            new_dic = dict()
            new_dic["title"] = key
            for key2, val2 in val.items():
                new_dic[key2] = val2
            movie_lst.append(new_dic)
        field_names = []
        for movie in movie_lst:
            for key in movie.keys():
                if not key in field_names:
                    field_names.append(key)
        with open(self.file_path, 'w', encoding="utf8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(movie_lst)



