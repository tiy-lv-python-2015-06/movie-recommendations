import csv

class Movie:

    def __init__(self, id, name):
        self.movie_id = id
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

    def __init__(self, id):
        self.user_id = id
        self.user_ratings = []

    def __str__(self):
        return \
            "user id: {} ratings: {}".format(self.user_id, self.user_ratings)

class Movie_Gen:

    def __init__(self):
        pass

    def find_user_dict(self, user_data_list, user_id):
        # for each user
        the_user_dict = {}
        for data_set in user_data_list:
            # we only need to make a new user if this user is not already in the
            # user dict
            # we are only going to this user if its not the one wanting the reviews
            if data_set['user id'] != user_id:
                if data_set['user id'] not in the_user_dict:
                    user = User(data_set['user id'])
                else:
                    user = the_user_dict[data_set['user id']]

                for u_dict in the_user_dict:

                    if u_dict == data_set['user id']:
                        user.user_ratings.append(data_set['rating'])

                # if this user id is not already in the dict
                if data_set['user id'] not in the_user_dict:
                    the_user_dict[data_set['user id']] = user
                    #print('adding this user {}'.format(str(user)))

        return the_user_dict

if __name__ == '__main__':

    # with the dict of movies & ratings display the X movies with the
    # highest ave rating
    num_movies = int(input('How many movies do you want us to recommend?'))
    min_reviews = \
        int(input('What is the minimum number of reviews you want to ' \
                  'include in your search?'))
    user_id = input('What is your user ID?')

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
            #print(user_data_dict)

    user_dict1 = find_user_dict(user_data_list, user_id1)
    user_dict2 = find_user_dict(user_data_list, user_id2
                                )
    # for each user
    the_user_dict = {}
    for data_set in user_data_list:
        # we only need to make a new user if this user is not already in the
        # user dict
        # we are only going to this user if its not the one wanting the reviews
        if data_set['user id'] != user_id:
            if data_set['user id'] not in the_user_dict:
                user = User(data_set['user id'])
            else:
                user = the_user_dict[data_set['user id']]

            for u_dict in the_user_dict:

                if u_dict == data_set['user id']:
                    user.user_ratings.append(data_set['rating'])

            # if this user id is not already in the dict
            if data_set['user id'] not in the_user_dict:
                the_user_dict[data_set['user id']] = user
                #print('adding this user {}'.format(str(user)))

    # get each movie id out of the movie dict list
    # we'll need a dictionary of movie objects with key movie id
    the_movie_dict = {}
    # we'll also need just a list of movie objects
    the_movie_list = []
    for each in movie_dict_list:
        movie = Movie(each['movie id'], each['movie title'])

        # Find all ratings for a movie by id
        for m_dict in user_data_list:

            if m_dict['movie id'] == each['movie id']:
                movie.ratings.append(int(m_dict['rating']))

        movie.find_ave_rating_with_min_num(min_reviews)
        the_movie_list.append(movie)
        the_movie_dict[(int(each['movie id']))] = movie

    # info = []
    # new = []
    # header2 = ['users', 'items', 'ratings']
    # with open('./ml-100k/u.info') as file:
    #     reader = csv.reader(file, delimiter="\n")
    #     for row in reader:
    #         info.append(row)
    #
    #     for item in range(len(info)):
    #         idx = info[item][0].index(' ')
    #         new.append(info[item][0][:idx])
    #
    #     movie_info_dict = dict(zip(header2, new))
    #     print(movie_info_dict)

    highest_ratings = \
        sorted(the_movie_list, key=lambda movie: movie.ave_rating, reverse=True)
    highest_ratings = highest_ratings[:num_movies]

    print('Your top {} movies are:'.format(num_movies))
    for each in highest_ratings:
        print('{}  with an average rating of {} and ratings list of {}'.
              format(each.name, each.ave_rating, each.ratings))
