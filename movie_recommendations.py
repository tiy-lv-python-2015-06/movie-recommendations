import csv
import math


class Movie:
    def __init__(self, title=None, genres=None, ratings=None, movieid=None, link=None, date=None):
        self.title = title
        self.genres = genres
        self.ratings = {}
        self.movieid = movieid
        self.link = link
        self.date = date
        self.avg_rating = ''

    @property
    def calc_avg_rating(self):
        self.avg_rating = round((sum(float(x) for x in self.ratings.values()) / len(self.ratings.values())), 5)
        return self.avg_rating
    """I don't know what @property means, but pycharm told me to do it
     and pycharm is smarter than me....what does this mean???"""


def menu():
    print('Welcome to the Movie Recommender 5k\nPlease select an option')
    while True:
        choice = input('To see the top rated movies please press 1\n'
                       'To see movies recommended for you, please press 2')
        if choice == '1' or choice == '2':
            return choice
            break
        else:
            print('Please make a valid choice (1 or 2')
            continue

def get_data():
    # I used a global variable here because I didn't want to have to run through the data twice, and the user list is
    # Used a lot. I also don't need it, because the numbers seem to be sequential, but in case they aren't...
    global user_list
    with open('u.item') as data:
        reader = csv.reader(data, delimiter='|')
        movies = {}
        for row in reader:
            key = row[0]
            movies[key] = Movie(title=row[1], link=row[4], genres=row[5:], movieid=key, date=row[2])

    with open('u.data') as data:
        reader = csv.reader(data, delimiter='\t')
        for row in reader:
            key = row[1]
            movies[key].ratings[row[0]] = row[2]
            if row[0] not in user_list:
                user_list.extend([row[0]])
    return movies


def calc_all_avg_ratings():
    {key: movies[key].calc_avg_rating for key in movies.keys()}


def highest_rated(max_items):
    high_rated = ({key: movies[key].avg_rating for key in movies.keys()})
    return sorted(high_rated.items(), key=lambda x: (x[1]), reverse=True)[:max_items]


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
    user2_common_ratings =[]
    for movie in movies:
        if user1 in movies[movie].ratings.keys() and user2 in movies[movie].ratings.keys():
            user1_common_ratings.append(float(movies[movie].ratings[user1]))
            user2_common_ratings.append(float(movies[movie].ratings[user2]))
    return user1_common_ratings, user2_common_ratings


def user_like_users(user_id, user_list):
    like_user = {}
    for user in user_list:
        if user != user_id:
            movies_in_common = (common_movies(user_id, user))
            like_user[user] = round(euclidean_distance(movies_in_common[0], movies_in_common[1]), 4)
    return sorted(like_user.items(), key=lambda x: (x[1], x[0]), reverse=True)[:15]



def movies_not_seen(user_id, like_users, idx = 0):
    recommend_dict = {}
    not_seen = []
    for movie in movies:
        for user in like_users:
            if user_id not in movies[movie].ratings.keys() and user[0] in movies[movie].ratings.keys():
                recommend_dict[(movies[movie].movieid)] = (float(movies[movie].ratings[user[0]]) * float(user[1]))
    for x in sorted(recommend_dict.items(), key=lambda x: (x[1], x[0]), reverse=True):
        not_seen.append(movies[x[0]].title)
    return not_seen[idx- 10:idx]

    """this would be better if it was a generator,
    so i could print ten at a time and then return the next set if ask for more"""


if __name__ == '__main__':
    user_list = []
    movies = get_data()
    calc_all_avg_ratings()
    # if menu() == 1:
    #     pass

    # print(highest_rated(20))
    # print(common_movies(user1,user2))
    # print(euclidean_distance(common_movies(user1,user2)[0], common_movies(user1,user2)[1]))
    # print(user_like_users('1', user_list))
    x = 0
    while input('a to go') == 'a':
        x +=10
        print(movies_not_seen('2', user_like_users('199', user_list), idx = x))


    # print(movies['242'].calc_avg_rating())
    # print(movies['242'].title)
    # print(movies['242'].date)
    # print(movies['242'].link)
    # print(movies['242'].movieid)
    # print(movies['242'].ratings.values())
    # # print(sum((movies['242'].ratings.values())))
    # print(movies['242'].genres)
