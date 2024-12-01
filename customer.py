import os
import pickle
import pandas as pd

''' Customer Class and Methods for M4: Unique Method '''

def get_customer_ids(reviews_segment_df) -> set:
    ''' Returns a set of all customer ids '''
    customer_ids = set()
    for cust_id in reviews_segment_df.customer_id:
        customer_ids.add(cust_id)
    return customer_ids

class Customer:
    def __init__(
            self, group, cust_id, metadata_index:dict=None, metadata:list[str]=None, 
            reviews:list[str]=None, num_reviews:int=None, 
            star_sum:int=None, helpful_count:int=None, out_of_helpful_count:int=None, 
            avg_stars:float=None, avg_helpfulness:float=None, avg_positivity:float=None
            ):
        self.group = group
        self.cust_id = cust_id
        self.metadata_index = {
            0: "review_id",
            1: "prodcut_id",
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
        self.metadata = self.get_metadata()
        '''
        self.reviews = self.get_reviews()
        self.num_reviews = self.get_num_reviews()
        self.star_sum = self.get_star_sum()
        self.avg_stars = self.calc_avg_stars()
        self.avg_helpfulness = self.calc_avg_helpfulness()
        self.avg_positivity = self.calc_avg_positivity()
        '''

    def get_metadata(self):
        metadata:list[str] = []
        for _, row in self.group.iterrows():
            metadata.append(row["review_with_metadata"])
        return metadata

    def get_data(self):
        for _, row in self.group.iterrows():
            pass
            #self.reviews.append(ro)

    def get_num_reviews(self):
        return len(self.reviews)

    def get_star_sum(self):
        star_sum = 0
        for _, row in self.group.iterrows():
            star_sum += int(row["customer_review_rating"])
        return star_sum 

    def get_helpful_count(self):
        pass

    def calc_avg_stars(self):
        return self.star_sum / self.num_reviews

    def calc_avg_helpfulness(self):
        return self.helpful_count / self.out

    def calc_avg_positivity(self):
        pass

    def diagnostic(self):
        attributes = [
            attr for attr in dir(self) if not attr.startswith('__') 
            and not callable(getattr(self, attr))
            ]
        for attr_name in attributes:
            attr_value = getattr(self, attr_name)
            print(f"{attr_name}: {attr_value}")

def main():
    with open("reviews_segment.pkl", "rb") as f:
        # <class 'pandas.core.frame.DataFrame'>
        reviews_segment_df = pickle.load(f)

    # Pre-group rows by customer_id
    grouped_reviews = reviews_segment_df.groupby("customer_id")

    customers:list[Customer] = []
    for cust_id, group in grouped_reviews:
        customers.append(Customer(group, cust_id))

    #print(reviews_segment_df.review_id)
    #print(f"Num customers: {len(customer_ids)}")

    customers[0].diagnostic()

if __name__ == "__main__":
    main()