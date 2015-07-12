import csv
import itertools
import math
import numpy


def load_movie_details():
    #NOTE: I normalized u.items by putting these headers in it:
    #movie_id|movie_title|release_date|video_release_date|imdb_url|
    # unknown|action|adventure|animation|childrens|comedy|crime|documentary|
    # drama|fantasy|film_noir|horror|musical|mystery|romance|sci_fi|thriller|war|western
    with open("u.item") as file:
        reader = csv.DictReader(file, delimiter="|")
        movie_details_dict = {row["movie_id"]: row for row in reader}
        return movie_details_dict


def load_movie_user_cross_reference():
    """LIST of lists of:  user_id | item_id | rating | timestamp"""
    # this HAS to be a list because there is no unique identifier!
    with open("u.data") as file:
        reader = csv.reader(file, delimiter="\t")
        movie_user_ratings_list = [row for row in reader]
    return movie_user_ratings_list


def load_rating_data():
    with open("u.info") as file:
        reader = csv.reader(file)
        return [(row) for row in reader]


def find_movie_title(movie_id):
    # Find the name of a movie by id
    # Args: movie_id (String)    Return: movie_title (String)   => Celestial Clockwork (1994)
    return load_movie_details()[movie_id]['movie_title']

def find_movie_titles_given_list(list):
    """Given ('121', 4) list, Returns list, replacing movie titles where there were movie_ids"""
    # [('688', 1.84), ('368', 1.9), ('890', 1.95), ('743', 1.95)]
    pass


def find_all_ratings_for_movie(movie_id):
    # user_id | item_id | rating | timestamp
    # Find all ratings for a movie by id
    # Args: movie_id (String)   Return: ratings_list (List of Ints) => [3,5,2,1,2,3,4,5]
    movie_user_ratings_list = load_movie_user_cross_reference()
    its_ratings_list = [
        int(rating_item[2])
        for rating_item in movie_user_ratings_list
        if rating_item[1] == movie_id
    ]
    return its_ratings_list

def find_average_rating_for_movie(movie_id):
    # Find the average rating for a movie by id
    its_ratings_list = find_all_ratings_for_movie(movie_id)
    raw_average = sum(its_ratings_list)/len(its_ratings_list)
    return round(raw_average, 2)


def find_all_ratings_for_user(user_id):
    #Find all ratings and movies a user has rated
    #Args: user_id (String)  Return: {user_id: {{movie_id: rating}} Dict of dicts => {'203':{'333':4},{'888':2}}
    # user_id | item_id | rating | timestamp
    # d = {key: value for (key, value) in iterable}
    movie_user_ratings_list = load_movie_user_cross_reference()
    user_ratings_dict = {}
    user_ratings_dict[user_id] = {}
    for item in movie_user_ratings_list:
        if item[0] == user_id:
            user_ratings_dict[user_id][item[1]] = item[2]
    return user_ratings_dict


def movie_ratings_frequency():
    """Returns dict of ALL movies (movie_id, frequency_of_ratings)
    #   make dictionary of all 1682 load_movie_details()/movie_details_dict for X(1682 movies)times.
    # cross reference list = user_id | item_id | rating | timestamp"""
    movie_user_ratings_list = load_movie_user_cross_reference()
    all_movies_ratings_frequency = {}
    for movie in movie_user_ratings_list:
        if movie[1] not in all_movies_ratings_frequency:
            all_movies_ratings_frequency[(movie[1])] = 1
        else:
            all_movies_ratings_frequency[(movie[1])] += 1
    return all_movies_ratings_frequency

def filter_for_minimum_number_of_ratings(min_number_of_ratings):
    simple_dict = {"a":{"foo":"bar"}, "b":{"bar":"foo"}}
    movie_ratings_dict = movie_ratings_frequency()
    filtered_dict = {}
    for key, value in movie_ratings_dict.items():
        if int(value) >= min_number_of_ratings:
            filtered_dict[key] = value
    #print(filtered_dict)
    return filtered_dict


def averages_of_all_movies():
    dict_of_movies_and_ratings = filter_for_minimum_number_of_ratings(200)
    movie_averages_dict = {}
    for key, value in dict_of_movies_and_ratings.items():
        movie_averages_dict[key] = find_average_rating_for_movie(key)
    return movie_averages_dict


def find_top_unviewed_movies(user_id):
    """Given dict of all movie averages, return sorted list of top movies user not seen, sorted by average first"""
    movie_averages_dict = averages_of_all_movies()
    viewed_movies_dict = find_all_ratings_for_user(user_id)
    for key, value in viewed_movies_dict.items():
        if key in viewed_movies_dict:
            del movie_averages_dict[key]
    sorted_movie_list = sorted(movie_averages_dict, key=movie_averages_dict.get, reverse=True)[:40]
    sorted_movie_dict = {}
    #get averages for all movies in that list
    for movie_id in sorted_movie_list:
        sorted_movie_dict[movie_id] = find_average_rating_for_movie(movie_id)
    return sorted_movie_dict

