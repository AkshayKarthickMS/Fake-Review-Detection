import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load your CSV file
df = pd.read_csv('results.csv')  # Replace with your actual CSV file path

# Fill NaN values in the 'message' column with an empty string
df['message'] = df['message'].fillna('')

# Convert the text data to TF-IDF vectors
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(df['message'])

# Apply k-means clustering
k = 2  # Number of clusters (you can adjust this)
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(vectors)

# Analyze the clusters
cluster_analysis = df.groupby('cluster').agg({
    'user': 'unique',
    'message': 'count',
    'star_rating': 'mean'
}).rename(columns={'message': 'review_count', 'star_rating': 'average_rating'}).sort_values('review_count', ascending=False)

# Print the cluster analysis
print(cluster_analysis)

# Manually inspect the clusters and identify those that might contain fake reviews
# Update the 'label' column accordingly (for example, label clusters with low average rating as 'fake')
df['label'] = 'non-fake'  # Default label
df.loc[df.groupby('cluster')['star_rating'].transform('mean') < 3, 'label'] = 'fake'  # Adjust the threshold as needed

# Save the results to a new CSV file
df[['user', 'message', 'label']].to_csv('results_with_labels_and_users.csv', index=False)
