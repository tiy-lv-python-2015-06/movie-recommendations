import csv
import itertools


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
    return movie_details_dict[movie_id]['movie_title']

def find_movie_titles_given_list(list):
    """Given ('121', 4) list, Returns list, replacing movie titles where there were movie_ids"""
    # [('688', 1.84), ('368', 1.9), ('890', 1.95), ('743', 1.95)]
    pass


def find_all_ratings_for_movie(movie_id):
    # user_id | item_id | rating | timestamp
    # Find all ratings for a movie by id
    # Args: movie_id (String)   Return: ratings_list (List of Ints) => [3,5,2,1,2,3,4,5]
    movie_user_ratings_list = load_movie_user_cross_reference()
    its_ratings_list = []
    for rating_item in movie_user_ratings_list:
        if rating_item[1] == movie_id:
            its_ratings_list.append(int(rating_item[2]))
    return its_ratings_list

def find_average_rating_for_movie(movie_id):
    #SUCCESS
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

    #Recommend the most popular movies.
    #Show the top X (40) movies by average rating with their rating
    #Movie must have been rated at least X (10) times

    #a function makes a dictionary of all movies key:value movie_id:frequency_of_ratings

def movie_ratings_frequency():
    """Returns LIST of TUPLES of ALL movies (movie_id, frequency_of_ratings)
    #   make dictionary of all 1682 load_movie_details()/movie_details_dict for X(1682 movies)times.
    # user_id | item_id | rating | timestamp"""
    movie_user_ratings_list = load_movie_user_cross_reference()
    all_movies_ratings_frequency = {}
    for movie in movie_user_ratings_list:
        if movie[1] not in all_movies_ratings_frequency:
            all_movies_ratings_frequency[(movie[1])] = 1
        else:
            all_movies_ratings_frequency[(movie[1])] += 1
    return all_movies_ratings_frequency

def filter_for_minimum_number_of_ratings(min_number_of_ratings):
    # SUCCESS
    # for movie in dict
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

if __name__ == '__main__':

   # print(averages_of_all_movies())

 #   print(load_rating_data())
    print(filter_for_minimum_number_of_ratings(400))

    print("find_top_unviewed_movies('28')")
    print(find_top_unviewed_movies('28'))

    print("this is  find_movie_title('100')")
    print(find_movie_title('100'))
    print('---------------------')


    print("find_average_rating_for_movie('1080')")
    print(find_average_rating_for_movie('1080'))

    print("user_ratings_list is:")
    print("find_all_ratings_for_user('33')")
    print(find_all_ratings_for_user('33'))
    #
    # print(type(movie_details_dict))
    # print(movie_ratings_frequency()['100'])
    # movie_ratings_frequency_dict = movie_ratings_frequency()
    # print(len(movie_ratings_frequency_dict))
    # print((type(movie_ratings_frequency_dict)))
    # print("first 10 movies in movie_ratings_frequency_dict")
    # print(movie_ratings_frequency_dict['100'])
    # print('----------')
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
