import pickle

def read_postings_list_sample(filename, sample_size=10):
    # Load the postings list from the pickle file
    with open(filename, "rb") as f:
        postings_list = pickle.load(f)
    
    # Display a sample of key-value pairs
    print(f"Displaying a sample of {sample_size} key-value pairs from the postings list:")
    for i, (word, indices) in enumerate(postings_list.items()):
        if i >= sample_size:
            break
        print(f"{word}: {indices}")

def read_postings_list_keys(filename, bool: sorted):
    with open(filename, "rb") as f:
        postings_list = pickle.load(f)
    
    if sorted == True:
        # Extract and sort the keys alphabetically
        words = sorted(postings_list.keys())
        output_file = "sorted_postings_list_keys"
    else:
        words = postings_list.keys()
        output_file = "postings_list_keys"
        
    # Write the words to a file
    with open(output_file, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")

    print(f"postings_list.pkl keys have been written to '{output_file}'")

def search_postings_list_key(filename, search_term):
    # Load the postings list from the pickle file
    with open(filename, "rb") as f:
        postings_list = pickle.load(f)
    
    # Search for the specified key and display the result
    if search_term in postings_list:
        print(f"{search_term}: {postings_list[search_term]}")
        print(f"Number of Reviews containing {search_term}: {len(postings_list[search_term])}")
    else:
        print(f"'{search_term}' not found in the postings list.")

def compare_set_vs_list(filename, search_term):
    # Load the postings list from the pickle file
    with open(filename, "rb") as f:
        postings_list = pickle.load(f)
    
    # Search for the specified key and display the result
    if search_term in postings_list:
        print(f"{search_term} indices list length: {len(postings_list[search_term])}")
        print(f"{search_term} indices set length: {len(set((postings_list[search_term])))}")
    else:
        print(f"'{search_term}' not found in the postings list.")

def result_vs_homogenous_search(result_filename, posting_filename, search_term):
    '''For ensuring consistency between postings list # of indices and binary search results
    Ensure that prior commands to boolean_search_help.py are homogenous. e.g.
    python boolean_search_help.py --aspect1 gps --aspect2 gps --opinion gps --method method'''
    with open(result_filename, "rb") as f:
        result_indices = pickle.load(f)
    with open(posting_filename, "rb") as f:
        postings_list = pickle.load(f)
    
    if search_term in postings_list:
        print(f"Num indices in {result_filename}: {len(result_indices)}")
        print(f"Num indices in {posting_filename}: {len(postings_list[search_term])}")

def main():
    # Uncomment one of the functions below to use it:

    # Display a sample of the postings list
    #read_postings_list_sample("postings_list.pkl")

    # Save keys to a text file
    sorted = False
    #read_postings_list_keys("postings_list.pkl", sorted)

    search_term = "gps"
    # Search for a specific key
    #search_postings_list_key("postings_list.pkl", search_term) 

    # Ensure validity of postings list via length of term:set vs term:list
    #compare_set_vs_list("postings_list.pkl", search_term)

    method = "method1"
    result_filename = f"{search_term}_{search_term}_{search_term}_{method}.pkl"
    # Ensure consistency between postings list # of indices and binary search results
    result_vs_homogenous_search(result_filename, "postings_list.pkl", search_term)

if __name__ == "__main__":
    main()
