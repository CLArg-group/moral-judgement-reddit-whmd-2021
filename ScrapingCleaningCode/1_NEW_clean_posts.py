import pandas as pd
import time

#############################################################################
####################################INPUT####################################

# select which scraped posts to process
posts_path = "RawScraped/posts_scraped.csv"

#############################################################################
#############################################################################

# Get the scraped posts
df = pd.read_csv(posts_path, dtype={"id":str, "timestamp":str, "title":str, "body":str, "edited":str, "verdict":str, "score":int, "num_comments":int})
df.set_index("id", inplace=True)
num_initial_posts = len(df)
df_dict = df.to_dict()


# Identify low rated posts
start_time = time.time()
print("Identifying low-rated posts...")
ids_to_drop = set()
for post_id, post_score in df_dict['score'].items():
    if int(post_score) < 3:
        ids_to_drop.add(post_id)
print("--- %s seconds ---" % (time.time() - start_time))
print()


# Identify very short posts
start_time = time.time()
print("Identifying short comments...")
for post_id, post_body in df_dict['body'].items():
    if len(str(post_body)) < 12:
        ids_to_drop.add(post_id)
print("--- %s seconds ---" % (time.time() - start_time))
print()


# Drop appropriate posts
ids_to_drop_list = list(ids_to_drop)
df.drop(index=ids_to_drop_list, inplace=True)

num_dropped_posts = len(ids_to_drop_list)
num_remaining_posts = len(df)

print("Initially, there were {} posts!".format(num_initial_posts))
print("A total of {} posts were then dropped on account of their length or score!".format(num_dropped_posts))
print("This leaves us with {} posts!".format(num_remaining_posts))

df.to_csv('NewAttempt/all_posts_cleaned.csv', index=True)