def find_common_movies(first_user, second_user):
    """Given 2 user_id's, find common movies, return a common list of movies. JUST ONE LIST OF MOVIE IDS
    RETURN: common_list is [('268', '5'), ('288', '4')]
    """
    first_user_dict = find_all_ratings_for_user(first_user)
    # common_dict = first_user_dict
    second_user_dict = find_all_ratings_for_user(second_user)
    first_user_list = first_user_dict[first_user]
    second_user_list = second_user_dict[second_user]
    #return first_user_dict
    first_user_set = set(first_user_list)
    second_user_set = set(second_user_list)
    common_list = [ key for key in first_user_set.intersection(second_user_set) ]
    print("user list 1{}".format(first_user_list))
    print("user list 1{} length".format(len(first_user_list)))
    print("user list 2{}".format(second_user_list))
    print("user list 2{} length".format(len(second_user_list)))
    common_list.sort()
    print("common_list length is {} ".format(len(common_list)))
    print("common_list is {}".format(common_list))


    return common_list
    #common_list is [('268', '5'), ('288', '4')]

def create_movie_ratings_list(common_movie_list, user_id):
    """Given a list of just movie_ids, create a list of (movie_id, rating) for that user"""
    user_common_movie_ratings_list = [
        get_user_rating_for_a_movie(movie_id, user_id)
        for movie_id in common_movie_list
        ]
    return user_common_movie_ratings_list


def get_user_rating_for_a_movie(movie_id, user_id):
    """Given a list of just movie_ids, return (movie_id,user_rating)"""
    # user_id | item_id | rating | timestamp
    # go thru the list of ratings for user_id
    all_ratings_for_user_dict = find_all_ratings_for_user(user_id)

    user_rating_for_a_movie = int(all_ratings_for_user_dict[user_id][movie_id])
    return user_rating_for_a_movie
    # make list of [(movie_id, user_rating), (movie_id, user_rating)

# to take two users and find their similarity.
# If you have a list of movie ratings for user 1 (v) and a list for user 2 (w),
# where each list is made up of ratings for movies they've both seen in the same order,
# then you can use this formula:

def euclidean_distance(first_user_list, second_user_list):
    """Given two lists of user ratings of the same movies, return the Euclidean distance between them on a scale
    of 0 to 1. 1 means the two lists are identical.
    """
    # Guard against empty lists.
    if len(first_user_list) is 0:
        return 0
    # Note that this is the same as vector subtraction.
    differences = [first_user_list[idx] - second_user_list[idx] for idx in range(len(first_user_list))]
    squares = [diff ** 2 for diff in differences]
    sum_of_squares = sum(squares)
    return 1 / (1 + math.sqrt(sum_of_squares))


def pearson_correlation(first_user_list, second_user_list):
    return numpy.corrcoef(first_user_list, second_user_list)[0, 1]

# Now that you can calculate the similarity between two users, add a new ability.
# Given a list of all users, find the users most similar to a specific user,
# and then recommend the highest rated movies from those users that the specific user hasn't seen.
# A good formula for figuring out movies that user might like the most is similarity * rating

def most_similar_user(user_id):
    """Given a user_id, does euclidian or pearson correlation to each user in the db, and returns the most """
    #for each in :

    pass

if __name__ == '__main__':

    # print(averages_of_all_movies())

    #   print(load_rating_data())
    # print(filter_for_minimum_number_of_ratings(400))
    #
    # print("find_top_unviewed_movies('28')")
    # print(find_top_unviewed_movies('28'))
    #
    # print("this is  find_movie_title('100')")
    # print(find_movie_title('100'))
    # print('---------------------')
    #
    # print("find_common_movies between two users")
    # print(find_common_movies('11', '33'))
    # print(find_common_movies('11','12'))
    # print(find_common_movies('100','150'))
    # print("create_movie_ratings_list(common_movie_list, user_id)")

    first_user_rated_common_list = (create_movie_ratings_list(find_common_movies('100','150'), '100'))
    second_user_rated_common_list = (create_movie_ratings_list(find_common_movies('100','150'), '150'))
    print(first_user_rated_common_list)
    print(second_user_rated_common_list)

    print("euclidean_distance between user 100 & 150")
    print(euclidean_distance(first_user_rated_common_list, second_user_rated_common_list))

    print("find_average_rating_for_movie('1080')")
    print(find_average_rating_for_movie('1080'))


    # print("{} has been rated {} times its average rating is {}".format(find_movie_title('100'),movie_ratings_frequency_dict['100'],find_average_rating_for_movie('100')))
    # filtered_movie_ratings_frequency_dict = filter_for_minimum_number_of_ratings(movie_ratings_frequency(), 400)
    # print(len(filter_for_minimum_number_of_ratings(400)))
    # print(filtered_movie_ratings_frequency_dict)
    # # #print(top_rated_movies_list(filter_for_minimum_number_of_ratings(movie_ratings_frequency(), 30))[0:10])
    # # # for all movies in the whole movie list:
    # # #     find_all_ratings_for_movie(movie_id)
    # #
    # all_movie_averages = (averages_of_all_movies(filtered_movie_ratings_frequency_dict))
    # print(all_movie_averages['100'])
    # #print(top_rated_movies_dict(filtered_movie_ratings_frequency_dict))
    # # print("{} big list of averaged movies".format(len(all_movie_averages)))
    # # top_unviewed_movies = (find_top_unviewed_movies(all_movie_averages, '33'))
    # # print("{} unviewed movies".format(len(top_unviewed_movies)))
    # # print(top_unviewed_movies)
    # # print('done')
