from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:sec-002
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
# url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
# requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:

#Code for Part 3:Caching----------------------------------------------------------------
#Finish parts 1 and 2 and then come back to this
#using code from class
# on startup, try to load the cache from file
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_tweet_id(result_dict_list):
    tweet_id = []
    for aDict in result_dict_list:
        tweet_id.append(aDict['id_str'])
    return tweet_id


def params_unique_combination(username, tweet_id_list):
    return username + "-" + "_".join(tweet_id_list)


def make_request_using_cache(baseurl, params, auth, username):
    resp = requests.get(baseurl, params, auth=auth)
    resp_list = json.loads(resp.text)
    unique_ident = params_unique_combination(username, get_tweet_id(resp_list))

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        pass ## it's a cache miss, fall through to refresh code

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file

    print("Making a request for new data...")
    # Make the request and cache the new data
    CACHE_DICTION[unique_ident] = resp_list
    dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]


#extract just the 'text' from the data structures returned by twitter api
def get_text_list(tweet_dict_list):
    atweet = []
    for adict in tweet_dict_list:
            atweet.append(adict['text'])
    return atweet

def get_tweet(username, num_tweets, auth):
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name': username, 'count': num_tweets}
    return make_request_using_cache(base_url, params, auth, username)

def tweet_token(alist_with_text):
    tweet_tokenize = []
    for sentence in alist_with_text:
        tweet_tokenize.append(nltk.tokenize.word_tokenize(sentence))
    return tweet_tokenize

def filted_freqDist(tokenizedList):
    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dist = nltk.FreqDist()
    for tokened_sen in tokenizedList:
        for token in tokened_sen:
            if token not in stop_words and token.isalpha():
                freq_dist[token.lower()] += 1
    return freq_dist




if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()

    print('----------**Result for Extra 2**----------')

    # base_url_part2 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    # response_part2 = requests.get(base_url_part2, {'screen_name': username, 'count': num_tweets}, auth = auth).text
    # tweetDictList_part2 = json.loads(response_part2)
    # print(params_unique_combination(username, get_tweet_id(tweetDictList_part2)))
    try:
        tweet_whole_dictList = get_tweet(username, num_tweets, auth)
    except:
        print('Oops! Invalid username! Please try a different one. :)')
        quit()
    tweet_text_list = get_text_list(tweet_whole_dictList)
    if tweet_text_list != []:
        tokenized_list = tweet_token(tweet_text_list)
        print(filted_freqDist(tokenized_list).most_common(5))
    print('-----------------------------------------')
