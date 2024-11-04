import pandas as pd
import argparse
import random

def _sample_reviews(max_sample_size, reviews_df, review_indices, matching_reviews):
    if max_sample_size > 0:
        sample_size = min(max_sample_size, len(matching_reviews))  # Limit sample size to 5 reviews
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

    parser.add_argument("-a1", "--aspect1", type=str, required=True, help="First word of the aspect")
    parser.add_argument("-a2", "--aspect2", type=str, required=True, help="Second word of the aspect")
    parser.add_argument("-o", "--opinion", type=str, required=True, help="Opinion word or phrase")
    parser.add_argument("-m", "--method", type=str, required=True, default=None, help="The method of the resulting boolean search file. Methods\
                        can be method1, method2 or method3")
    
    # Parse the arguments
    args = parser.parse_args()

    # Define the filename based on method
    result_filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_{args.method}.pkl"

    # Load the result file into result_df
    try:
        # Load the indices from the results file
        result_df = pd.read_pickle(result_filename)
    except FileNotFoundError:
        print(f"\n!! Results file '{result_filename}' not found !!\n")
        return
    
    # Extract the list of review indices from the result file
    review_indices = result_df["review_index"].tolist()

    # Load the reviews data
    reviews_df = pd.read_pickle("reviews_segment.pkl")

     # Filter the reviews DataFrame to include only the relevant rows
    matching_reviews = reviews_df.loc[review_indices]

     # Summary Statistics
    aspect1_count = matching_reviews['review_text'].str.contains(args.aspect1, case=False).sum()
    aspect2_count = matching_reviews['review_text'].str.contains(args.aspect2, case=False).sum()
    opinion_count = matching_reviews['review_text'].str.contains(args.opinion, case=False).sum()

    print(f"\nSummary for '{args.aspect1} {args.aspect2}:{args.opinion}' using {args.method}:")
    print(f"Total reviews: {len(reviews_df)}")
    print(f"Total reviews matched: {len(matching_reviews)}")
    print(f"Reviews containing '{args.aspect1}': {aspect1_count}")
    print(f"Reviews containing '{args.aspect2}': {aspect2_count}")
    print(f"Reviews containing '{args.opinion}': {opinion_count}\n")

    # Sample display of matching reviews for manual verification
    max_sample_size = 0
    _sample_reviews(max_sample_size, reviews_df, review_indices, matching_reviews)

if __name__ == "__main__":
    main()

'''
TERMINAL:
 python bs_checker.py --aspect1 audio --aspect2 quality --opinion poor --method method1
 python bs_checker.py --aspect1 audio --aspect2 quality --opinion poor --method method2
 python bs_checker.py --aspect1 audio --aspect2 quality --opinion poor --method method3
'''