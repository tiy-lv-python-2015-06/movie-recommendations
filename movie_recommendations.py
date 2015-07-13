import csv
import math
import re


class Movie:
    def __init__(self, title=None, genres=None,
                 movieid=None, link=None, date=None):
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
     and pycharm is smarter than me....what does this mean???

     I also don't know what pycharm is yelling at me about: expected size
     got iterable instead?"""


def get_data():
    """imports the movie data"""
    global user_list
    with open('u.item') as data:
        reader = csv.reader(data, delimiter='|')
        import_movies = {}
        for row in reader:
            key = row[0]
            import_movies[key] = Movie(title=row[1], link=row[4],
                                       genres=row[5:], movieid=key, date=row[2])

    with open('u.data') as data:
        reader = csv.reader(data, delimiter='\t')
        for row in reader:
            key = row[1]
            import_movies[key].ratings[row[0]] = row[2]
            if row[0] not in user_list:
                user_list.extend([row[0]])
    return import_movies


def calc_all_avg_ratings():
    """Tells all the movies to Calculate their average rating"""
    """I put this in again so it didn't run
    before all data was enter for the movies. Probably a better way"""
    # noinspection PyStatementEffect
    {key: movies[key].calc_avg_rating for key in movies.keys()}


def menu():
    """The menu that allows users to what movies they want to see"""
    while True:
        choice = input('\nTo see the Top Rated movies, press 1\n'
                       'To see movies recommended for you, press 2\n'
                       'Or press [E] to Exit\n').lower()
        if choice == '1' or choice == '2' or choice == 'e':
            print('\n')
            return choice
        else:
            print('\nPlease make a valid choice (1,2 or [E]xit)')
            continue


def highest_rated(max_items):
    """Returns the next 5 movies with the highest average rating"""
    high_rated = ({key: movies[key].avg_rating for key in movies.keys()})
    high_rated = sorted(high_rated.items(), key=lambda x: (x[1], (x[0])),
                        reverse=True)[max_items - 5:max_items]
    return high_rated


def user_like_users(user_id, other_users):
    """Finds the top x (currently 15) users by euclidean_distance for a
    given user"""
    like_user = {}
    for user in other_users:
        if user != user_id:
            movies_in_common = (common_movies(user_id, user))
            like_user[user] = round(
                euclidean_distance(
                    movies_in_common[0], movies_in_common[1]), 4)
    return sorted(
        like_user.items(), key=lambda x: (x[1], x[0]), reverse=True)[:15]


def common_movies(user1, user2):
    """Finds movies two users have both rated"""
    user1_common_ratings = []
    user2_common_ratings = []
    for movie in movies:
        if user1 in movies[movie].ratings.keys() \
                and user2 in movies[movie].ratings.keys():
            user1_common_ratings.append(float(movies[movie].ratings[user1]))
            user2_common_ratings.append(float(movies[movie].ratings[user2]))
    return user1_common_ratings, user2_common_ratings


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


def movies_not_seen(user_id, like_users, idx=0):
    """Returns the top movies that a specified user has not seen
    from a list of other users"""
    recommend_dict = {}
    not_seen = []
    for movie in movies:
        for user in like_users:
            if user_id not in movies[movie].ratings.keys() \
                    and user[0] in movies[movie].ratings.keys():
                recommend_dict[movies[movie].movieid] = \
                    (float(movies[movie].ratings[user[0]]) * float(user[1]))
    for movie in sorted(
            recommend_dict.items(), key=lambda x: (x[1], x[0]), reverse=True):
        not_seen.append((movie[0], movie[1],))
    return not_seen[idx - 5:idx]
    # I think this is the hack way to make a generator. Make it a real one?


def show_top_rated():
    """Displays the movies from the list of top rated movies"""
    x = 0
    answer = 'n'
    while answer == 'n' or answer == 'next':
        x += 5
        top_movies = highest_rated(x)
        for y in top_movies:
            print('{} \nAverage Rating:{}\n{}\n'.format(
                id_to_title(y), movies[y[0]].avg_rating, movies[y[0]].link))
        if next_results():
            continue
        else:
            break


def show_top_recommended():
    """Displays the movies with highest
     recommended score based on other users"""
    x = 0
    user_num = input('Please Enter your ID\n')
    while user_num not in user_list:
        user_num = input('Please Enter a valid ID\n')
    answer = 'n'
    while answer == 'n' or answer == 'next':
        x += 5
        top_movies = (
            movies_not_seen(user_num, user_like_users(user_num, user_list),
                            idx=x))
        for movie in top_movies:
            print('\n{} \nAverage Rating: {}\nGuess for you: {}\n{}'
                  .format(id_to_title(movie),
                          movies[movie[0]].avg_rating, movie[1],
                          movies[movie[0]].link))
        if next_results():
            continue
        else:
            break


def next_results():
    """Menu prompt for displaying the next set of results"""
    answer = input(('\nWould you like to see the [N]ext 5 results,'
                    '  or [E]xit to the Menu?\n')).lower()
    while answer != 'e':
        if answer == 'n' or answer == 'next':
            return True
        else:
            answer = input(
                'Please enter a valid choice("[N]ext or [E]xit)\n').lower()
    return False


def id_to_title(id_to_change):
    """converts a movies ID to the title of the movie"""
    return movies[id_to_change[0]].title


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
    print('*****Enjoy your movie*****')
