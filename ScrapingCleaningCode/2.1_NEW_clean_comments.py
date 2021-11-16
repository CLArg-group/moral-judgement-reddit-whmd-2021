import pandas as pd
import time

#############################################################################
####################################INPUT####################################

# select which scraped comments to process
comments_path = "RawScraped/raw_comments_combined.csv"

#############################################################################
#############################################################################

# Get the scraped comments that you want to clean
df = pd.read_csv(comments_path)
df.set_index("id", inplace=True)
num_initial_comments = len(df)
df_dict = df.to_dict()


# Identify low rated comments
start_time = time.time()
print("Identifying low-rated comments...")
ids_to_drop = set()
for comment_id, comment_score in df_dict['score'].items():
    if int(comment_score) < 3:
        ids_to_drop.add(comment_id)
print("--- %s seconds ---" % (time.time() - start_time))
print()


# Identify very short comments
start_time = time.time()
print("Identifying short comments...")
for comment_id, comment_body in df_dict['body'].items():
    if len(str(comment_body)) < 12:
        ids_to_drop.add(comment_id)
print("--- %s seconds ---" % (time.time() - start_time))
print()


# Drop appropriate comments
ids_to_drop_list = list(ids_to_drop)
df.drop(index=ids_to_drop_list, inplace=True)

num_dropped_comments = len(ids_to_drop_list)
num_remaining_comments = len(df)

print("Initially, there were {} comments!".format(num_initial_comments))
print("A total of {} comments were then dropped on account of their length or score!".format(num_dropped_comments))
print("This leaves us with {} comments!".format(num_remaining_comments))

df.to_csv('NewAttempt/all_comments_cleaned.csv', index=True)