import pandas as pd
import argparse

def method1(review_df, aspect1, aspect2, opinion):
    """
    the first method will only perform the aspect1 OR aspect2 OR opinion
    """
    return review_df[
        review_df['review_text'].str.contains(aspect1, case=False) |
        review_df['review_text'].str.contains(aspect2, case=False) |
        review_df['review_text'].str.contains(opinion, case=False)
    ].index.tolist()

def method2(review_df, aspect1, aspect2, opinion):
    """
    the second method will only perform the aspect1 AND aspect2 AND opinion
    """
    return review_df[
        review_df['review_text'].str.contains(aspect1, case=False) &
        review_df['review_text'].str.contains(aspect2, case=False) &
        review_df['review_text'].str.contains(opinion, case=False)
    ].index.tolist()

def method3(review_df, aspect1, aspect2, opinion):
    """
    the third method will only perform the aspect1 OR aspect2 AND opinion
    """
    return review_df[
        (review_df['review_text'].str.contains(aspect1, case=False) |
         review_df['review_text'].str.contains(aspect2, case=False)) &
        review_df['review_text'].str.contains(opinion, case=False)
    ].index.tolist()

def main():

    parser = argparse.ArgumentParser(description="Perform the boolean search.")
    
    parser.add_argument("-a1", "--aspect1", type=str, required=True, default=None, help="First word of the aspect")
    parser.add_argument("-a2", "--aspect2", type=str, required=True, default=None, help="Second word of the aspect")
    parser.add_argument("-o", "--opinion", type=str, required=True, default=None, help="Only word of the opinion")
    parser.add_argument("-m", "--method", type=str, required=True, default=None, help="The method of boolean operation. Methods\
                        can be method1, method2 or method3")

    # Parse the arguments
    args = parser.parse_args()

    # Read pickle, transform into pandas dataframe
    review_df = pd.read_pickle("reviews_segment.pkl")

    if args.method.lower() == "method1":
        result = method1(review_df, args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method2":
        result = method2(review_df, args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method3":
        result = method3(review_df, args.aspect1, args.aspect2, args.opinion)
    else:
        print("\n!! The method is not supported !!\n")
        return

    revs = pd.DataFrame()
    revs["review_index"] = result
    output_filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_{args.method}.pkl"
    revs.to_pickle(output_filename)
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()

'''
TERMINAL:
REQUIRED:
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
 
OTHER: 
 How to handle two word queries:  
 python boolean_search_help.py --aspect1 mouse --aspect2 button --opinion "click problem" --method method1
'''