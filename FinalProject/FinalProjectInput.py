import csv
from datetime import datetime

# Author: Abhinay Dalwadi
# Student ID: 1835076
# FinalProjectInput.py

class Item:
    def __init__(self, item_id, manufacturer_name, item_type, price, service_date, damaged=None):
        self.item_id = item_id
        self.manufacturer_name = manufacturer_name
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged
    
    def __repr__(self):
        return f"Item({self.item_id}, {self.manufacturer_name}, {self.item_type}, {self.price}, {self.service_date}, {self.damaged})"

def read_manufacturer_data(file_path):
    """
    Loads item data from a CSV file and creates Item objects.
    This function stores items in a dictionary with item_id as the key.
    """
    items = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            item_id, manufacturer_name, item_type, damaged = row
            items[item_id] = Item(
                item_id=item_id,
                manufacturer_name=manufacturer_name.strip(),
                item_type=item_type.strip(),
                price=None,
                service_date=None,
                damaged=damaged.strip() if damaged else None
            )
    print(f"Successfully read manufacturer data: {items}")
    return items

def read_price_data(file_path, items):
    """
    Updates the price details for each item from the provided CSV file.
    """
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            item_id, price = row
            if item_id in items:
                items[item_id].price = float(price)
    print(f"Updated price data for items: {items}")

def read_service_date_data(file_path, items):
    """
    Updates the service dates for items based on the provided CSV file.
    """
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            item_id, service_date = row
            if item_id in items:
                items[item_id].service_date = datetime.strptime(service_date, '%m/%d/%Y')
    print(f"Updated service dates for items: {items}")

def sort_by_manufacturer_name(item):
    return item.manufacturer_name

def sort_by_item_id(item):
    return item.item_id

def sort_by_service_date(item):
    return item.service_date

def sort_by_price_desc(item):
    return -item.price

def write_full_inventory(items, output_file):
    """
    Writes a comprehensive inventory list to a CSV file, including all item details.
    The items are sorted by the manufacturer's name.
    """
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['item_ID', 'manufacturer_name', 'item_type', 'price', 'service_date', 'damaged'])
        sorted_items = sorted(items.values(), key=sort_by_manufacturer_name)
        for item in sorted_items:
            writer.writerow([
                item.item_id,
                item.manufacturer_name,
                item.item_type,
                item.price,
                item.service_date.strftime('%m/%d/%Y') if item.service_date else '',
                item.damaged if item.damaged else ''
            ])
    print(f"Full inventory written to {output_file}")

def write_item_type_inventory(items, output_dir):
    """
    Creates separate CSV files for each item type and writes the corresponding inventory data.
    """
    item_types = set(item.item_type for item in items.values())
    for item_type in item_types:
        item_file = f"{output_dir}/{item_type}Inventory.csv"
        with open(item_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['item_ID', 'manufacturer_name', 'price', 'service_date', 'damaged'])
            sorted_items = [item for item in items.values() if item.item_type == item_type]
            sorted_items.sort(key=sort_by_item_id)
            for item in sorted_items:
                writer.writerow([
                    item.item_id,
                    item.manufacturer_name,
                    item.price,
                    item.service_date.strftime('%m/%d/%Y') if item.service_date else '',
                    item.damaged if item.damaged else ''
                ])
        print(f"Inventory for item type '{item_type}' written to {item_file}")

def write_past_service_date_inventory(items, output_file):
    """
    Generates a CSV file listing items with service dates that are past due.
    The items are sorted by their service dates.
    """
    today = datetime.now()
    past_service_items = [item for item in items.values() if item.service_date and item.service_date < today]
    past_service_items.sort(key=sort_by_service_date)
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['item_ID', 'manufacturer_name', 'item_type', 'price', 'service_date', 'damaged'])
        for item in past_service_items:
            writer.writerow([
                item.item_id,
                item.manufacturer_name,
                item.item_type,
                item.price,
                item.service_date.strftime('%m/%d/%Y'),
                item.damaged if item.damaged else ''
            ])
    print(f"Past service date inventory written to {output_file}")

def write_damaged_inventory(items, output_file):
    """
    Writes a CSV file listing damaged items, sorted by price in descending order.
    """
    damaged_items = [item for item in items.values() if item.damaged]
    damaged_items.sort(key=sort_by_price_desc)
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['item_ID', 'manufacturer_name', 'item_type', 'price', 'service_date'])
        for item in damaged_items:
            writer.writerow([
                item.item_id,
                item.manufacturer_name,
                item.item_type,
                item.price,
                item.service_date.strftime('%m/%d/%Y') if item.service_date else ''
            ])
    print(f"Damaged inventory written to {output_file}")

def main():
    """
    Main function to read data from files, process it, and generate various inventory reports.
    """
    manufacturer_file = 'ManufacturerList.csv'
    price_file = 'PriceList.csv'
    service_date_file = 'ServiceDatesList.csv'
    output_dir = 'output'

    items = read_manufacturer_data(manufacturer_file)
    read_price_data(price_file, items)
    read_service_date_data(service_date_file, items)

    write_full_inventory(items, f"{output_dir}/FullInventory.csv")
    write_item_type_inventory(items, output_dir)
    write_past_service_date_inventory(items, f"{output_dir}/PastServiceDateInventory.csv")
    write_damaged_inventory(items, f"{output_dir}/DamagedInventory.csv")

if __name__ == '__main__':
    main()
