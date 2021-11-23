import pandas as pd
import time
import re

start_time = time.time()
print("Reading the comments csv as a dataframe...")
df = pd.read_csv("NewAttempt/comments_with_verdict_automod_cleaned.csv", dtype={"id":str, "Unnamed: 0":int, "score":int, "parent_id":str, "created_utc":str, "body":str, "author_flair_text":str, "verdict":str})
df.set_index("id", inplace=True)
print("There are {} comments!".format(len(df)))
print("--- %s seconds ---" % (time.time() - start_time))
print()

df_dict = df.to_dict()

# Remove the etiquettes from the comments.
query = "( *[^a-zA-Z0-9]*YTA[^a-zA-Z0-9]* *)|( *[^a-zA-Z0-9]*NTA[^a-zA-Z0-9]* *)|( *[^a-zA-Z0-9]*ESH[^a-zA-Z0-9]* *)|( *[^a-zA-Z0-9]*NAH[^a-zA-Z0-9]* *)" # Note: I added these blanks to remove them from the start of target sentences. Did it work? Yes!
comment_bodies_no_etiquettes = []
for comment_id, comment_body in df_dict["body"].items():
    comment_bodies_no_etiquettes.append(re.sub(query, " ", comment_body))

df['body'] = comment_bodies_no_etiquettes

start_time = time.time()
print("Saving the dataframe of the {} comments for grasp!".format(len(df)))
df.to_csv('NewAttempt/FinalForBert/comments_for_bert_no_etiquettes.csv', index=True, index_label="id")
print("--- %s seconds ---" % (time.time() - start_time))
print()