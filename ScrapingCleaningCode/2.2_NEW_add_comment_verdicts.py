import pandas as pd
import time

#############################################################################
####################################INPUT####################################

# select which scraped comments to process
comments_path = "NewAttempt/all_comments_cleaned.csv"

#############################################################################
#############################################################################

# Get the scraped comments that you want to clean
start_time = time.time()
print("Reading the comments csv as a dataframe...")
df = pd.read_csv(comments_path, dtype={"score":int, "parent_id":str, "id":str, "created_utc":str, "body":str, "author_flair_text":str})
df.set_index("id", inplace=True)
num_initial_comments = len(df)
print("There are {} comments in the dataframe!".format(num_initial_comments))
print("--- %s seconds ---" % (time.time() - start_time))
print()
df_dict = df.to_dict()


# Identify the verdicts in comments
start_time = time.time()
print("Identifying the verdicts of comments...")
id_verdict_dict = dict()
unknown_verdict_com_ids = set()
for comment_id, comment_body in df_dict['body'].items():
    if "nta" in comment_body.lower():
        id_verdict_dict[comment_id] = "NTA"
    elif "yta" in comment_body.lower():
        id_verdict_dict[comment_id] = "YTA"
    elif "nah" in comment_body.lower():
        id_verdict_dict[comment_id] = "NAH"
    elif "esh" in comment_body.lower():
        id_verdict_dict[comment_id] = "ESH"
    else:
        unknown_verdict_com_ids.add(comment_id)
print("There were {} comments with unknown verdicts. These will be dropped!".format(len(unknown_verdict_com_ids)))
print("There were {} comments with identifiable verdict. These will be kept!". format(len(id_verdict_dict)))
print("--- %s seconds ---" % (time.time() - start_time))
print()

# Drop appropriate comments
ids_to_drop_list = list(unknown_verdict_com_ids)
df.drop(index=ids_to_drop_list, inplace=True)
list_of_empty_strings = ["" for _ in range(df.shape[0])]
df["verdict"] = list_of_empty_strings

start_time = time.time()
print("Adding the verdicts to the comments...")
df_dict = df.to_dict()
for comment_id, comment_verdict in id_verdict_dict.items():
    df_dict["verdict"][comment_id] = comment_verdict
print("--- %s seconds ---" % (time.time() - start_time))
print()

start_time = time.time()
print("Checking that all the remaining comments have indeed been assigned their verdict!")
all_comments_have_verdicts = True
for comment_id, comment_verdict in df_dict["verdict"].items():
    if len(comment_verdict) < 2:
        print(comment_verdict)
        all_comments_have_verdicts = False
print("--- %s seconds ---" % (time.time() - start_time))
print()

df = pd.DataFrame.from_dict(df_dict)

start_time = time.time()
print("Saving the dataframe of the remaining {} comments enriched with verdicts!".format(len(df)))
df.to_csv('NewAttempt/comments_with_verdict_cleaned.csv', index=True)
print("--- %s seconds ---" % (time.time() - start_time))
print()