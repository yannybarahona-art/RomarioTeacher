#from src.api_classes.api_client import InventoryAPIClient
from api_client import InventoryAPIClient
from report_generator import InventoryReportGenerator


if __name__ == "__main__":
    # Initialize the InventoryAPIClient
    api_client = InventoryAPIClient()

    # Fetch all products from the API
    all_products = api_client.fetch_all_products()

    # Initialize the InventoryReportGenerator with the fetched products
    report_generator = InventoryReportGenerator(all_products)

    # Generate and print the report
    #report = report_generator.generate_report()
   # print(report)