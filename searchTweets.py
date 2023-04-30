from searchtweets import ResultStream, gen_request_parameters, load_credentials
from tqdm import tqdm
import json
import time


def create_query(keyword, start_date, end_date):
    print("Creating search query!!")
    query_params = gen_request_parameters(query = keyword,
                                          results_per_call = 500,
                                          granularity = None,
                                          start_time = start_date,
                                          end_time = end_date,
                                          expansions = 'author_id',
                                          tweet_fields = 'id,text,created_at,referenced_tweets',
                                          user_fields  = 'id,username'
                                          )
    return query_params


def stream(query, max_tweets, max_requests, search_args):
    print("The request is running!!")
    rs = ResultStream(request_parameters=query, max_tweets=max_tweets, max_requests=max_requests, **search_args)

    return list(rs.stream())


if __name__ == "__main__":
    search_args = load_credentials(filename='./twitter_keys.yaml',
                                   yaml_key='search_tweets_v2',
                                   env_overwrite=False)
    
    #Time period inputs for the request every 3 months
    """
    Batch 1 = January 1, 2022 - March 31, 2022
    Batch 2 = April 1, 2022 - June 30, 2022
    Batch 3 = July 1, 2022 - September 30, 2022
    Batch 4 = October 1, 2022 - December 31, 2022
    """
    keyword = "(e-vehicle OR (electric vehicle) OR (kendaraan listrik) OR (mobil listrik) OR (motor listrik) OR (bus listrik) OR #evehicle OR #electricvehicle OR #kendaraanlistrik OR #mobillistrik OR #motorlistrik OR #buslistrik) lang:id"
    start_list = ['2021-01-01',
                 '2021-04-01',
                 '2021-07-01',
                 '2021-10-01']

    end_list =   ['2021-03-31',
                 '2021-06-30',
                 '2021-09-30',
                 '2021-12-31']
    
    max_tweets = 60000
    max_request = 300
    count_request = 0
    tweets = []
    total_tweets = 0

    for i in tqdm(range(0,len(start_list))):
        #Counting tweets per time period
        count = 0

        #Create Query Parameters
        query = create_query(keyword, start_list[i], end_list[i])

        #Stream
        result = stream(query, max_tweets, max_request, search_args)
        tweets.extend(result)

        for j in range (0, len(result)):
            count += result[j]['meta'].get('result_count')
        
        print("Total Tweets Added from this time period: ", count)

        if i != len(start_list):
            time.sleep(930) # Give 15+ Minutes delay for every time period
        else:
            continue

    with open('data.json', 'w') as f:
        json.dump(tweets, f)

    for k in range (0, len(tweets)):
        total_tweets += tweets[k]['meta'].get('result_count')

    print("Total number of results: ", total_tweets)