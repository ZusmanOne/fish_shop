import requests
from environs import Env
import time


def get_token(client_id, secret_id):
    data = {
        'client_id': client_id,
        'client_secret': secret_id,
        'grant_type': 'client_credentials',
    }
    token_response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    token_response.raise_for_status()
    access_token = token_response.json()['access_token']
    authorization_data = {
        'authorization': f'Bearer {access_token}',
        'expires': token_response.json()['expires'],
    }
    return authorization_data


def get_all_product(token):
    headers = {'Authorization': token}
    product_response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    product_response.raise_for_status()
    return product_response.json()


def get_product(product_id, token):
    headers = {'Authorization': token}
    response = requests.get(f'https://api.moltin.com/v2/products/{product_id}', headers=headers)
    response.raise_for_status()
    return response.json()


def get_id_file(product_id,token):
    headers = {'Authorization': token}
    url = 'https://api.moltin.com/v2/products/'
    response = requests.get(url+str(product_id), headers=headers)
    response.raise_for_status()
    file_id = response.json()['data']['relationships']['files']['data'][0]['id']
    return file_id


def download_file(product_id, token):
    id_file = get_id_file(product_id)
    headers = {'Authorization': token}
    file_response = requests.get(f'https://api.moltin.com/v2/files/{id_file}', headers=headers)
    file_response.raise_for_status()
    url_image = file_response.json()['data']['link']['href']
    download_response = requests.get(url_image)
    with open(f'fish/{id_file}.jpg', 'wb') as file:
        file.write(download_response.content)


def get_cart(cart_id, token):
    cart_url = f'https://api.moltin.com/v2/carts/{cart_id}'
    headers = {'Authorization': token}
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_cart_items(cart_id, token):
    cart_url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
    headers = {'Authorization': token}
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    return response.json()


def delete_cart_item(cart_id, item_id, token):
    headers = {'Authorization': token}
    response = requests.delete(f'https://api.moltin.com/v2/carts/{cart_id}/items/{item_id}', headers=headers)
    response.raise_for_status()


def get_all_files(token):
    headers = {'Authorization': token}
    response = requests.get('https://api.moltin.com/v2/files', headers=headers)
    response.raise_for_status()


def create_file_product(token):
    headers = {'Authorization': token}
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
    file_id = file_response.json()['data']['id']
    return file_id


def bind_product_image(product_id, token):
    file_id = create_file_product()
    headers = {'Authorization': token}
    product_data = {
        'data': [
            {
                'type': 'file',
                'id': file_id,
            },
        ],
    }
    bind_response = requests.post(f'https://api.moltin.com/v2/products/{product_id}/relationships/files',
                                  headers=headers, json=product_data)
    bind_response.raise_for_status()


def delete_image_relationship(product_id, token):
    file_id = get_id_file(product_id)
    headers = {'Authorization': token}
    json_data = {
        'data': [
            {
                "type": "main_image",
                'id': file_id,
            },

            ],
             }
    response = requests.delete(f'https://api.moltin.com/v2/products/{product_id}/relationships/files', headers=headers,
                               json=json_data)
    response.raise_for_status()


def delete_image(image_id, token):
    headers = {'Authorization': token}
    response = requests.delete(f'https://api.moltin.com/v2/files/{image_id}', headers=headers)
    response.raise_for_status()


def add_product_cart(cart_id, product_id, quantity, token):
    headers = {'Authorization': token}
    product_data = {
        'data':
            {
                "id": product_id,
                "type": 'cart_item',
                "quantity": quantity
            }
    }
    add_cart_response = requests.post(f'https://api.moltin.com/v2/carts/{cart_id}/items', headers=headers,
                                      json=product_data)
    add_cart_response.raise_for_status()


def create_inventory(product_id, token):
    headers = {'Authorization': token}
    data = {
        'data': {
            'type': 'stock-transaction',
            'action': 'increment',
            'quantity': 2100,
        },
    }
    response = requests.post(f'https://api.moltin.com/v2/inventories/{product_id}/transactions', headers=headers,
                             json=data)
    response.raise_for_status()


def create_cart(chat_id, token):
    headers = {'Authorization': token}
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


def delete_cart(cart_id, token):
    headers = {'Authorization': token}
    response = requests.delete(f'https://api.moltin.com/v2/carts/{cart_id}', headers=headers)
    response.raise_for_status()


def create_customers(email, token):
    headers = {'Authorization': token}
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


