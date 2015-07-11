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
        self.avg_rating = round((sum(int(x) for x in self.ratings.values()) / len(self.ratings.values())), 3)
        return self.avg_rating
    """I don't know what @property means, but pycharm told me to do it
     and pycharm is smarter than me....what does this mean???"""


def get_data():
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
    return movies


def calc_all_avg_ratings():
    {key: movies[key].calc_avg_rating for key in movies.keys()}
    pass


def highest_rated(max_items):
    high_rated = ({key: movies[key].avg_rating for key in movies.keys()})
    return (sorted(high_rated.items(), key=lambda x: (x[1]), reverse=True)[:max_items])


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

def user_lists(user1, user2):
    user1_list = []
    user2_list =[]
    for movie in movies:
        if user1 in movies[movie].ratings.keys() and user2 in movies[movie].ratings.keys():
            user1_list.append(int(movies[movie].ratings[user1]))
            user2_list.append(int(movies[movie].ratings[user2]))

    return user1_list, user2_list

if __name__ == '__main__':
    movies = get_data()
    calc_all_avg_ratings()
    # print(highest_rated(20))
    user1 = '196'
    user2 = '186'
    print(user_lists(user1,user2))
    print(euclidean_distance(user_lists(user1,user2)[0], user_lists(user1,user2)[1]))

    # need to create two lists for users, each made up of movies that each has seen, in order.

    # print(movies['242'].calc_avg_rating())
    # print(movies['242'].title)
    # print(movies['242'].date)
    # print(movies['242'].link)
    # print(movies['242'].movieid)
    # print(movies['242'].ratings.values())
    # # print(sum((movies['242'].ratings.values())))
    # print(movies['242'].genres)
