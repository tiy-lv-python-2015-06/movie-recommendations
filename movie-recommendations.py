import csv


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

        #only find the ave rating for movies that have over x number of ratings
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

    def euclideanDistance(self, v, w):
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

    def trim_rating_list(self, trim_to_list):

        print('the length of this list is {} and the length of ' \
              'the trim to list is {}' \
              .format(len(self.user_movie_rating), len(trim_to_list)))

        for i in self.user_movie_rating:
            print(i)
            print('is i in this list {}'. \
                  format(i[0] not in self.user_movie_rating))
            if i[0] not in trim_to_list:
                print('we are deleting i {} from this list'.format(i))
                #del self.user_movie_rating.index(i)
                self.user_movie_rating.remove(i)
                print('now the length is {}'.format(len(i)))

        print('now the length of this list is {}'.
              format(len(self.user_movie_rating)))
        return self.user_movie_rating

    def __str__(self):
        return \
            "user id: {} user movie rating tuple: {}".\
                format(self.user_id, self.user_movie_rating)

class MovieGen:

    def __init__(self, user_id):
        self.user_id = user_id

    def find_user_list(self, user_data_list):
        """
            This function will create a list of user id indexed dictionaries
            that contain a user object.
        """
        this_user_list = []
        the_user_dict = {}
        for data_set in user_data_list:
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
                        (int(data_set['movie id']), data_set['rating']))

            # if this user id is not already in the dict/list
            if data_set['user id'] not in the_user_dict:
                the_user_dict[data_set['user id']] = user
                this_user_list.append(the_user_dict)

        return the_user_dict

    def take_out_already_reviewed(self, the_movie_dict, user_obj):

        #print('the users tuple is {}'.format(user_obj.user_movie_rating))
        # if this user already rated this movie take it out of the list
        for tup in user_obj.user_movie_rating:
            del the_movie_dict[tup[0]]

        #print('now the size of the list is {}'.format(len(the_movie_dict)))
        return the_movie_dict

    def find_movie_dict(self, movie_dict_list, user_data_list, user_obj):
        # get each movie id out of the movie dict list
        # we'll need a dictionary of movie objects with key movie id
        the_movie_dict = {}
        # we'll also need just a list of movie objects
        the_movie_list = []
        for each in movie_dict_list:
            movie = Movie(each['movie id'], each['movie title'])

            # Find all ratings for a movie by id
            for user in user_data_list:
                if user['movie id'] == each['movie id']:
                    movie.ratings.append(int(user['rating']))

            movie.find_ave_rating_with_min_num(min_reviews)
            the_movie_list.append(movie)
            the_movie_dict[(int(each['movie id']))] = movie

        user_obj.movies_not_reviewed = the_movie_list
        return the_movie_dict


