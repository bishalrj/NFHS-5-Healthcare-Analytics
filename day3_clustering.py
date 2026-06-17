import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
import os

def main():
    # Load model_ready_data.csv
    df = pd.read_csv('data/processed/model_ready_data.csv')

    # Separate identifier columns and numerical feature columns
    identifiers = ['District Names', 'State/UT']
    feature_cols = [c for c in df.columns if c not in identifiers]
    
    df_ids = df[identifiers]
    df_features = df[feature_cols]

    # Verify no missing values and all numeric
    assert df_features.isnull().sum().sum() == 0, "Missing values detected!"
    assert all(pd.api.types.is_numeric_dtype(df_features[c]) for c in df_features.columns), "Non-numeric columns detected!"

    # Standardize all numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_features)

    # Evaluate candidate cluster counts
    K_range = range(2, 11)
    inertias = []
    silhouette_scores = []

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_scores.append(score)

    # Generate Elbow plot
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, inertias, marker='o', linestyle='--')
    plt.title('Elbow Method for Optimal K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia')
    plt.grid(True)
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/elbow_plot.png')
    plt.close()

    # Generate Silhouette plot
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, silhouette_scores, marker='o', color='orange', linestyle='--')
    plt.title('Silhouette Score for Optimal K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.grid(True)
    plt.savefig('reports/figures/silhouette_plot.png')
    plt.close()

    # Select optimal K automatically based on max silhouette score
    # (Typically optimal K has a distinct elbow and good silhouette score)
    optimal_k_idx = np.argmax(silhouette_scores)
    optimal_k = K_range[optimal_k_idx]

    # Alternatively, you might want K=3, K=4 depending on domain, but here we pick max silhouette
    # Let's say optimal K is chosen
    # Train final model
    kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_final.fit_predict(X_scaled)

    # Assign cluster label
    df['Cluster'] = cluster_labels

    # Create district_clusters.csv
    df.to_csv('data/processed/district_clusters.csv', index=False)

    # Prepare info for report
    cluster_sizes = df['Cluster'].value_counts().sort_index().to_dict()
    cluster_sizes_str = {str(k): int(v) for k, v in cluster_sizes.items()}
    
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans_final.cluster_centers_), columns=feature_cols)
    
    # Let's pick a few top features for centroid variation to include in report
    report_info = {
        'optimal_k': int(optimal_k),
        'silhouette_scores': {str(k): float(s) for k, s in zip(K_range, silhouette_scores)},
        'inertias': {str(k): float(i) for k, i in zip(K_range, inertias)},
        'cluster_sizes': cluster_sizes_str,
        'centroids_summary': centroids.to_dict(orient='index')
    }

    with open('reports/clustering_results.json', 'w') as f:
        json.dump(report_info, f, indent=4)

    print(f"Clustering complete. Optimal K: {optimal_k}")
    
if __name__ == '__main__':
    main()
