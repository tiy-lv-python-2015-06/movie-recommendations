import csv
import math


class Movie:

    def __init__(self, mid, name):
        self.movie_id = mid
        self.ratings = []
        self.name = name
        self.ave_rating = 0

    def __str__(self):
        return "movie id: {} title: {} ratings: {} average rating: {}".\
            format(self.movie_id, self.name, self.ratings, self.ave_rating)

    def find_ave_rating(self):

        self.ave_rating = int(sum(self.ratings)/len(self.ratings))
        return self.ave_rating

    def find_ave_rating_with_min_num(self, min_num):
        """
            only find the ave rating for movies that have
            over x number of ratings
        """
        if len(self.ratings) > min_num:
            self.find_ave_rating()
            return self.ave_rating
        else:
            return 0


class User:

    def __init__(self, uid):
        self.user_id = uid
        self.user_movie_rating = []  # a list of tuples (movie id, rating)
        self.movies_not_reviewed = []

    def find_highest_rated(self, num):

        # sort the list from highest to lowest
        high_ratings = \
            sorted(self.movies_not_reviewed,
                   key=lambda movie: movie.ave_rating,
                   reverse=True)

        # get just the number the user requested
        return high_ratings[:num]

    def movie_id_list_from_tuple(self):
        return [movie_id[0] for movie_id in self.user_movie_rating]

    def __str__(self):
        return \
            "user id: {} user movie rating tuple: {}".\
            format(self.user_id, self.user_movie_rating)


class MovieGen:

    def __init__(self, user_id):
        self.user_id = user_id

    def find_user_list(self, user_list):
        """
            This function will create a list of user id indexed dictionaries
            that contain a user object.
        """
        this_user_list = []
        the_user_dict = {}
        for data_set in user_list:
            # we only need to make a new user if this user is not
            # already in the
            # user dict
            if data_set['user id'] not in the_user_dict:
                user = User(data_set['user id'])
            else:
                user = the_user_dict[data_set['user id']]

            for u_dict in the_user_dict:

                if u_dict == data_set['user id']:

                    user.user_movie_rating.append(
                        (int(data_set['movie id']), int(data_set['rating'])))

            # if this user id is not already in the dict/list
            if data_set['user id'] not in the_user_dict:
                the_user_dict[data_set['user id']] = user
                this_user_list.append(the_user_dict)

        return the_user_dict

    def take_out_already_reviewed(self, the_movie_dict, user_obj):

        new_movie_dict = the_movie_dict
        # if this user already rated this movie take it out of the list
        for tup in user_obj.user_movie_rating:
            if tup[0] in the_movie_dict:
                del new_movie_dict[tup[0]]

        return new_movie_dict

    def find_movie_dict(self, movie_dict, user_list, user_obj):
        # get each movie id out of the movie dict list
        # we'll need a dictionary of movie objects with key movie id
        the_movie_dict = {}
        # we'll also need just a list of movie objects
        the_movie_list = []
        for each_d in movie_dict:
            movie = Movie(each_d['movie id'], each_d['movie title'])

            # Find all ratings for a movie by id
            for user in user_list:
                if user['movie id'] == each_d['movie id']:
                    movie.ratings.append(int(user['rating']))

            movie.find_ave_rating_with_min_num(min_reviews)
            the_movie_list.append(movie)
            the_movie_dict[(int(each_d['movie id']))] = movie

        user_obj.movies_not_reviewed = the_movie_list
        return the_movie_dict


