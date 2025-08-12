import requests
from azure.cosmos import CosmosClient, exceptions
from config import config

def fetch_products():

    con = config()

    # Cosmos DB client
    client = CosmosClient(con["endpoint"], con["key"])
    db = client.get_database_client(con["database_name"])
    container = db.get_container_client(con["container_name"])

    # Fetch products
    for i in range(1, 100):
        url = f"https://dummyjson.com/products/{i}"
        response = requests.get(url)
        if response.status_code == 200:
            product = response.json()
            product["id"] = str(product["id"])
            container.upsert_item(product)
        else:
            print(f"Failed to fetch product. Status: {response.status_code}")
    
    return container


def queries(container):

    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    print(items)

def manual_product_input():

    products = []

    while True:
        name = input("Type x to exit\nProduct name:  " ).strip()
        if name == "x":
            break
        else:
            category = input("Category: ").strip()

            while True:
                try:
                    price = float(input("Price: "))
                    if price < 0:
                        print("Price has to be more than 0")
                    else:
                        break
                except ValueError:
                    print("Price has to be a number.")

            product = {
                "name" : name,
                "category" : category,
                "price" : price
            }

            products.append(product)

    print(products)

    return products

def Main():

    question = input("Create new product? y/n: ")
    if question.lower() == "y":
        manual_product_input()

    #products_container = fetch_products()
    #queries(products_container)


if __name__ == "__main__":

    Main()
