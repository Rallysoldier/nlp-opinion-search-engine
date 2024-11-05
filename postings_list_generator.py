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

def main():
    # Load the reviews_segment
    reviews_segment_df = pd.read_pickle("reviews_segment.pkl")
    
    # Create the postings list
    postings_list = create_postings_list(reviews_segment_df)
    
    # Save the postings list to a file
    with open("postings_list.pkl", "wb") as f:
        pickle.dump(postings_list, f)
    
    print("Postings list created and saved as 'postings_list.pkl'")
    
if __name__ == "__main__":
    main()

