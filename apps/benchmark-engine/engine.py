import pandas as pd
import numpy as np

class MetadataBenchmarkEngine:
    def __init__(self):
        # Weighted importance of metadata fields
        self.weights = {
            "description": 0.3,
            "owner": 0.2,
            "tags": 0.2,
            "lineage": 0.2,
            "quality_metrics": 0.1
        }

    def calculate_coverage_score(self, metadata_df: pd.DataFrame):
        """
        Calculates a completeness score for a set of data assets.
        """
        scores = []
        for col, weight in self.weights.items():
            if col in metadata_df.columns:
                completeness = metadata_df[col].notnull().mean()
                scores.append(completeness * weight)
            else:
                scores.append(0)
        
        total_score = sum(scores) * 100
        return round(total_score, 2)

    def benchmark_search_relevance(self, expected_results: list, actual_results: list):
        """
        Calculates precision/recall for search discovery testing.
        """
        if not actual_results:
            return 0.0
            
        matches = set(expected_results).intersection(set(actual_results))
        precision = len(matches) / len(actual_results)
        return round(precision * 100, 2)

if __name__ == "__main__":
    engine = MetadataBenchmarkEngine()
    
    # Mock data
    data = {
        "asset_id": [1, 2, 3, 4, 5],
        "description": ["Customer Table", "Sales Data", None, "Orders", "Products"],
        "owner": ["Data Team", "Finance", "Data Team", None, "Logistics"],
        "tags": ["PII", "Fact", "Raw", "PII", "Dim"]
    }
    df = pd.DataFrame(data)
    
    score = engine.calculate_coverage_score(df)
    print(f"Metadata Coverage Score: {score}%")
