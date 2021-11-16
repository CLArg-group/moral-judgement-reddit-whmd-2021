import pandas as pd
from pmaw import PushshiftAPI
import datetime as dt
import time

######################################################################################
######################################################################################

start_year = 2014
end_year = 2014
after = int(dt.datetime(end_year, 11, 1, 0, 0).timestamp())
before = int(dt.datetime(end_year, 12, 31, 23, 59).timestamp())
subreddit = "AmItheAsshole"
limit = None
limit_type = "average"  # in {"average", "backoff"}

######################################################################################
######################################################################################

# Scrape the comments
if limit_type == "average":
    api = PushshiftAPI(num_workers=20, limit_type='average', rate_limit=75, max_sleep=50)
elif limit_type == "backoff":
    api = PushshiftAPI(num_workers=20, limit_type='backoff', jitter='full')
else:
    raise ValueError

# 12 seconds for 1000 comments => ~ 55 hours for 16,000,000 comments from 1 year. (before rate_limit)
start_time = time.time()
comments = api.search_comments(subreddit=subreddit, limit=limit, before=before, after=after, mem_safe=True)
print(f'Retrieved {len(comments)} comments from Pushshift')
print("--- %s seconds ---" % (time.time() - start_time))

# Put the scraped comments in a dataframe
comments_df = pd.DataFrame(comments)

# From the dataframe keep only the columns you want
comments_df_selected = comments_df[["score", "parent_id", "id", "created_utc", "body", "author_flair_text"]]
del comments_df

# Save the dataframe as a .csv file
comments_df_selected.to_csv('comments{}-{}_testttt.csv'.format(str(start_year), str(end_year)), header=True, index=False, columns=list(comments_df_selected.axes[1]))
