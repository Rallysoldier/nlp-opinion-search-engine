import pickle
import pandas as pd
import ast
import re

''' Customer Class and Methods for M4: Unique Method '''
class Customer:
    def __init__(
            self, group, cust_id, positive_words=None, negative_words=None, 
            metadata:list[str]=None, formatted_metadata:list[tuple]=None, 
            tuple_sizes:int=None, reviews:list[dict]=None, num_reviews:int=0, 
            star_sum:int=0, helpful_count:int=0, out_of_helpful_count:int=0, 
            avg_stars:float=None, avg_helpfulness:float=None, avg_positivity:float=None
            ):
        self.group = group
        self.cust_id = cust_id
        self.positive_words = positive_words if positive_words is not None else None
        self.negative_words = negative_words if negative_words is not None else None
        self.metadata = self.get_metadata()
        self.formatted_metadata = self.format_metadata()
        self.tuple_sizes = self.get_tuple_sizes()
        self.reviews = []
        self.helpful_count = 0
        self.out_of_helpful_count = 0
        self.star_sum = 0
        self.num_reviews = 0
        self.extract_metadata()
        self.avg_stars = self.calc_avg_stars()
        self.avg_helpfulness = self.calc_avg_helpfulness()
        if positive_words and negative_words:
            self.avg_positivity = self.calc_avg_positivity()
        else:
            self.avg_positivity = None

    def get_metadata(self):
        metadata:list[str] = []
        for _, row in self.group.iterrows():
            metadata.append(row["review_with_metadata"])
        return metadata

    def format_metadata(self):
        formatted_metadata:list[tuple] = []
        for field in self.metadata:
            # Convert the serialized tuple string back to a tuple
            if isinstance(field, str):
                try:
                    # Account for errors in metadata format
                    if field.__contains__(";\n"):
                        field1 = field.split(";\n")[0]
                    else:
                        field1 = field
                    if field1.endswith(","):
                        field2 = field1[:-1]
                    else:
                        field2 = field1
                    prepped_field = field2.replace("NULL", "None")
                    # Convert str field to tuple
                    field_tuple = ast.literal_eval(prepped_field)
                    if isinstance(field_tuple, tuple) and len(field_tuple) > 1:
                        formatted_metadata.append(field_tuple)
                    else:
                        formatted_metadata.append(field)
                except Exception as e:
                    print(f"Error parsing field: {field}")
                    print(f"Error message: {e}")
            else:
                print(f"Unexpected field type: {type(field)}")
        return formatted_metadata

    def get_tuple_sizes(self):
        tuple_sizes:list[int] = []
        for tupl in self.formatted_metadata:
            tuple_sizes.append(len(tupl))
        return tuple_sizes

    def extract_metadata(self):
        # Metadata field indices for each element
        index = {
            0: "review_id",
            1: "product_id",
            2: "customer_id",
            3: "helpful_count",
            4: "out_of_helpful_count",
            5: "customer_review_rating",
            6: "review_title",
            7: "review_written_date",
            8: "customer_name",
            9: "review_from_title",
            10: "review_text" 
        }
        # Populate class member variables from tuple
        for field in self.formatted_metadata:
            self.reviews.append({
                index[0]: field[0], 
                index[2]: field[2],
                index[10]: field[10]
            })
            self.helpful_count += int(field[3])
            self.out_of_helpful_count += int(field[4])
            self.star_sum += int(field[5])
            self.num_reviews += 1

    def calc_avg_stars(self):
        return self.star_sum / self.num_reviews

    def calc_avg_helpfulness(self):
        if self.out_of_helpful_count == 0:
            return 0
        else:
            return self.helpful_count / self.out_of_helpful_count 

    def calc_avg_positivity(self):
        positive_sum = 0
        negative_sum = 0
        for review in self.reviews:
            review_text = review["review_text"]
            # Tokenize and Count
            words = re.findall(r'\b\w+\b', review_text.lower())
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            positive_sum += positive_count
            negative_sum += negative_count
        total_sum = positive_sum + negative_sum
        if total_sum > 0:
            return positive_sum / total_sum
        else:
            return None

    def diagnostic(self):
        attributes = [
            attr for attr in dir(self) if not attr.startswith('__') 
            and not callable(getattr(self, attr))
            ]
        for attr_name in attributes:
            attr_value = getattr(self, attr_name)
            if attr_name != "metadata" and attr_name != "formatted_metadata":
                print(f"{attr_name}: {attr_value}: {type(attr_value)}")
            else:
                print(f"{attr_name}: length={len(attr_value)}: {type(attr_value)}")

def get_groups(corpus_filename) -> pd.DataFrame:
    ''' Split the corpus into groups based on 'customer_id' '''
    with open(corpus_filename, "rb") as f:
        reviews_segment_df = pickle.load(f)
    return reviews_segment_df.groupby("customer_id")

def get_customers(
        grouped_reviews:pd.DataFrame, 
        positive_words_filename, 
        negative_words_filename
    ) -> list[Customer]:
    ''' Initialize instances of class Customer to create customer profiles'''
    # Load positive words
    with open(positive_words_filename, "r", encoding="utf-8") as f:
        positive_words = {line.strip() for line in f if line.strip()}
    # Load negative words
    with open(negative_words_filename, "r", encoding="utf-8") as f:
        negative_words = {line.strip() for line in f if line.strip()}
    # Generate Profiles
    customers:list[Customer] = []
    for cust_id, group in grouped_reviews:
        customers.append(Customer(group, cust_id, positive_words, negative_words))
    return customers

def customer_generation(
        corpus_filename = "reviews_segment.pkl",
        positive_words_filename = "positive-words.txt", 
        negative_words_filename = "negative-words.txt"
    ) -> list[Customer]:
    ''' Master Function to generate profiles '''
    grouped_reviews = get_groups(corpus_filename)
    return get_customers(grouped_reviews, positive_words_filename, negative_words_filename)

def save_customers_to_file(customers, filename="customers.pkl"):
    ''' Create customers.pkl for export '''
    with open(filename, "wb") as f:
        pickle.dump(customers, f)
    print(f"Customers saved to {filename}")

def run_customer_diagnostic(customers:list[Customer], reviews_segment_df):
    total_customers = len(customers)
    user_input = input("How many customers do you wish to review? ")
    try:
        user_input = int(user_input)
        if user_input > total_customers:
            warning_input = input("Too Many! Defaulting to max... You asked for this. Continue? y/n ")
            if warning_input == 'y':
                user_input = total_customers - 1
            else:
                user_input = -1
                print("Good Choice")
        for i, customer in enumerate(customers):
            if user_input >= i and user_input < total_customers:
                customers[i].diagnostic()
    except Exception as e:
        print(f"Error message: {e}")
    print(f"Number of Unique Customers: {len(customers)}")
    print(f"Number of Reviews: {len(reviews_segment_df)}")
    
def main():
    # Configure filename override
    corpus_filename = "reviews_segment.pkl"
    positive_words_filename = "positive-words.txt", 
    negative_words_filename = "negative-words.txt"

    # Choose regeneration or diagnostic
    diagnostic = False
    if not diagnostic:
        # Generate profiles
        customers = customer_generation(
            corpus_filename,
            positive_words_filename,
            negative_words_filename
        )
        # Save to pickle
        save_customers_to_file(customers)
    else:
        customers = customer_generation(
            corpus_filename,
            positive_words_filename,
            negative_words_filename
        )
        with open(corpus_filename, "rb") as f:
            reviews_segment_df = pickle.load(f)
        run_customer_diagnostic(customers, reviews_segment_df)
  
if __name__ == "__main__":
    main()
