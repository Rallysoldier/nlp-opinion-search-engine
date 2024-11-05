import pandas as pd
import argparse
import random

def _sample_reviews(reviews_df, review_indices, max_sample_size=5):
    """Display a random sample of reviews based on provided indices."""
    if max_sample_size > 0:
        sample_size = min(max_sample_size, len(review_indices))  # Limit sample size
        sample_indices = random.sample(review_indices, sample_size)
        
        print("\nSample reviews:")
        for index in sample_indices:
            print(f"\nReview at index {index}:")
            print(reviews_df.loc[index, "review_text"])  # Display the review text
            print("----")
    else:
        return

def main():
    parser = argparse.ArgumentParser(description="Check results against corpus")

    parser.add_argument("-f", "--file", type=str, required=True, help="The boolean search result pickle file to check")
    parser.add_argument("-t", "--terms", nargs="*", help="List of terms to check occurrences in matching reviews")
    parser.add_argument("-s", "--sample_size", type=int, default=5, help="Number of random reviews to sample for display")
    
    # Parse the arguments
    args = parser.parse_args()

    # Load the result file into result_df
    try:
        result_df = pd.read_pickle(args.file)
    except FileNotFoundError:
        print(f"\n!! Results file '{args.file}' not found !!\n")
        return

    # Extract the list of review indices from the result file
    review_indices = result_df["review_index"].tolist()

    # Load the reviews data
    reviews_df = pd.read_pickle("reviews_segment.pkl")

    # Filter the reviews DataFrame to include only the relevant rows
    matching_reviews = reviews_df.loc[review_indices]

    # Display summary statistics
    print(f"\nSummary for file '{args.file}':")
    print(f"Total reviews in corpus: {len(reviews_df)}")
    print(f"Total reviews matched in results file: {len(matching_reviews)}")

    # Display term-specific counts if terms are provided
    if args.terms:
        for term in args.terms:
            term_count = matching_reviews['review_text'].str.contains(term, case=False).sum()
            print(f"Reviews containing '{term}': {term_count}")

    # Display sample reviews for manual verification
    _sample_reviews(reviews_df, review_indices, args.sample_size)

if __name__ == "__main__":
    main()
