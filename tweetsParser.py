import json
import csv
import pandas as pd
from tqdm import tqdm


def getUserDetails(tweet, users):
    tweet_author = str(tweet['author_id'])
    
    for user in users:
        user_values = str(user.get('id'))
        
        if tweet_author == user_values:
            return user
        else:
            continue
            
    return None

def getUserData(tweet, users):
    userDetails = getUserDetails(tweet, users)
    
    if userDetails != None:
        return {
            'username': userDetails['username'],
        }
    
    else:
        return {
            'username': None,
        }
    
def getReferencedTweets(tweet):
    if 'referenced_tweets' in tweet:
        if len(tweet['referenced_tweets']) >= 1:
            reference_type = []
               
            for reference_tweet in tweet['referenced_tweets']:
                reference_type.append(reference_tweet['type'])
            
        return reference_type
    
    else:
        return None
    
def generateTemp():
    return {
        'created_at': None,
        'author_id': None,
        'username' : None,
        'text': None,
        'reference_type': None,
    }

if __name__ == "__main__":
    #Load JSON file
    data = json.load(open('data.json'))

    data_tweets = []

    for i in tqdm(range (0, len(data))):
        for tweet in data[i]['data']:
            
            temp = generateTemp()

            temp.update({
                'created_at': tweet['created_at'],
                'author_id': tweet['author_id'],
                'username': getUserData(tweet, data[i]['includes']['users'])['username'],
                'text': tweet['text'],
                'reference_type': getReferencedTweets(tweet),
            })

            data_tweets.append(temp)

    df = pd.DataFrame(data_tweets)
    df.to_csv('data.csv', index=False)