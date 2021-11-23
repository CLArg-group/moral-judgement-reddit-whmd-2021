# We go through the pushshift API to get the ids of every post, then use the official reddit
# API to get the contents of each post and metadata of interest.
import requests
import json
import pandas as pd
import time
import datetime as dt

######################################################################################
######################################################################################

after = int(dt.datetime(2019, 1, 1, 0, 0).timestamp())
before = int(dt.datetime(2019, 12, 31, 23, 59).timestamp())

######################################################################################
######################################################################################

def getPushshiftData(after, before):
    url = 'https://api.pushshift.io/reddit/submission/search/?sort_type=created_utc&sort=asc&subreddit=amitheasshole&after='+ str(after) +"&before"+str(before)+"&size=1000"
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

scores = []
ids = []
created_utcs = []
titles = []
bodies = []
verdicts = []
editeds = []
nums_comments = []

while int(after) < before:
    data = getPushshiftData(after, before)
    print(data[0])
    for post in data:

        try:
            tmp_score = post['score']
        except:
            tmp_score = "NA"
        tmp_id = post['id']
        tmp_created_utc = post['created_utc']
        try:
            tmp_title = post['title']
        except:
            tmp_title = "NA"
        try:
            tmp_body = post['selftext']
        except:
            tmp_body = "NA"
        try:
            tmp_verdict = post['link_flair_text']
        except:
            tmp_verdict = "NA"
        try:
            tmp_edited = post['edited']
        except:
            tmp_edited = "NA"
        try:
            tmp_num_comments = post['num_comments']
        except:
            tmp_num_comments = "NA"

        scores.append(tmp_score)
        ids.append(tmp_id)
        created_utcs.append(tmp_created_utc)
        titles.append(tmp_title)
        bodies.append(tmp_body)
        verdicts.append(tmp_verdict)
        editeds.append(tmp_edited)
        nums_comments.append(tmp_num_comments)

    after = created_utcs[-1]
    print([str(len(ids)) + " posts collected so far."])
    time.sleep(0.1)

# Write to a csv file
d = {'id': ids, 'timestamp': created_utcs, 'title': titles, 'body': bodies, 'edited': editeds, 'verdict': verdicts, 'score': scores, 'num_comments': nums_comments}
df = pd.DataFrame(d)
df.to_csv("posts_scraped.csv", index=False)