import pickle
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import time

def prepare_labeled_data(review_metadata):
    """
    Prepares labeled data from review metadata.
    Args:
        review_metadata (dict): Dictionary containing review text and ratings.
    Returns:
        list: List of tuples (review_text, label), where label is 1 for positive and 0 for negative.
    """
    labeled_data = []
    for ID in review_metadata:
        rating = review_metadata[ID].get('customer_review_rating', None)
        text = review_metadata[ID].get('text', "")
        if rating is not None:
            if int(rating) > 3:
                labeled_data.append((text, 1))  # Positive
            else:
                labeled_data.append((text, 0))  # Negative
    return labeled_data

def preprocess_text(text):
    """
    Preprocesses a single review text: tokenization, lowercasing, and stopword removal.
    Args:
        text (str): Raw review text.
    Returns:
        str: Preprocessed text.
    """
    tokens = re.findall(r'\b\w+\b', text.lower())
    tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]
    return " ".join(tokens)

def preprocess_metadata(review_metadata):
    """
    Adds preprocessed text to review metadata.
    Args:
        review_metadata (dict): Dictionary containing review text and ratings.
    Returns:
        dict: Updated review_metadata with preprocessed text.
    """
    for ID, data in review_metadata.items():
        data["preprocessed_text"] = preprocess_text(data["text"])
    return review_metadata

def vectorize_text(labeled_data):
    """
    Vectorizes the text using TF-IDF.
    Args:
        labeled_data (list): List of tuples (review_text, label).
    Returns:
        tuple: Features, labels, and the TF-IDF vectorizer.
    """
    texts, labels = zip(*labeled_data)
    tfidf = TfidfVectorizer(max_features=5000)
    features = tfidf.fit_transform(texts)
    return features, labels, tfidf

def train_classifier(features, labels):
    """
    Trains a Naive Bayes classifier.
    Args:
        features (sparse matrix): TF-IDF features.
        labels (list): Labels corresponding to features.
    Returns:
        MultinomialNB: Trained model.
    """
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    return model

def filter_results_with_classifier(model, tfidf, result_ids, review_metadata, positivity):
    """
    Filters Boolean search results using the sentiment classifier.
    Args:
        model (MultinomialNB): Trained sentiment classifier.
        tfidf (TfidfVectorizer): Trained TF-IDF vectorizer.
        result_ids (list): List of review IDs from Boolean search.
        review_metadata (dict): Metadata containing reviews.
        positivity (bool): Desired sentiment orientation (True for positive, False for negative).
    Returns:
        list: Filtered result IDs.
    """
    review_texts = [review_metadata[ID]["preprocessed_text"] for ID in result_ids if "preprocessed_text" in review_metadata[ID]]
    vectorized_texts = tfidf.transform(review_texts)
    sentiments = model.predict(vectorized_texts)

    return [
        ID for ID, sentiment in zip(result_ids, sentiments)
        if (positivity and sentiment == 1) or (not positivity and sentiment == 0)
    ]

def save_artifacts(model, tfidf, model_filename="sentiment_classifier.pkl", tfidf_filename="tfidf_vectorizer.pkl"):
    """
    Saves the trained model and TF-IDF vectorizer to disk.
    Args:
        model: The trained sentiment classification model.
        tfidf: The trained TF-IDF vectorizer.
        model_filename: The filename to save the model.
        tfidf_filename: The filename to save the vectorizer.
    """
    with open(model_filename, "wb") as model_file:
        pickle.dump(model, model_file)
        print(f"Model saved as '{model_filename}'")

    with open(tfidf_filename, "wb") as tfidf_file:
        pickle.dump(tfidf, tfidf_file)
        print(f"TF-IDF vectorizer saved as '{tfidf_filename}'")

def load_artifacts():
    """
    Loads the trained model and vectorizer from disk.
    Returns:
        tuple: Loaded model and vectorizer.
    """
    with open("sentiment_classifier.pkl", "rb") as f:
        model = pickle.load(f)
    with open("tfidf_vectorizer.pkl", "rb") as f:
        tfidf = pickle.load(f)
    return model, tfidf

def main():
    start_time = time.time()

    # Load review metadata
    with open("review_metadata.pkl", "rb") as f:
        review_metadata = pickle.load(f)

    # Step 1: Prepare labeled data
    labeled_data = prepare_labeled_data(review_metadata)

    # Step 2: Preprocess metadata for efficiency
    review_metadata = preprocess_metadata(review_metadata)

    # Step 3: Vectorize text
    features, labels, tfidf = vectorize_text(labeled_data)

    # Step 4: Train classifier
    model = train_classifier(features, labels)

    # Step 5: Save artifacts
    save_artifacts(model, tfidf)

    print(f"Training completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()