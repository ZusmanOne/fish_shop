import requests
from environs import Env


env = Env()
env.read_env()
CLIENT_ID = env('CLIENT_ID')
CLIENT_SECRET = env('CLIENT_SECRET')


def get_token():

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    token_response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    access_token = token_response.json()['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return headers


def get_all_product():
    headers = get_token()
    product_response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    return product_response.json()


def get_product(id_product):
    headers = get_token()
    url = 'https://api.moltin.com/v2/products/'
    response = requests.get(url+str(id_product), headers=headers)
    response.raise_for_status()
    return response.json()


def get_id_file(id_product):
    headers = get_token()
    url = 'https://api.moltin.com/v2/products/'
    response = requests.get(url+str(id_product), headers=headers)
    response.raise_for_status()
    id_file = response.json()['data']['relationships']['files']['data'][0]['id']
    return id_file


def download_file(id_product):
    id_file = get_id_file(id_product)
    headers = get_token()
    file_response = requests.get(f'https://api.moltin.com/v2/files/{id_file}', headers=headers)
    file_response.raise_for_status()
    url_image = file_response.json()['data']['link']['href']
    download_response = requests.get(url_image)
    with open(f'fish/{id_file}.jpg', 'wb') as file:
        file.write(download_response.content)


def get_cart(id_cart):
    cart_url = f'https://api.moltin.com/v2/carts/{id_cart}'
    headers = get_token()
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_cart_items(id_cart):
    cart_url = f'https://api.moltin.com/v2/carts/{id_cart}/items'
    headers = get_token()
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    return response.json()


def delete_cart_item(cart_id, item_id):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/carts/{cart_id}/items/{item_id}', headers=headers)
    response.raise_for_status()


def get_all_files():
    headers = get_token()
    response = requests.get('https://api.moltin.com/v2/files', headers=headers)
    response.raise_for_status()


def create_file_product():
    headers = get_token()
    data = {
        'data':
            {
                'file_name': '123'
            }
    }
    files = {
        'file_location': (None, 'https://fermaspb.ru/uploads/gallery/15549806505caf1f2a825bb.jpg'),
    }

    file_response = requests.post('https://api.moltin.com/v2/files', json=data, headers=headers, files=files)
    file_response.raise_for_status()
    file_response.raise_for_status()
    id_file = file_response.json()['data']['id']
    return id_file


def bind_product_image(id_product):
    id_file = create_file_product()
    headers = get_token()
    json_data = {
        'data': [
            {
                'type': 'file',
                'id': id_file,
            },

            ],
             }
    bind_response = requests.post(f'https://api.moltin.com/v2/products/{id_product}/relationships/files',
                                  headers=headers, json=json_data)
    bind_response.raise_for_status()


def delete_image_relationship(id_product):
    id_file = get_id_file(id_product)
    headers = get_token()
    json_data = {
        'data': [
            {
                "type": "main_image",
                'id': id_file,
            },

            ],
             }
    response = requests.delete(f'https://api.moltin.com/v2/products/{id_product}/relationships/files', headers=headers,
                               json=json_data)
    response.raise_for_status()


def delete_image(id_image):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/files/{id_image}', headers=headers)
    response.raise_for_status()


def add_product_cart(id_cart, id_product, quantity):
    headers = get_token()
    product_data = {
        'data':
            {
                "id": id_product,
                "type": 'cart_item',
                "quantity": quantity
            }
    }
    add_cart_response = requests.post(f'https://api.moltin.com/v2/carts/{id_cart}/items', headers=headers,
                                      json=product_data)
    add_cart_response.raise_for_status()


def create_product(id_product):
    headers = get_token()
    url = f'https://api.moltin.com/v2/products/{id_product}'
    data = {
        'data':
            {
                "id": id_product,
                "type": "product",
                "name": "Судак",
                "slug": "sudak",
                "sku": "3",
                "description": "Самый лучший судак, когда либо пойманный",
                "manage_stock": False,
                "price": [
                    {
                        "amount": 589,
                        "currency": "USD",
                        "includes_tax": True
                    }
                ],
                "status": "live",
                "commodity_type": "physical",
                "meta" : {
                    "stock": {
                        "level": 1,
                        "availability": "out-stock"
                    }
                }
            }
        }
    create_response = requests.put(url, headers=headers, json=data)
    create_response.raise_for_status()


def create_inventory(id_product):
    headers = get_token()
    data = {
        'data': {
            'type': 'stock-transaction',
            'action': 'increment',
            'quantity': 2100,
        },
    }
    response = requests.post(f'https://api.moltin.com/v2/inventories/{id_product}/transactions', headers=headers,
                             json=data)
    response.raise_for_status()


def create_cart(chat_id):
    headers = get_token()
    data = {
        'data':
            {
                "name": "Fish Cart",
                "id": str(chat_id),
                "description": "For Fish",
            }
    }
    response = requests.post('https://api.moltin.com/v2/carts', headers=headers, json=data)
    response.raise_for_status()


def delete_cart(id_cart):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/carts/{id_cart}', headers=headers)
    response.raise_for_status()


def create_customers(email):
    headers = get_token()
    json_data = {
        'data': {
            'type': 'customer',
            'name': email,
            'email': email,
        },
    }
    response = requests.post('https://api.moltin.com/v2/customers', headers=headers, json=json_data)
    response.raise_for_status()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    env = Env()
    env.read_env()
    client_id = env('CLIENT_ID')
    client_secret = env('CLIENT_SECRET')
    get_all_product()
