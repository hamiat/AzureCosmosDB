import requests
from azure.cosmos import CosmosClient, exceptions
from config import config

def Fetch_Products():

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


def Queries(container):

    # Query average price
    query = "SELECT VALUE AVG(c.price) FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    avg_price = items[0] 
    print(f"Average price: {avg_price}")

    # Add a product to my database
    product = {
        "id" : "1001",
        "name" : "Rick and Morty: Vol 1",
        "category" : "Books",
        "price" : 39.99
    }

    #container.create_item(body=product)

def Main():
    products_container = Fetch_Products()
    Queries(products_container)


if __name__ == "__main__":
    Main()
