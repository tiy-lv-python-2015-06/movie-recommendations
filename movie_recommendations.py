import csv
import math
import re


class Movie:
    def __init__(self, title=None, genres=None,
                 ratings=None, movieid=None, link=None, date=None):
        self.title = title
        self.genres = genres
        self.ratings = {}
        self.movieid = movieid
        self.link = re.sub(r'\([^)]*\)', '', link)
        self.date = date
        self.avg_rating = ''

    @property
    def calc_avg_rating(self):
        self.avg_rating = round((sum(float(x) for x in self.ratings.values()) /
                                 len(self.ratings.values())), 5)
        return self.avg_rating

    """I don't know what @property means, but pycharm told me to do it
     and pycharm is smarter than me....what does this mean???"""


def menu():
    """The menu that allows users to what movies they want to see"""
    while True:
        choice = input('\nTo see the Top Rated movies, press 1\n'
                       'To see movies recommended for you, press 2\n'
                       'Or press [E] to Exit\n').lower()
        if choice == '1' or choice == '2' or choice == 'e':
            print('\n')
            return choice
            break
        else:
            print('\nPlease make a valid choice (1,2 or E)')
            continue


def get_data():
    """imports the movie data"""
    """I used a global variable here because I didn't want
    to have to run through the data twice, and the user list is
    Used a lot. I also don't need it, because
    the numbers seem to be sequential, but in case they aren't..."""
    global user_list
    with open('u.item') as data:
        reader = csv.reader(data, delimiter='|')
        movies = {}
        for row in reader:
            key = row[0]
            movies[key] = Movie(title=row[1], link=row[4],
                                genres=row[5:], movieid=key, date=row[2])

    with open('u.data') as data:
        reader = csv.reader(data, delimiter='\t')
        for row in reader:
            key = row[1]
            movies[key].ratings[row[0]] = row[2]
            if row[0] not in user_list:
                user_list.extend([row[0]])
    return movies


def calc_all_avg_ratings():
    """Tells all the movies to Calculate their aveage rating"""
    """I put this in again so it didn't run
    before all data was enter for the movies. Probably a better way"""
    {key: movies[key].calc_avg_rating for key in movies.keys()}


def highest_rated(max_items):
    """Returns the next 5 movies with the highest average rating"""
    high_rated = ({key: movies[key].avg_rating for key in movies.keys()})
    return sorted(high_rated.items(), key=lambda x: (x[1], (x[0])),
                  reverse=True)[max_items - 5:max_items]


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


def common_movies(user1, user2):
    user1_common_ratings = []
    user2_common_ratings = []
    for movie in movies:
        if user1 in movies[movie].ratings.keys() \
                and user2 in movies[movie].ratings.keys():
            user1_common_ratings.append(float(movies[movie].ratings[user1]))
            user2_common_ratings.append(float(movies[movie].ratings[user2]))
    return user1_common_ratings, user2_common_ratings


def user_like_users(user_id, user_list):
    like_user = {}
    for user in user_list:
        if user != user_id:
            movies_in_common = (common_movies(user_id, user))
            like_user[user] = round(
                euclidean_distance(
                    movies_in_common[0], movies_in_common[1]), 4)
    return sorted(
        like_user.items(), key=lambda x: (x[1], x[0]), reverse=True)[:15]


def movies_not_seen(user_id, like_users, idx=0):
    recommend_dict = {}
    not_seen = []
    for movie in movies:
        for user in like_users:
            if user_id not in movies[movie].ratings.keys() \
                    and user[0] in movies[movie].ratings.keys():
                recommend_dict[(movies[movie].movieid)] = \
                    (float(movies[movie].ratings[user[0]]) * float(user[1]))
    for x in sorted(
            recommend_dict.items(), key=lambda x: (x[1], x[0]), reverse=True):
        not_seen.append([x[0]])
    return not_seen[idx - 5:idx]
    # I think this is the hack way to make a generator. Make it a real one?


def show_top_rated():
    x = 0
    answer = 'n'
    while answer == 'n' or answer == 'next':
        x += 5
        top_movies = highest_rated(x)
        for y in top_movies:
            print(('{} \nAverage Rating:{}\n{}\n').format(
                id_to_title(y), movies[y[0]].avg_rating, movies[y[0]].link))
        if next_results():
            continue
        else:
            break


def show_top_recommended():
    x = 0
    user_num = input('Please Enter your ID\n')
    while user_num not in user_list:
        user_num = input('Please Enter a valid ID\n')
    answer = 'n'
    while answer == 'n' or answer == 'next':
        x += 5
        top_movies = (
            movies_not_seen('2', user_like_users(user_num, user_list), idx=x))
        for y in top_movies:
            print('{} \nAverage Rating:{}\n{}\n'
                  .format(id_to_title(y),
                          movies[y[0]].avg_rating, movies[y[0]].link))
        if next_results():
            continue
        else:
            break


def next_results():
    answer = input(('\nWould you like to see the [N]ext 5 results,'
                    '  or [R]eturn to the Menu?\n')).lower()
    while answer != 'r':
        if answer == 'n' or answer == 'next':
            return True
        else:
            answer = input('Please enter a valid choice("N" or "R"\n').lower()
    return False


def id_to_title(list_of_ids):
    if len(list_of_ids) == 2:
        return movies[list_of_ids[0]].title
    else:
        titles = []
        for x in list_of_ids:
            titles.append(movies[x[0]].title)
        return titles


def show_for_user():
    user_num = input('Please Enter your ID\n')
    while user_num not in user_list:
        user_num = input('Please Enter a valid ID\n')
    print('working')


if __name__ == '__main__':
    print('\n*****Welcome to the Hipster Movie Recommender*****\n')
    user_list = []
    movies = get_data()
    calc_all_avg_ratings()
    while True:
        prompt = menu()
        if prompt == '1':
            show_top_rated()
            continue
        elif prompt == '2':
            show_top_recommended()
        else:
            break
    print('*****Enjoy your movie***')
