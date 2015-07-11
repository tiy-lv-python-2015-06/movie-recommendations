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
    with open("u.data") as file:
        reader = csv.DictReader(file, delimiter="\t")
        movie_user_ratings_dict = {row["user_id"]: row for row in reader}
        return movie_user_ratings_dict


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

# key is user value is a list of movies that they've rated

def find_all_ratings_for_movie(movie_id):
    # user_id | item_id | rating | timestamp
    # Find all ratings for a movie by id
    # Args: movie_id (String)   Return: ratings_list (List of Ints) => [3,5,2,1,2,3,4,5]
    #DONT PRINT this result it'll end in tears
    # movie_user_ratings_dict = {'1010': {'timestamp': '875072956', 'rating': '2', 'user_id': '1', 'movie_id': '94'}}
    its_ratings_list = []
    for item_dict in movie_user_ratings_dict:
        # if the key named 'movie_id' exists in that item row of movie_user_ratings_dict, append its value to its_ratings_list
        if movie_id in item_dict:
            print(item_dict[movie_id]['movie_id'])
        #
        # if int(item[1]) == int(movie_id):
        #     its_ratings_list.append(int(item[2]))
    return its_ratings_list


def find_average_rating_for_movie(movie_id):
    #SUCCESS
    # Find the average rating for a movie by id
    its_ratings_list = find_all_ratings_for_movie(movie_id)
    raw_average = sum(its_ratings_list)/len(its_ratings_list)
    return round(raw_average, 2)


def find_all_ratings_for_user(user_id):
    #Find all ratings and movies a user has rated
    #Args: user_id (String)  Return: (movie_id, rating) List of String Tuples => [(908,3),(777,5),(213,44)]
    # user_id | item_id | rating | timestamp
    # d = {key: value for (key, value) in iterable}
    user_ratings_dict = {

    }

    user_ratings_list = []
    for item in movie_user_ratings_list:
        if int(item[0]) == int(user_id):
            # (movie_id, rating)
            #user_ratings_list.append((int(item[1]),int(item[2])))
            user_ratings_list.append((item[1],int(item[2])))
    return user_ratings_list

    #Recommend the most popular movies.
    #Show the top X (40) movies by average rating with their rating
    #Movie must have been rated at least X (10) times

    #a function makes a dictionary of all movies key:value movie_id:frequency_of_ratings

def movie_ratings_frequency():
    """Returns LIST of TUPLES of ALL movies (movie_id, frequency_of_ratings)
    #   make dictionary of all 1682 load_movie_details()/movie_details_dict for X(1682 movies)times.
    # user_id | item_id | rating | timestamp"""

    # d = {key: value for (key, value) in iterable}
    all_movies_ratings_frequency = {}
    print("AHHHHH")
    print(movie_user_ratings_list[1])
    for movie in movie_user_ratings_list:
        if movie[1] not in all_movies_ratings_frequency:
            all_movies_ratings_frequency[(movie[1])] = 1
        else:
            all_movies_ratings_frequency[(movie[1])] += 1
    return sorted(all_movies_ratings_frequency.items(), key=lambda x :x[1], reverse=True)


def filter_for_minimum_number_of_ratings(movie_ratings_list, min_number_of_ratings):
    #SUCCESS
    #for movie in list
    return [movie for movie in movie_ratings_list if int(movie[1]) > min_number_of_ratings]
    # filtered_list = []
    # for idx, movie in enumerate(movie_ratings_list):
    #     if int(movie[1]) > min_number_of_ratings:
    #         filtered_list.append(movie)
    # return filtered_list


def averages_of_all_movies(list_of_movies_and_ratings):
    unsorted_filtered_movie_averages = [
        (movie[0], find_average_rating_for_movie(movie[0]))
        for movie in list_of_movies_and_ratings
     ]
    return sorted(unsorted_filtered_movie_averages, key=lambda x: x[1])


def find_top_unviewed_movies(list_of_movies_and_averages, user_id):
    """Given list of (movie_id,avg rating), return sorted subset of that list user has not seen"""
    #  Generate the list of movies user has rated, compare that against all movies and subtract movies viewed
    viewed_list = find_all_ratings_for_user(user_id)
    all_list = list_of_movies_and_averages
    print("user_id {} has seen {} movies in the list of {} movies )".format(user_id, len(viewed_list), len(all_list)))
    unviewed_list = all_list
    for viewed_movie in viewed_list: # go through just the list of a user's rated movies
        for total_movie in unviewed_list:
            if viewed_movie[0] == total_movie[0]:
                unviewed_list.remove(total_movie)
    unviewed_list_sorted = sorted(unviewed_list, key=lambda x: x[1])
    #return Top 40 Unviewed List Of Movies for that user!
    return unviewed_list_sorted[0:41]


# for each movie in your filtered_for_minimum_number_of_ratings() list
#   find_average_rating_for_movie(movie_id)
#   make that into a list of movie_id and average rating
#   find the highest in that list
if __name__ == '__main__':

    print(load_rating_data())

    movie_user_ratings_dict = load_movie_user_cross_reference()
    print("this is movie_user_ratings_dict['1']   :")
    print(movie_user_ratings_dict['1'])
    print("-------------------")

    movie_details_dict = load_movie_details()
    #clockwork = (movie_details_dict['1080']['movie_title'])
    print("this is movie_details_dict['1080']  : ")
    print(movie_details_dict['1080'])
    print('--------------------')

    print("this is  find_movie_title('333')")
    print(find_movie_title('333'))
    print('---------------------')

    print("find_all_ratings_for_movie('333')")
    print(find_all_ratings_for_movie('333'))
    #
    # print("find_average_rating_for_movie('1080)")
    # print(find_average_rating_for_movie('1080'))
    #
    # print("the following is movie_user_ratings_list[0]")
    # print(movie_user_ratings_list[0])
    #
    # print("user_ratings_list is:")
    # print("find_all_ratings_for_user(user_id)")
    # print(find_all_ratings_for_user('33'))
    #
    # #print(type(movie_details_dict))
    # #print(movie_ratings_frequency()['1080'])
    # movie_ratings_frequency_list = movie_ratings_frequency()
    # len(movie_ratings_frequency_list)
    # print(movie_ratings_frequency_list[0:10])
    # print('foo')
    # filtered_movie_ratings_frequency_list = filter_for_minimum_number_of_ratings(movie_ratings_frequency(), 30)
    # # print(len(filter_for_minimum_number_of_ratings(movie_ratings_frequency(), 30)))
    # print(filtered_movie_ratings_frequency_list)
    # #print(top_rated_movies_list(filter_for_minimum_number_of_ratings(movie_ratings_frequency(), 30))[0:10])
    # # for all movies in the whole movie list:
    # #     find_all_ratings_for_movie(movie_id)
    #
    # all_movie_averages = (averages_of_all_movies(filtered_movie_ratings_frequency_list))
    # #print(top_rated_movies_list(filtered_movie_ratings_frequency_list))
    # print("{} big list of averaged movies".format(len(all_movie_averages)))
    # top_unviewed_movies = (find_top_unviewed_movies(all_movie_averages, '33'))
    # print("{} unviewed movies".format(len(top_unviewed_movies)))
    # print(top_unviewed_movies)
    # print('done')
