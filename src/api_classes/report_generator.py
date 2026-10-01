from pathlib import Path
import pandas as pd


class InventoryReportGenerator:
    """Transforms raw product API data into structured business reports."""

    def __init__(self, raw_data: list[dict]):
        # TODO: Load raw_data into a pandas DataFrame attribute
        self.df = pd.DataFrame(raw_data)

        #pass

    def process_inventory(self, low_stock_threshold: int = 10) -> pd.DataFrame:
        """Calculate discounted prices and identify low-stock items."""
        # TODO: Calculate 'discounted_price' = price * (1 - discountPercentage / 100)
        self.df['discounted_price'] = self.df['price'] * (1 - self.df['discountPercentage'] / 100)
        # TODO: Add boolean column 'low_stock_warning' if stock < low_stock_threshold
        self.df['low_stock_warning'] = self.df['stock'] < low_stock_threshold
        # TODO: Select and reorder relevant columns
        self.df = self.df[['id', 'title', 'description', 'price', 'discountPercentage', 'discounted_price', 'stock', 'low_stock_warning']]


        #pass

    def export_csv(self, destination: str | Path) -> None:
        """Export the processed DataFrame to CSV format."""
        # TODO: Save DataFrame to CSV using pandas
        self.df.to_csv(destination, index=False)


        #pass

    def export_summary_metrics(self, destination: str | Path) -> None:
        """Export high-level metrics (total inventory value, item count) as JSON."""
        # TODO: Compute summary statistics and export to JSON
        summary_metrics = {
            "total_inventory_value": self.df['discounted_price'].sum(),
            "total_item_count": len(self.df)
        }
        with open(destination, 'w') as f:
            import json
            json.dump(summary_metrics, f, indent=4)

        #pass
