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
    Batch 1 = January 1, 2023 - January 31, 2022
    Batch 2 = February 1, 2022 - February 28, 2022
    Batch 3 = March 1, 2022 - March 33, 2022
    Batch 4 = April 1, 2022 - April 30, 2022
    Batch 5 = May 1, 2022 - May 24, 2022
    """
    keyword = '((e-vehicle OR ev OR "electric vehicle" OR "kendaraan listrik" OR "mobil listrik" OR "motor listrik" OR tesla OR "wuling air ev" OR "renault twizy" OR "nissan leaf" OR "hyundai ioniq") (harga OR mahal OR murah OR biaya OR performa OR "jarak tempuh" OR kilometer OR km OR awet OR irit OR hemat OR fitur OR canggih OR mesin OR akselerasi OR torsi OR kecepatan OR nyaman OR enak OR charging OR charge OR cas OR baterai OR battery OR "charging station" OR "stasiun pengisian kendaraan listrik umum" OR spklu OR pln OR stasiun OR infrastruktur OR nikel OR pertamina OR insentif OR subsidi OR pajak OR pemerintah OR kebijakan OR peraturan OR lingkungan OR emisi OR karbondioksida OR polusi OR energi OR co2 OR iklim)) lang:id -is:retweet'
    start_list = ['2023-01-01',
                 '2023-02-01',
                 '2023-03-01',
                 '2023-04-01',
                 '2023-05-01',
                 '2023-06-01']

    end_list =   ['2023-01-31',
                 '2023-02-28',
                 '2023-03-31',
                 '2023-04-30',
                 '2023-05-31',
                 '2023-06-30']
    
    max_tweets = 100
    max_request = 500
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

        # if i != len(start_list):
        #     time.sleep(930) # Give 15+ Minutes delay for every time period
        # else:
        #     continue

    with open('data/data.json', 'w') as f:
        json.dump(tweets, f)

    for k in range (0, len(tweets)):
        total_tweets += tweets[k]['meta'].get('result_count')

    print("Total number of results: ", total_tweets)