if __name__ == '__main__':

    def find_one_user_match(match_id):
        ratings = user_dict1[match_id].movie_id_list_from_tuple()
        the_euc_dist = (0,)
        for key, item in user_dict1.items():
                if match_id != key:
                    ratings2 = item.movie_id_list_from_tuple()
                    common_movie_id_list = find_common_rating_list(ratings,
                                                                   ratings2)

                    user1_common_ratings = \
                        trim_list(common_movie_id_list,
                                  user_dict1[match_id].user_movie_rating)
                    user2_common_ratings = \
                        trim_list(common_movie_id_list,
                                  item.user_movie_rating)

                    new_euc_dist = euclidean_distance(user1_common_ratings,
                                                      user2_common_ratings)
                    if new_euc_dist > the_euc_dist[0]:
                        the_euc_dist = (new_euc_dist, item.user_id)

        return the_euc_dist

    def find_common_rating_list(lista, listb):
        return set(lista) & set(listb)

    def trim_list(common_rlist, user_rlist):

        new_user_list = []
        for each_r in user_rlist:

            if each_r[0] in common_rlist:
                new_user_list.append(each_r[0])

        return new_user_list

    def euclidean_distance(v, w):
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

    user_choice = ''

    # with the dict of movies & ratings display the X movies with the
    # highest ave rating
    while user_choice.lower() != 'e':
        user_choice = input('\n'
                            'Choose (P) for popular movies you haven\'t seen '
                            'or (A) for all movies specific to you.'
                            '\nPlease type (E) to exit\n\n')

        if user_choice.lower() != 'e':
            num_movies = int(input(
                'How many movies do you want us to recommend?'))
            min_reviews = \
                int(input('What is the minimum number of reviews you want to '
                          'include in your search?'))
            user_id1 = input('What is your user ID?')

            md_header = ['movie id', 'movie title', 'release date', 'unknown',
                         'IMDb URL', 'genres1', 'genres2', 'genres3',
                         'genres4', 'genres5', 'genres6', 'genres7', 'genres8',
                         'genres9', 'genres10', 'genres11', 'genres12',
                         'genres13', 'genres14', 'genres15', 'genres16',
                         'genres17', 'genres18', 'genres19']
            movie_dict_list = []
            with open('./ml-100k/u.item', encoding="ISO-8859-1") as file:
                reader = csv.reader(file, delimiter="|")
                for row in reader:
                    movie_item_dict = dict(zip(md_header, row))
                    movie_dict_list.append(movie_item_dict)

            ud_header = ['user id', 'movie id', 'rating', 'timestamp']
            user_data_list = []
            with open('./ml-100k/u.data', encoding="ISO-8859-1") as file:
                reader = csv.reader(file, delimiter="\t")
                for row in reader:
                    user_data_dict = dict(zip(ud_header, row))
                    user_data_list.append(user_data_dict)

            user1_mov_gen = MovieGen(user_id1)

            user_dict1 = user1_mov_gen.find_user_list(user_data_list)

            the_movie_dict1 = \
                user1_mov_gen.find_movie_dict(movie_dict_list, user_data_list,
                                              user_dict1[user_id1])

            the_movie_dict1 = \
                user1_mov_gen.take_out_already_reviewed(the_movie_dict1,
                                                        user_dict1[user_id1])

        if user_choice.lower() == 'p':
            # sort the list from highest to lowest
            highest_ratings = user_dict1[user_id1].\
                find_highest_rated(num_movies)

            print('\nYour top {} movies are:\n'.format(num_movies))
            for each in highest_ratings:
                print('{}  with an average rating of {}'.
                      format(each.name, each.ave_rating, each.ratings))
        elif user_choice.lower() == 'a':
            # given our user loop through all the other
            # users and find the highest
            # euclidean distance then show their top ratings * euclid distance
            matched_user_tuple = find_one_user_match(user_id1)
            print('\nthe user with the top euclidean distance to you is:{} '
                  ' and the distance is:{}'
                  .format(matched_user_tuple[1], matched_user_tuple[0]))

            user2_mov_gen = MovieGen(matched_user_tuple[1])
            user_dict2 = user2_mov_gen.find_user_list(user_data_list)
            the_movie_dict2 = \
                user1_mov_gen.\
                    find_movie_dict(movie_dict_list, user_data_list,
                                    user_dict2[matched_user_tuple[1]])

            the_movie_dict2 = \
                user1_mov_gen.take_out_already_reviewed(the_movie_dict1,
                                                        user_dict1[user_id1])

            highest_ratings = user_dict2[matched_user_tuple[1]].\
                find_highest_rated(num_movies)

            print('Your top {} movies are:\n'.format(num_movies))
            for each in highest_ratings:
                print('{}  with your predicted rating of {}'.
                      format(each.name, each.ave_rating*matched_user_tuple[0]))
