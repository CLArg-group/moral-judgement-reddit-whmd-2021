import pandas as pd
import time

#############################################################################
####################################INPUT####################################

# select which scraped comments to process
comments_path = "NewAttempt/comments_with_verdict_cleaned.csv"

#############################################################################
#############################################################################

# Get the scraped comments that you want to clean
start_time = time.time()
print("Reading the comments csv as a dataframe...")
df = pd.read_csv(comments_path, dtype={"score":int, "parent_id":str, "created_utc":str, "body":str, "author_flair_text":str, "verdict":str})
num_initial_comments = len(df)
print("There are {} comments in the dataframe!".format(num_initial_comments))
print("--- %s seconds ---" % (time.time() - start_time))
print()
df_dict = df.to_dict()


# Identify the verdicts in comments
start_time = time.time()
print("Identifying the automod comments...")
automod_com_ids = set()
for comment_id, comment_body in df_dict['body'].items():
    if "^^^AUTOMOD" in comment_body:
        automod_com_ids.add(comment_id)
print("There were {} automod comments. These will be dropped!".format(len(automod_com_ids)))
print("--- %s seconds ---" % (time.time() - start_time))
print()

# Drop appropriate comments
ids_to_drop_list = list(automod_com_ids)
df.drop(index=ids_to_drop_list, inplace=True)

start_time = time.time()
print("Saving the dataframe of the remaining {} comments enriched with verdicts!".format(len(df)))
df.to_csv('NewAttempt/comments_with_verdict_automod_cleaned.csv', index=True)
print("--- %s seconds ---" % (time.time() - start_time))
print()