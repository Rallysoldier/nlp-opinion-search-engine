import pandas as pd
from collections import defaultdict
import pickle
import re

def create_postings_list(reviews_segment_df):
    postings_list = defaultdict(set)  # Use set to avoid duplicate indices

    # Iterate over each review in the df
    for index, row in reviews_segment_df.iterrows():
        review_text = row['review_text']
        
        # Tokenize
        words = re.findall(r'\b\w+\b', review_text.lower())
        
        # Add each word to the postings list with the current review index
        for word in words:
            postings_list[word].add(index+2)
    
    # Convert defaultdict(set) to a regular dictionary with lists for saving, sort everything
    postings_list = {word:sorted(list(indices)) for word, indices in sorted(postings_list.items())}
    return postings_list

def create_review_metadata(reviews_segment_df):
    """
    Create a metadata dictionary for reviews, keyed by review index.
    """
    metadata = {}

    for index, row in reviews_segment_df.iterrows():
        metadata[index+2] = {
            "customer_review_rating": row.get("customer_review_rating", None), 
            "text": row.get("review_text", ""),  
        }
    return metadata

def run_diagnostic(posting_filename, metadata_fileame):
    # Read data into variable
    with open("reviews_segment.pkl", "rb") as f:
        reviews_segment = pickle.load(f)
    # Check the structure of reviews_segment.pkl
    print(f"reviews_segment.pkl: {type(reviews_segment)}")
    # Create DF from Pickle
    reviews_segment_df = pd.DataFrame(list(reviews_segment.items()), columns=["Word", "Review_IDs"])
    # Sample corpus
    print(f"reviews segment sample: {reviews_segment_df.head()}")

    # Read data into variable
    with open("posting_list.pkl", "rb") as f:
        posting_list = pickle.load(f)
    # Check the structure of posting_list
    print(f"posting_list.pkl: {type(posting_list)}")
    # Create DF from Pickle
    posting_list_df = pd.DataFrame(list(posting_list.items()), columns=["Word", "Review_IDs"])
    # Sample posting list
    print(f"posting list sample: {posting_list_df.sample(5)}")

    # Read metadata into variable
    with open(metadata_fileame, "rb") as f:
        review_metadata = pickle.load(f)
    # Check structure of metadata
    print(type(review_metadata))
    # Create DF from Pickle
    review_metadata_df = pd.DataFrame(list(review_metadata.items()), columns=["IDs", "Reviews with Metadata"])
    # Sample metadata
    print(f"metadata: {review_metadata_df.sample(5)}")

    custom_diagnostic(posting_list_df, review_metadata_df)

def custom_diagnostic(posting_list_df, review_metadata_df):
    """
    Prompts the user for a word, retrieves the corresponding row from posting_list_df,
    and saves the list of ID's where the word appears. 
    Then Prompts the user to choose an ID within that list--which is searched for in the
    review_metadata_df. If found, the row is displayed.
    """
    # Prompt the user for a word
    word = input("Enter a word to lookup: ")
    # Check if the word is a key in the posting list
    if word in posting_list_df["Word"].values:
        # Retrieve the row corresponding to the word
        row = posting_list_df.loc[posting_list_df["Word"] == word]
        print(f"Word found:\n {row}")

        # Extract and return the value from the second column
        ID_list = row["Review_IDs"].iloc[0]  # Assuming the column is named 'Review_IDs'
        print(ID_list[0], type(ID_list[0]))

        # Prompt for the indice of the desired ID in the posting_list
        ID = int(input("Search for Review by ID: "))
        if ID in ID_list:
            pass
        else:
            print(f"The ID {ID} was not found in posting_list_df.")
            return None
        
        # Retrieve the row from review_metadata_df corresponding to the review ID
        meta_row = review_metadata_df.loc[review_metadata_df["IDs"] == ID]
        print(f"Metadata found: {meta_row}")
    else:
        print(f"The word '{word}' was not found in posting_list_df.")
        return None

def main():

    # Regenerate posting_list.pkl and review_metadata.pkl, or run diagnostic
    diagnostic:bool = None
    while(diagnostic == None):
        user_input = input("Regenerate: 0\nDiagnostic: 1\nPlease enter 0 or 1: ")
        if user_input == '0':
            print("Regenerating... \n")
            diagnostic = False
        elif user_input == '1':
            print("Running Diagnostic...\n")
            diagnostic = True
        elif user_input == 'exit':
            return -1
        else:
            print("Invalid Input\n")
            continue

    if not diagnostic:
        # Load the reviews_segment
        reviews_segment_df = pd.read_pickle("reviews_segment.pkl")
        
        # Create the postings list
        postings_list = create_postings_list(reviews_segment_df)
        
        # Save the postings list to a file
        with open("posting_list.pkl", "wb") as f:
            pickle.dump(postings_list, f)
        
        print("Postings list created and saved as 'posting_list.pkl'")

        # Create the review metadata
        review_metadata = create_review_metadata(reviews_segment_df)
        
        # Save the review metadata to a file
        with open("review_metadata.pkl", "wb") as f:
            pickle.dump(review_metadata, f)

        print("Metadata saved as 'review_metadata.pkl'")

        # Check ID consistency
        postings_indices = set(index for indices in postings_list.values() for index in indices)
        metadata_indices = set(review_metadata.keys())
        assert postings_indices == metadata_indices, "Index mismatch detected!"
    else:
        run_diagnostic('posting_list.pkl', 'review_metadata.pkl')

if __name__ == "__main__":
    main()

