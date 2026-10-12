from performancetask.sheet_handler import extract_table_entities
from performancetask.apriori import get_product_set, filter_validate_support, get_k_1, get_k_2
import argparse

FILE_PATH = "Cleaned-Data-Set.xlsx"
SHEET_NAME = "Supermarket_Sample_100"

CONFIDENCE = 0.5
SUPPORT = 0.04

    
arg_parser = argparse.ArgumentParser(description="West Coast Apriori Result.")
arg_parser.add_argument(
    "--print-data",
    action="store_true",
    help="Print the extracted data"
)
args = arg_parser.parse_args()


def get_records() -> list:
    return extract_table_entities(
        file_path=FILE_PATH,
        sheet_name=SHEET_NAME,
        header_row=54,   
        columns="A:F"  
    )


def main() -> None:

    records = get_records()

    if args.print_data:
        print("\nExtracted Records:")
        for entity in records:
            print(entity)

    product_set = get_product_set(records)
    if args.print_data:
        print("\nProducts Set: ", product_set)
        
    k_1_itemsets = get_k_1(records)
    if args.print_data:
        print("\nK-1 Itemsets:")
        for itemset in k_1_itemsets:
            print(itemset)

    accepted_k_1_itemsets = filter_validate_support(k_1_itemsets, SUPPORT)
    if args.print_data:
        print("\nK-1 Itemsets (Accepted Support):")
        for itemset in accepted_k_1_itemsets:
            print(itemset)

    k_2_itemsets = get_k_2(accepted_k_1_itemsets, records)
    if args.print_data:
        print("\nK-2 Itemsets:")
        for itemset in k_2_itemsets:
            print(itemset)
    
    
