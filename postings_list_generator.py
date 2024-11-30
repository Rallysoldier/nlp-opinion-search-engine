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
            postings_list[word].add(index)
    
    # Convert defaultdict(set) to a regular dictionary with lists for saving, sort everything
    postings_list = {word:sorted(list(indices)) for word, indices in sorted(postings_list.items())}
    return postings_list

def create_review_metadata(reviews_segment_df):
    """
    Create a metadata dictionary for reviews, keyed by review index.
    """
    metadata = {}

    for index, row in reviews_segment_df.iterrows():
        metadata[index] = {
            "customer_review_rating": row.get("customer_review_rating", None), 
            "text": row.get("review_text", ""),  
        }

    return metadata

def run_diagnostic(posting_filename, metadata_fileame):
    # Load the posting_list.pkl file
    with open(posting_filename, "rb") as f:
        posting_list = pickle.load(f)

    # Load the review_metadata.pkl file
    with open(metadata_fileame, "rb") as f:
        review_metadata = pickle.load(f)

    print(f"customer_review_rating: {review_metadata[0]['customer_review_rating']}")

def main():
    
    # Set diagnostic to True to skip regeneration, run diagnostic
    diagnostic = True
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

