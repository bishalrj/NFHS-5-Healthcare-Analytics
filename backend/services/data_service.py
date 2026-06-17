import pandas as pd
from typing import Dict, Any, List
from fastapi import HTTPException

# Constants matching the project context
CLUSTER_NAMES = {
    0: "High Intervention Priority Districts",
    1: "High-Cost & Specific-Risk Districts",
    2: "Healthcare Leaders"
}

class DataService:
    def __init__(self):
        self.district_df = pd.DataFrame()
        self.state_dist_df = pd.DataFrame()
        self.cluster_comp_df = pd.DataFrame()
        self.loaded = False

    def load_data(self):
        """Loads all CSVs into memory once at startup."""
        try:
            self.district_df = pd.read_csv("data/processed/district_clusters.csv")
            # Strip whitespace from string columns to prevent lookup failures
            self.district_df['District Names'] = self.district_df['District Names'].str.strip()
            self.district_df['State/UT'] = self.district_df['State/UT'].str.strip()

            self.state_dist_df = pd.read_csv("reports/state_cluster_distribution.csv")
            # Actual columns: 'State/UT', 'Total_Districts', 'High Intervention Priority',
            # 'High Intervention Priority (%)', 'High-Cost & Specific-Risk',
            # 'High-Cost & Specific-Risk (%)', 'Healthcare Leaders', 'Healthcare Leaders (%)'
            self.state_dist_df['State/UT'] = self.state_dist_df['State/UT'].str.strip()

            # Actual columns: 'Unnamed: 0', 'Cluster_0_mean', 'Cluster_0_z_diff',
            # 'Cluster_1_mean', 'Cluster_1_z_diff', 'Cluster_2_mean', 'Cluster_2_z_diff'
            self.cluster_comp_df = pd.read_csv("reports/cluster_comparison_table.csv")
            # Rename for clarity
            self.cluster_comp_df.rename(columns={'Unnamed: 0': 'Indicator'}, inplace=True)
            # Drop trailing empty rows
            self.cluster_comp_df.dropna(subset=['Indicator'], inplace=True)

            self.loaded = True
            print(f"Data loaded: {len(self.district_df)} districts, {len(self.state_dist_df)} states, {len(self.cluster_comp_df)} indicators")
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            raise e

    def get_all_districts(self) -> List[Dict[str, Any]]:
        records = self.district_df[['District Names', 'State/UT', 'Cluster']].to_dict(orient="records")
        return records

    def get_district_by_name(self, district_name: str) -> Dict[str, Any]:
        match = self.district_df[self.district_df['District Names'].str.lower() == district_name.strip().lower()]
        if match.empty:
            raise HTTPException(status_code=404, detail=f"District '{district_name}' not found")

        record = match.iloc[0].to_dict()
        indicators = {k: round(float(v), 4) if isinstance(v, float) else v
                      for k, v in record.items()
                      if k not in ['District Names', 'State/UT', 'Cluster']}

        return {
            "District Names": record['District Names'],
            "State/UT": record['State/UT'],
            "Cluster": int(record['Cluster']),
            "indicators": indicators
        }

    def get_all_states(self) -> List[Dict[str, Any]]:
        states = []
        for _, r in self.state_dist_df.iterrows():
            states.append({
                "state_name": r["State/UT"],
                "total_districts": int(r["Total_Districts"]),
                "cluster_0_count": int(r["High Intervention Priority"]),
                "cluster_1_count": int(r["High-Cost & Specific-Risk"]),
                "cluster_2_count": int(r["Healthcare Leaders"]),
                "cluster_0_pct": round(float(r["High Intervention Priority (%)"]), 2),
                "cluster_1_pct": round(float(r["High-Cost & Specific-Risk (%)"]), 2),
                "cluster_2_pct": round(float(r["Healthcare Leaders (%)"]), 2)
            })
        return states

    def get_state_by_name(self, state_name: str) -> Dict[str, Any]:
        match = self.state_dist_df[self.state_dist_df['State/UT'].str.lower() == state_name.strip().lower()]
        if match.empty:
            raise HTTPException(status_code=404, detail=f"State '{state_name}' not found")
        r = match.iloc[0]
        return {
            "state_name": r["State/UT"],
            "total_districts": int(r["Total_Districts"]),
            "cluster_0_count": int(r["High Intervention Priority"]),
            "cluster_1_count": int(r["High-Cost & Specific-Risk"]),
            "cluster_2_count": int(r["Healthcare Leaders"]),
            "cluster_0_pct": round(float(r["High Intervention Priority (%)"]), 2),
            "cluster_1_pct": round(float(r["High-Cost & Specific-Risk (%)"]), 2),
            "cluster_2_pct": round(float(r["Healthcare Leaders (%)"]), 2)
        }

    def _build_comparison(self) -> List[Dict[str, Any]]:
        comparisons = []
        for _, row in self.cluster_comp_df.iterrows():
            comparisons.append({
                "indicator": row["Indicator"],
                "cluster_0_mean": round(float(row["Cluster_0_mean"]), 4),
                "cluster_1_mean": round(float(row["Cluster_1_mean"]), 4),
                "cluster_2_mean": round(float(row["Cluster_2_mean"]), 4),
                "cluster_0_zscore": round(float(row["Cluster_0_z_diff"]), 4),
                "cluster_1_zscore": round(float(row["Cluster_1_z_diff"]), 4),
                "cluster_2_zscore": round(float(row["Cluster_2_z_diff"]), 4)
            })
        return comparisons

    def get_all_clusters(self) -> List[Dict[str, Any]]:
        comparisons = self._build_comparison()
        clusters = []
        for c_id, c_name in CLUSTER_NAMES.items():
            count = len(self.district_df[self.district_df['Cluster'] == c_id])
            clusters.append({
                "cluster_id": c_id,
                "name": c_name,
                "total_districts": count,
                "comparison": comparisons
            })
        return clusters

    def get_cluster_by_id(self, cluster_id: int) -> Dict[str, Any]:
        if cluster_id not in CLUSTER_NAMES:
            raise HTTPException(status_code=404, detail=f"Cluster ID {cluster_id} not found. Valid IDs are 0, 1, 2.")
        count = len(self.district_df[self.district_df['Cluster'] == cluster_id])
        comparisons = self._build_comparison()
        return {
            "cluster_id": cluster_id,
            "name": CLUSTER_NAMES[cluster_id],
            "total_districts": count,
            "comparison": comparisons
        }

data_service = DataService()