if __name__ == '__main__':

    # with the dict of movies & ratings display the X movies with the
    # highest ave rating
    num_movies = int(input('How many movies do you want us to recommend?'))
    min_reviews = \
        int(input('What is the minimum number of reviews you want to ' \
                  'include in your search?'))
    user_id1 = input('USER1:  What is your user ID?')
    user_id2 = input('USER2:  What is your user ID?')

    md_header = ['movie id', 'movie title', 'release date', 'unknown', \
              'IMDb URL', 'genres1', 'genres2', 'genres3', \
              'genres4', 'genres5', 'genres6', 'genres7', 'genres8', \
              'genres9', 'genres10', 'genres11', 'genres12', 'genres13', \
              'genres14', 'genres15', 'genres16', 'genres17', 'genres18', \
              'genres19']
    movie_dict_list = []
    with open('./ml-100k/u.item', encoding = "ISO-8859-1") as file:
        reader = csv.reader(file, delimiter="|")
        for row in reader:
            movie_item_dict = dict(zip(md_header, row))
            movie_dict_list.append(movie_item_dict)

    ud_header = ['user id', 'movie id', 'rating', 'timestamp']
    user_data_list = []
    with open('./ml-100k/u.data', encoding = "ISO-8859-1") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            user_data_dict = dict(zip(ud_header, row))
            user_data_list.append(user_data_dict)

    user1_mov_gen = MovieGen(user_id1)
    user2_mov_gen = MovieGen(user_id2)

    user_dict1 = user1_mov_gen.find_user_list(user_data_list)
    user_dict2 = user2_mov_gen.find_user_list(user_data_list)

    the_movie_dict1 = \
        user1_mov_gen.find_movie_dict(movie_dict_list, user_data_list,
                                      user_dict1[user_id1])

    the_movie_dict1 = user1_mov_gen.take_out_already_reviewed(
        the_movie_dict1, user_dict1[user_id1])

    print('the size of the movie gen movie list is {}'.
          format(len(the_movie_dict1)))
    print('the size of users review tuple is {}'.
          format(len(user_dict1[user_id1].user_movie_rating)))

    # sort the list from highest to lowest
    # highest_ratings = \
    #     sorted(the_movie_dict1, key=attrgetter('ave_rating'), reverse=True)
    highest_ratings = sorted(user_dict1[user_id1].movies_not_reviewed, \
                             key=lambda movie: movie.ave_rating, \
                             reverse=True)

    # get just the number the user requested
    highest_ratings = highest_ratings[:num_movies]

    print('USER1:  Your top {} movies are:\n'.format(num_movies))
    for each in highest_ratings:
        print('{}  with an average rating of {}'.
              format(each.name, each.ave_rating, each.ratings))

    the_movie_dict2 = \
        user2_mov_gen.find_movie_dict(movie_dict_list, user_data_list,
                                      user_dict2[user_id2])

    the_movie_dict2 = user2_mov_gen.take_out_already_reviewed(
        the_movie_dict2, user_dict2[user_id2])

    print('the size of the movie gen movie list is {}'.
          format(len(the_movie_dict2)))
    print('the size of users review tuple is {}'.
          format(len(user_dict2[user_id2].user_movie_rating)))

    # sort the list from highest to lowest
    highest_ratings = \
        sorted(user_dict2[user_id2].movies_not_reviewed, \
               key=lambda movie: movie.ave_rating, \
               reverse=True)

    # get just the number the user requested
    highest_ratings = highest_ratings[:num_movies]

    print('USER2:  Your top {} movies are:\n'.format(num_movies))
    for each in highest_ratings:
        print('{}  with an average rating of {}'.
              format(each.name, each.ave_rating, each.ratings))

    if len(user_dict1[user_id1].user_movie_rating) > \
        len(user_dict2[user_id2].user_movie_rating):
        trimmed_user1_list = user_dict1[user_id1].trim_rating_list(
            user_dict2[user_id2].user_movie_rating)
    else:
        trimmed_user2_list = user_dict2[user_id2].trim_rating_list(
            user_dict1[user_id1].user_movie_rating)

    # lets find the euclidean distance between these two users:
    # the_diff = user_dict1[user_id1]. \
    #     euclideanDistance(user_dict1[user_id1].user_movie_rating ,
    #                       user_dict2[user_id2].user_movie_rating)
    #
    # print('the euclidean different between user {} and user {} is {}'.
    #       format(user_id1, user_id2, the_diff))

    # for each user
    # the_user_dict = {}
    # for data_set in user_data_list:
    #     # we only need to make a new user if this user is not already in the
    #     # user dict
    #     # we are only going to this user if its not the one wanting the reviews
    #     if data_set['user id'] != user_id:
    #         if data_set['user id'] not in the_user_dict:
    #             user = User(data_set['user id'])
    #         else:
    #             user = the_user_dict[data_set['user id']]
    #
    #         for u_dict in the_user_dict:
    #
    #             if u_dict == data_set['user id']:
    #                 user.user_ratings.append(data_set['rating'])
    #
    #         # if this user id is not already in the dict
    #         if data_set['user id'] not in the_user_dict:
    #             the_user_dict[data_set['user id']] = user
    #             #print('adding this user {}'.format(str(user)))

    # get each movie id out of the movie dict list
    # we'll need a dictionary of movie objects with key movie id
    # the_movie_dict = {}
    # # we'll also need just a list of movie objects
    # the_movie_list = []
    # for each in movie_dict_list:
    #     movie = Movie(each['movie id'], each['movie title'])
    #
    #     # Find all ratings for a movie by id
    #     for m_dict in user_data_list:
    #
    #         if m_dict['movie id'] == each['movie id']:
    #             movie.ratings.append(int(m_dict['rating']))
    #
    #     movie.find_ave_rating_with_min_num(min_reviews)
    #     the_movie_list.append(movie)
    #     the_movie_dict[(int(each['movie id']))] = movie



