import pandas as pd
import matplotlib.pyplot as plt
import os
import json

def main():
    # Load data
    df = pd.read_csv('data/processed/district_clusters.csv')
    
    # Map cluster IDs to descriptive names
    cluster_names = {
        0: 'High Intervention Priority',
        1: 'High-Cost & Specific-Risk',
        2: 'Healthcare Leaders'
    }
    
    # Calculate counts per state
    state_counts = pd.crosstab(df['State/UT'], df['Cluster'])
    
    # Rename columns to the descriptive names
    state_counts = state_counts.rename(columns=cluster_names)
    
    # Ensure all cluster columns exist even if some are missing
    for name in cluster_names.values():
        if name not in state_counts.columns:
            state_counts[name] = 0
            
    # Calculate Total Districts
    state_counts['Total_Districts'] = state_counts.sum(axis=1)
    
    # Calculate Percentages
    for name in cluster_names.values():
        state_counts[f'{name} (%)'] = (state_counts[name] / state_counts['Total_Districts'] * 100).round(2)
        
    # Reorder columns
    cols = ['Total_Districts', 
            'High Intervention Priority', 'High Intervention Priority (%)',
            'High-Cost & Specific-Risk', 'High-Cost & Specific-Risk (%)',
            'Healthcare Leaders', 'Healthcare Leaders (%)']
    state_counts = state_counts[cols]
    
    # Save the full state cluster distribution table
    os.makedirs('reports', exist_ok=True)
    state_counts.to_csv('reports/state_cluster_distribution.csv')
    
    # Identify top states for each cluster (by absolute count)
    # We filter out states with very few total districts (e.g., < 5) if we were doing pure percentage,
    # but by absolute count, the largest states will float to top. Let's provide top by count.
    
    top_intervention = state_counts.sort_values(by='High Intervention Priority', ascending=False).head(10)
    top_cost_risk = state_counts.sort_values(by='High-Cost & Specific-Risk', ascending=False).head(10)
    top_leaders = state_counts.sort_values(by='Healthcare Leaders', ascending=False).head(10)
    
    # Also look at high concentration (percentage) for states with at least 10 districts
    significant_states = state_counts[state_counts['Total_Districts'] >= 10]
    top_pct_intervention = significant_states.sort_values(by='High Intervention Priority (%)', ascending=False).head(5)
    top_pct_cost_risk = significant_states.sort_values(by='High-Cost & Specific-Risk (%)', ascending=False).head(5)
    top_pct_leaders = significant_states.sort_values(by='Healthcare Leaders (%)', ascending=False).head(5)
    
    # Save summary to JSON
    summary = {
        'top_count_intervention': top_intervention[['High Intervention Priority', 'Total_Districts']].to_dict(orient='index'),
        'top_count_cost_risk': top_cost_risk[['High-Cost & Specific-Risk', 'Total_Districts']].to_dict(orient='index'),
        'top_count_leaders': top_leaders[['Healthcare Leaders', 'Total_Districts']].to_dict(orient='index'),
        'top_pct_intervention': top_pct_intervention[['High Intervention Priority (%)']].to_dict(orient='index'),
        'top_pct_cost_risk': top_pct_cost_risk[['High-Cost & Specific-Risk (%)']].to_dict(orient='index'),
        'top_pct_leaders': top_pct_leaders[['Healthcare Leaders (%)']].to_dict(orient='index')
    }
    
    with open('reports/state_analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
        
    # Generate Visualizations
    os.makedirs('reports/figures', exist_ok=True)
    
    # Plot 1: Top 10 States by High Intervention Priority (Count)
    plt.figure(figsize=(10, 6))
    top_intervention['High Intervention Priority'].sort_values().plot(kind='barh', color='crimson')
    plt.title('Top 10 States by Count of High Intervention Priority Districts')
    plt.xlabel('Number of Districts')
    plt.tight_layout()
    plt.savefig('reports/figures/top_intervention_states.png')
    plt.close()
    
    # Plot 2: Top 10 States by Healthcare Leaders (Count)
    plt.figure(figsize=(10, 6))
    top_leaders['Healthcare Leaders'].sort_values().plot(kind='barh', color='forestgreen')
    plt.title('Top 10 States by Count of Healthcare Leaders Districts')
    plt.xlabel('Number of Districts')
    plt.tight_layout()
    plt.savefig('reports/figures/top_leader_states.png')
    plt.close()
    
    # Plot 3: 100% Stacked Bar for Top 15 largest states
    top_15_largest = state_counts.sort_values(by='Total_Districts', ascending=False).head(15)
    top_15_pcts = top_15_largest[['High Intervention Priority (%)', 'High-Cost & Specific-Risk (%)', 'Healthcare Leaders (%)']]
    
    ax = top_15_pcts.plot(kind='bar', stacked=True, figsize=(12, 6), color=['crimson', 'orange', 'forestgreen'])
    plt.title('Cluster Distribution (%) Across 15 Largest States')
    plt.ylabel('Percentage (%)')
    plt.xlabel('State/UT')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('reports/figures/stacked_state_distribution.png')
    plt.close()

    print("State analysis complete.")

if __name__ == '__main__':
    main()
