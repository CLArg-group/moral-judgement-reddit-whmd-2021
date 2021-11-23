import pandas as pd
import time


start_time = time.time()
print("Reading the comments csv as a dataframe...")
df_comments = pd.read_csv("NewAttempt/FinalForBert/comments_for_bert_no_etiquettes.csv", dtype={"id":str, "Unnamed: 0":int, "score":int, "parent_id":str, "created_utc":str, "body":str, "author_flair_text":str, "verdict":str})
df_comments.drop(columns=["Unnamed: 0", "created_utc", "author_flair_text"], inplace=True)
df_comments.set_index("id", inplace=True)
print("There are {} comments in the dataframe!".format(len(df_comments)))
print("--- %s seconds ---" % (time.time() - start_time))
print()

list_of_zeros = [0 for _ in range(df_comments.shape[0])]
df_comments['is_asshole'] = list_of_zeros

df_comments_dict = df_comments.to_dict()

start_time = time.time()
print("Deriving the is_asshole of the {} comments!".format(len(df_comments)))
for comment_id, comment_verdict in df_comments_dict["verdict"].items():
    if comment_verdict == "YTA" or comment_verdict == "ESH":
        df_comments_dict["is_asshole"][comment_id] = 1
    else:
        df_comments_dict["is_asshole"][comment_id] = 0
print("--- %s seconds ---" % (time.time() - start_time))
print()

df_comments = pd.DataFrame.from_dict(df_comments_dict)

start_time = time.time()
print("Saving the dataframe of the {} comments!".format(len(df_comments)))
df_comments.to_csv('NewAttempt/FinalForBert/comments_for_bert_no_etiquettes_with_parents.csv', index=True, index_label="id")
print("--- %s seconds ---" % (time.time() - start_time))
print()