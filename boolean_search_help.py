import pandas as pd
import argparse
import pickle
import re

# Load postings list
with open("posting_list.pkl", "rb") as f:
    postings_list = pickle.load(f)

# Load review metadata
with open("review_metadata.pkl", "rb") as f:
    review_metadata = pickle.load(f)

# Load positive words
with open("positive-words.txt", "r", encoding="utf-8") as f:
    positive_words = {line.strip() for line in f if line.strip()}

# Load negative words
with open("negative-words.txt", "r", encoding="utf-8") as f:
    negative_words = {line.strip() for line in f if line.strip()}

# Initialize positive and negative indexes
positive_index = set()
negative_index = set()

# Populate negative and positive indexes
def populate_sentiment_indexes():
    for ID in review_metadata:
        rating = review_metadata[ID]['customer_review_rating']
        if int(rating) > 3:
            positive_index.add(ID)
        else:
            negative_index.add(ID)

# Categorize the opinion using the opinion lexicon
def determine_positivity(opinion):
    if opinion in positive_words:
        return True
    elif opinion in negative_words:
        return False
    else:
        return None

def get_indices(term):
    """Retrieve the set of indices for a term from the postings list."""
    return set(postings_list.get(term, []))

# Method 1: OR operation on all terms
def method1(aspect1, aspect2, opinion):
    return list(get_indices(aspect1) | get_indices(aspect2) | get_indices(opinion))

# Method 2: AND operation on all terms
def method2(aspect1, aspect2, opinion):
    return list(get_indices(aspect1) & get_indices(aspect2) & get_indices(opinion))

# Method 3: OR on aspects, AND with opinion
def method3(aspect1, aspect2, opinion):
    return list((get_indices(aspect1) | get_indices(aspect2)) & get_indices(opinion))

def M1_rating_search(positivity, result):
    ''' Filter for positive/negative review ratings using opinion lexicon '''
    if positivity:
        result_index = set(result)
        return list(result_index & positive_index)
    elif not positivity:
        result_index = set(result)
        return list(result_index & negative_index)
    else:
        return result

def M2_ratio_filter(positivity, result):
    ''' Calculate a Positive/Negative word ratio for each review, filtering matching reviews with undesireable ratios '''
    ratioed_result = []
    for ID in result:
        review_text = review_metadata[ID]["text"]
        ratio = get_ratioed(review_text)
        if positivity and ratio is not None and ratio > 0.5:
            ratioed_result.append(ID)
        elif not positivity and ratio is not None and ratio <= 0.5:
            ratioed_result.append(ID)

    if len(ratioed_result) > 0:
        return ratioed_result
    else:
        return result

def get_ratioed(review_text):
    ''' M2 helper function that calculates the positive word to negative word ratio in a single review'''
    # Tokenize and Count
    words = re.findall(r'\b\w+\b', review_text.lower())
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    # Calculate ratio
    total_count = positive_count + negative_count
    if total_count == 0:
        return None  # No sentiment words found
    return positive_count / total_count

def combine_methods(result1, result2):
    return list(set(result1) & set(result2))

def main():

    parser = argparse.ArgumentParser(description="Perform the boolean search.")

    parser.add_argument("-a1", "--aspect1", type=str, required=True, default=None, help="First word of the aspect")
    parser.add_argument("-a2", "--aspect2", type=str, required=True, default=None, help="Second word of the aspect")
    parser.add_argument("-o", "--opinion", type=str, required=True, default=None, help="Only word of the opinion")
    parser.add_argument("-m", "--method", type=str, required=True, default=None, help="The method of boolean operation. Methods\
                        can be method1, method2 or method3")

    # Parse the arguments
    args = parser.parse_args()

    # Populate positive_index and negative_index
    populate_sentiment_indexes()

    # Bool that records the polarity of the opinion
    positivity = determine_positivity(args.opinion)

    ''' Baseline '''
    if args.method.lower() == "method1":
        result = method1(args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method2":
        result = method2(args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method3":
        result = method3(args.aspect1, args.aspect2, args.opinion)
    else:
        print("\n!! The method is not supported !!\n")
        return
    
    ''' M1: 4.2: Boolean and Rating Search '''
    M1_result = M1_rating_search(positivity, result)

    ''' M2: 4.4(b): Grammar and Structure Based Relevance using Review Title and Sentence Structure '''
    M2_result = M2_ratio_filter(positivity, result)

    ''' M1 + M2: AND operation on M1_result and M2_result '''
    combined_result = combine_methods(M1_result, M2_result)

    # Choose method for final output. result for baseline.
    final_result = result

    # Output final result to pkl if diagnostic is False
    diagnostic = True
    if not diagnostic:
        revs = pd.DataFrame()
        revs["review_index"] = final_result
        output_filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_{args.method}.pkl"
        revs.to_pickle(output_filename)
        print(f"Results saved to {output_filename}")
    else:
        print(f"{result}\n{M1_result}\n{M2_result}\n{combined_result}\n")
        print(f"Length of Baseline: {len(result)}")
        print(f"Length of M1_result: {len(M1_result)}")
        print(f"Length of M2_result: {len(M2_result)}")
        print(f"Length of combined result: {len(combined_result)}")

if __name__ == "__main__":
    main()
