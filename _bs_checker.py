import pandas as pd
import argparse

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
        filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_method1.pkl"
    elif args.method.lower() == "method2":
        filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_method2.pkl"
    elif args.method.lower() == "method3":
        filename = f"{args.aspect1}_{args.aspect2}_{args.opinion}_method3.pkl"
    else:
        print("\n FILE NOT FOUND \n")
        return
    
    # Transform pickle into Pandas df
    result_df = pd.read_pickle(filename)

    # Display summary statistics
    print(f"\nSummary for file '{filename}':")
    print(f"Number of Indices: {len(result_df)}")

if __name__ == "__main__":
    main()
