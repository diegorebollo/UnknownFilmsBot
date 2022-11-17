from random import randint
from configparser import ConfigParser
import requests
import tweepy
import time

secrets = ConfigParser()
secrets.read('secrets.ini')

TMDB_API_KEY = secrets['tmdb']['api_key']
MIN_YEAR = 1969
MAX_YEAR = 2012
REGION = 'us'
SORT_BY = 'popularity.asc'
VOTE_COUNT = '50'
RUN_TIME = '70'

TW_API_KEY = secrets['twitter']['tw_api_key']
TW_API_SECRETS = secrets['twitter']['tw_api_secrets']
TW_ACCESS_TOKEN = secrets['twitter']['tw_access_token']
TW_ACCESS_SECRET = secrets['twitter']['tw_access_secret']


def get_random_film():
    year = randint(MIN_YEAR, MAX_YEAR)
    temp_api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&region={REGION}&sort_by={SORT_BY}&include_adult=false&include_video=false&page=500&primary_release_year={year}&vote_count.lte={VOTE_COUNT}&with_runtime.gte={RUN_TIME}&with_watch_monetization_types=flatrate'
    total_pages = requests.get(temp_api_url).json()['total_pages']
    page = randint(1, total_pages - 1)
    movie_number = randint(0, 19)
    api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&region={REGION}&sort_by={SORT_BY}&include_adult=false&include_video=false&page={page}&primary_release_year={year}&vote_count.lte={VOTE_COUNT}&with_runtime.gte={RUN_TIME}&with_watch_monetization_types=flatrate'
    movie = requests.get(api_url).json()['results'][movie_number]
    return movie


def get_director(movie_id):
    api_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US'
    crew = requests.get(api_url).json()['crew']
    for people in crew:
        if people['job'] == 'Director':
            director = people['name']
            return director


def make_tweet_text():
    film = get_random_film()
    film_id = film['id']
    director = get_director(film_id)
    title = film['title']
    release_date = film['release_date'].split('-')[0]
    overview = film['overview']

    tweat_text = f'{title} | {release_date} | {director}\n\n{overview}'

    return [tweat_text, film['poster_path']]


def post_tweet():
    auth = tweepy.OAuthHandler(TW_API_KEY, TW_API_SECRETS)
    auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_SECRET)
    api = tweepy.API(auth)

    while True:
        tweet_content = make_tweet_text()
        tweet_text = tweet_content[0]
        tweet_img = tweet_content[1]
        tweet_lenght = len(tweet_text)

        if tweet_lenght > 280 or tweet_img == None:
            print('finding another film')
            time.sleep(2)
        else:
            break

    img_poster = requests.get(
        f'https://image.tmdb.org/t/p/w500{tweet_img}').content

    with open('poster.jpg', 'wb') as f:
        f.write(img_poster)

    status = tweet_text
    image_path = 'poster.jpg'
    api.update_status_with_media(status, image_path)

    print(f'Tweet send: {tweet_text}')
    return 'Tweet sent'
