import csv
import math


class MovieData(object):
    """Object that holds list of movies and methods that support it"""
    movie_list = []

    def __init__(self, movies):
        """Initializes object with list of movies"""
        self.movie_list = movies

    def retrieve_name_of_movie(self, movie_id):
        """Returns name of movie at movie_id"""
        count = 0
        found = False
        value_to_return = ""
        if movie_id > len(self.movie_list):
            print("Sorry there is no movie with that ID.")
        else:
            while not found:
                if int(self.movie_list[count][0]) == movie_id:
                    value_to_return = self.movie_list[count][1]
                    found = True
                else:
                    count += 1
                    found = False
        return value_to_return


class MovieRating(object):
    """Object that holds list of ratings for movies and methods that support it"""
    rating_list = []

    def __init__(self, ratings):
        """Initializes object with list of ratings of movies"""
        self.rating_list = ratings

    def retrieve_ratings_by_movie(self, movie_id):
        """Retrieves all ratings for a movie and returns them all as a list"""
        count = 0
        list_of_ratings = []
        if movie_id > len(self.rating_list):
            print("Sorry, there is no movie with that ID.")
        else:
            while count <= len(self.rating_list) - 1:
                if int(self.rating_list[count][1]) == movie_id:
                    list_of_ratings.append(self.rating_list[count])
                    count += 1
                else:
                    count += 1
        return list_of_ratings

    def retrieve_average_rating_for_movie(self, movie_id):
        """Computes the average rating for a movie and returns it"""
        list_of_movie_ratings = self.retrieve_ratings_by_movie(movie_id)
        count = 0
        list_length = len(list_of_movie_ratings)
        total_rating = 0
        while count <= list_length - 1:
            total_rating += int(list_of_movie_ratings[count][2])
            count += 1
        if list_length != 0:
            return total_rating / list_length
        else:
            return 0

    def retrieve_ratings_by_user(self, user_id):
        """Retrieves all ratings by user and returns them all as a list"""
        count = 0
        list_of_ratings = []
        if user_id > len(self.rating_list):
            print("Sorry, there is no user with that ID.")
        else:
            while count <= len(self.rating_list) - 1:
                if int(self.rating_list[count][0]) == user_id:
                    list_of_ratings.append(self.rating_list[count])
                    count += 1
                else:
                    count += 1
        return list_of_ratings

    def rate_all_movies(self):
        """Rates 20 movies and their ratings as a list"""
        average_rating_list = []
        count = 0
        while count <= 19:
            average_rating_list.append(self.retrieve_average_rating_for_movie(count + 1))
            count += 1
        return average_rating_list

    def euclidean_distance(self, v, w):
        """Given two lists, give the Euclidean distance between them on a scale
        of 0 to 1. 1 means the two lists are identical.
        """
        # Guard against empty lists.
        if len(v) is 0:
            return 0
        # Note that this is the same as vector subtraction.
        differences = [v[idx] - w[idx] for idx in range(len(v))]
        squares = [diff ** 2 for diff in differences]
        sum_of_squares = sum(squares)
        return 1 / (1 + math.sqrt(sum_of_squares))

    def prepare_eucl(self, user_list):
        """Creates a list that can then be sent to the Euclidean distance method"""
        eucl_list = []
        count = 0
        while count <= len(user_list) - 1:
            eucl_list.append(int(user_list[count][2]))
            count += 1
        return eucl_list


def read_movie_data():
    """Reads in data for movies from a file and returns it as a list."""
    # Read in all movie data
    movie_list = []
    with open("/users/scottholmes/documents/movieinfo/ml-100k/u.item", encoding='ISO-8859-1') as file:
        movie_data = csv.reader(file, delimiter="|")
        for movie in movie_data:
            movie_list.append(movie)
    return movie_list


def read_movie_ratings():
    """Reads in ratings data for movies from a file and returns it as a list."""
    rating_list = []
    with open("/users/scottholmes/documents/movieinfo/ml-100k/u.data", encoding='ISO-8859-1') as file:
        rating_data = csv.reader(file, delimiter="\t")
        for rating in rating_data:
            rating_list.append(rating)
    return rating_list


def menu(movie_object1, rating_object1):
    """Controls flow of menu"""
    print("Welcome to the movie rating menu!")
    print("Choose an option:")
    print("    Choose (1) to list all ratings for a movie by ID.")
    print("    Choose (2) to list the average rating for a movie by ID.")
    print("    Choose (3) to list the name of a movie by ID.")
    print("    Choose (4) to list all ratings for a user.")
    print("    Choose (5) to list ratings for 20 movies.")
    print("    Choose (6) to get the Euclidean distance between two lists of ratings from users.")
    print("    Enter (99) if done with menu. ")
    user_input = int(input("Enter choice here: "))
    if user_input == 1:
        user_input = int(input("Enter a movie ID. "))
        print(rating_object1.retrieve_ratings_by_movie(user_input))
    elif user_input == 2:
        user_input = int(input("Enter a movie ID. "))
        print(rating_object1.retrieve_average_rating_for_movie(user_input))
    elif user_input == 3:
        user_input = int(input("Enter a movie ID. "))
        print(movie_object1.retrieve_name_of_movie(user_input))
    elif user_input == 4:
        user_input = int(input("Enter user ID. "))
        print(rating_object1.retrieve_ratings_by_user(user_input))
    elif user_input == 5:
        print(rating_object1.rate_all_movies())
    elif user_input == 6:
        user_input_one = int(input("Enter first user. "))
        user_input_two = int(input("Enter second user. "))
        temp_list1 = rating_object1.prepare_eucl(rating_object1.retrieve_ratings_by_user(user_input_one))
        temp_list2 = rating_object1.prepare_eucl(rating_object1.retrieve_ratings_by_user(user_input_two))
        result = rating_object1.euclidean_distance(temp_list1, temp_list2)
        print("Euclidean distance is: {}".format(result))
    else:
        return True


if __name__ == '__main__':
    """Start here when file run directly."""

    movie_data_list = read_movie_data()  # reads in movie data from file and returns it as a list
    rating_data_list = read_movie_ratings()  # reads in rating data from file and returns it as a list
    enter_done = False

    movie_data_object = MovieData(movie_data_list)  # instantiates movie data object with a list of movies
    rating_data_object = MovieRating(rating_data_list)  # instantiates rating data object with a list of ratings

    while not enter_done:
        print()
        enter_done = menu(movie_data_object, rating_data_object)
        if enter_done:
            print("Exiting menu. ")
            break
