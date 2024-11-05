import pandas as pd
import argparse
import pickle

# Load postings list
with open("postings_list.pkl", "rb") as f:
    postings_list = pickle.load(f)

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

def main():

    parser = argparse.ArgumentParser(description="Perform the boolean search.")
    
    parser.add_argument("-a1", "--aspect1", type=str, required=True, default=None, help="First word of the aspect")
    parser.add_argument("-a2", "--aspect2", type=str, required=True, default=None, help="Second word of the aspect")
    parser.add_argument("-o", "--opinion", type=str, required=True, default=None, help="Only word of the opinion")
    parser.add_argument("-m", "--method", type=str, required=True, default=None, help="The method of boolean operation. Methods\
                        can be method1, method2 or method3")

    # Parse the arguments
    args = parser.parse_args()

    if args.method.lower() == "method1":
        result = method1(args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method2":
        result = method2(args.aspect1, args.aspect2, args.opinion)
    elif args.method.lower() == "method3":
        result = method3(args.aspect1, args.aspect2, args.opinion)
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
