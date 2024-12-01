import pandas as pd
import argparse
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load postings list
with open("posting_list.pkl", "rb") as f:
    postings_list = pickle.load(f)

# Load review metadata
with open("review_metadata.pkl", "rb") as f:
    review_metadata = pickle.load(f)

# Load Training Model
with open("sentiment_classifier.pkl", "rb") as f:
    model = pickle.load(f)

# Load tfidf 
with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

# Load positive words
with open("positive-words.txt", "r", encoding="utf-8") as f:
    positive_words = {line.strip() for line in f if line.strip()}

# Load negative words
with open("negative-words.txt", "r", encoding="utf-8") as f:
    negative_words = {line.strip() for line in f if line.strip()}

# Initialize positive/negative indexes
positive_index = set()
negative_index = set()

def populate_sentiment_indexes():
    ''' Populate positive/negative indexes '''
    for ID in review_metadata:
        rating = review_metadata[ID]['customer_review_rating']
        if int(rating) > 3:
            positive_index.add(ID)
        else:
            negative_index.add(ID)

def determine_positivity(opinion):
    ''' Categorize the opinion as positive or negative using the opinion lexicon '''
    if opinion in positive_words:
        return True
    elif opinion in negative_words:
        return False
    else:
        return None

def get_indices(term):
    ''' Retrieve the set of indices for a term from the postings list. '''
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
    
def M2_classifier(result, review_metadata, positivity, tfidf, model):
    """
    Filters the result list using the sentiment classifier.
    Args:
        result (list): List of review IDs from the baseline Boolean search.
        review_metadata (dict): Metadata dictionary with review text.
        positivity (bool): Polarity of the query's opinion (True = positive, False = negative).
        tfidf: Pre-trained TF-IDF vectorizer.
        model: Pre-trained sentiment classification model.
    Returns:
        list: Refined list of review IDs matching the query's sentiment.
    """
    # Preprocess the review texts for the given IDs
    review_texts = [review_metadata[ID]["text"] for ID in result]

    # Transform the texts into the TF-IDF feature space
    vectorized_texts = tfidf.transform(review_texts)

    # Predict sentiment for each review
    sentiments = model.predict(vectorized_texts)

    # Filter results based on query sentiment
    filtered_results = [
        ID for ID, sentiment in zip(result, sentiments)
        if (positivity and sentiment == 1) or (not positivity and sentiment == 0)
    ]
    return filtered_results

def M3_ratio_filter(positivity, result):
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
    ''' M3 helper function that calculates the positive word to negative word ratio in a single review'''
    # Tokenize and Count
    words = re.findall(r'\b\w+\b', review_text.lower())
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    # Calculate ratio
    total_count = positive_count + negative_count
    if total_count == 0:
        return None  # No sentiment words found
    return positive_count / total_count

def combine_methods(result1, result2, result3):
    return list(set(result1) & set(result2) & set(result3))

def diagnostic(result, M1_result, M2_result, M3_result, combined_result, print_raw:bool=False):
    if print_raw:
        print(f"{result}\n{M1_result}\n{M2_result}\n{M3_result}\n{combined_result}\n")
    print(f"Length of Baseline: {len(result)}")
    print(f"Length of M1_result: {len(M1_result)}")
    print(f"Length of M2_result: {len(M2_result)}")
    print(f"Length of M3_result: {len(M3_result)}")
    print(f"Length of combined result: {len(combined_result)}")

def main():

    parser = argparse.ArgumentParser(description="Perform the boolean search.")

    parser.add_argument("-a1", "--aspect1", type=str, required=True, default=None, help="First word of the aspect")
    parser.add_argument("-a2", "--aspect2", type=str, required=True, default=None, help="Second word of the aspect")
    parser.add_argument("-o", "--opinion", type=str, required=True, default=None, help="Only word of the opinion")
    parser.add_argument("-m", "--method", type=str, required=True, default=None, help="The method of boolean operation. Methods\
                        can be method1, method2 or method3")

    # Parse the arguments
    args = parser.parse_args()

    # Populate positive/negative indexes
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

    ''' M2: 4.3: Modeling Linguistic Relevance using Classification '''
    M2_result = M2_classifier(result, review_metadata, positivity, tfidf, model)

    ''' M3: 4.4(b): Grammar and Structure Based Relevance using Review Title and Sentence Structure '''
    M3_result = M3_ratio_filter(positivity, result)

    ''' M1 + M3: AND operation: M1_result AND M2_result AND M3_result '''
    combined_result = combine_methods(M1_result, M2_result, M3_result)

    ''' 
    Choose Method for Final Output:
    Baseline: 'result'
    Rating Search: 'M1_result'
    Classifier: 'M2_result'
    Ratio Filter: 'M3_result'
    Combined Methods: 'combined_result' 
    '''
    final_result = combined_result

    # Skip file generation is diagnostic is None
    skip_diagnostic = False
    if skip_diagnostic:
        revs = pd.DataFrame()
        revs["review_index"] = final_result
        output_filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_{args.method}.pkl"
        revs.to_pickle(output_filename)
        print(f"Results saved to {output_filename}")
    elif skip_diagnostic is not None:
        revs = pd.DataFrame()
        revs["review_index"] = final_result
        output_filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_{args.method}.pkl"
        revs.to_pickle(output_filename)
        print(f"Results saved to {output_filename}")
        diagnostic(result, M1_result, M2_result, M3_result, combined_result)
    else:
        diagnostic(result, M1_result, M2_result, M3_result, combined_result, print_raw=False)

if __name__ == "__main__":
    main()

'''
python boolean_search_help.py --aspect1 audio --aspect2 quality --opinion poor --method method1
python boolean_search_help.py --aspect1 audio --aspect2 quality --opinion poor --method method2
python boolean_search_help.py --aspect1 audio --aspect2 quality --opinion poor --method method3

python boolean_search_help.py --aspect1 wifi --aspect2 signal --opinion strong --method method1
python boolean_search_help.py --aspect1 wifi --aspect2 signal --opinion strong --method method2
python boolean_search_help.py --aspect1 wifi --aspect2 signal --opinion strong --method method3

python boolean_search_help.py --aspect1 gps --aspect2 map --opinion useful --method method1
python boolean_search_help.py --aspect1 gps --aspect2 map --opinion useful --method method2
python boolean_search_help.py --aspect1 gps --aspect2 map --opinion useful --method method3

python boolean_search_help.py --aspect1 image --aspect2 quality --opinion sharp --method method1
python boolean_search_help.py --aspect1 image --aspect2 quality --opinion sharp --method method2
python boolean_search_help.py --aspect1 image --aspect2 quality --opinion sharp --method method3
'''