import requests
from azure.cosmos import CosmosClient, exceptions
from config import config

con = config()
print(con)

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

print("******************")

# Query average price
query = "SELECT VALUE AVG(c.price) FROM c"
items = list(container.query_items(query=query, enable_cross_partition_query=True))
avg_price = items[0] 
print(f"Average price: {avg_price}")

print("******************")
# Add a product to my database
product = {
    "id" : "1001",
    "name" : "Wow Cool product",
    "category" : "Books",
    "price" : 39.99
}

#container.create_item(body=product)
print("Created item: ", product)
