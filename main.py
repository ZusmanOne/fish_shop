import requests
from environs import Env
from datetime import datetime


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
    #print(product_response.json())
    return product_response.json()


def get_product(id_product):
    headers = get_token()
    url = 'https://api.moltin.com/v2/products/'
    product_response = requests.get(url+str(id_product), headers=headers)
    #print(product_response.json())
    return product_response.json()


def get_id_file(id_product):
    headers = get_token()
    url = 'https://api.moltin.com/v2/products/'
    product_response = requests.get(url+str(id_product), headers=headers)
    id_file = product_response.json()['data']['relationships']['files']['data'][0]['id']
    return id_file


def download_file(id_product):
    id_file = get_id_file(id_product)
    headers = get_token()
    file_response = requests.get(f'https://api.moltin.com/v2/files/{id_file}',headers=headers)
    url_image = file_response.json()['data']['link']['href']
    download_response = requests.get(url_image)
    with open(f'fish/{id_file}.jpg','wb') as file:
        file.write(download_response.content)


def get_cart(id_cart):
    cart_url = f'https://api.moltin.com/v2/carts/{id_cart}'
    headers = get_token()
    cart_response = requests.get(cart_url, headers=headers)
    print(cart_response.json())


def get_all_files():
    headers = get_token()
    response_files = requests.get('https://api.moltin.com/v2/files', headers=headers)
    # print(response_files.json())




# def get_file_product():
#     headers = get_token()
#     bind_response = requests.get(
#         'https://api.moltin.com/v2/products/805755e7-892a-4527-b122-c230bfc728ae/relationships/files', headers=headers)
#     print(id_file = bind_response.json()['relationships'])
#     return bind_response.json()

# def download_file():
#     headers = get_token()
#     file_id =


def create_file_product():
    headers = get_token()
    data = {
        'data':{
            'file_name':'123'

        }

    }
    files = {
        'file_location': (None, 'https://fermaspb.ru/uploads/gallery/15549806505caf1f2a825bb.jpg'),
    }

    file_response = requests.post('https://api.moltin.com/v2/files', json=data, headers=headers, files=files)
    # print(file_response.status_code)
    # print(file_response.json())
    #file_response.raise_for_status()
    id_file = file_response.json()['data']['id']
    # print(id_file)
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
    # product_id =
    bind_response = requests.post(f'https://api.moltin.com/v2/products/{id_product}/relationships/files', headers=headers,
                             json=json_data)
    # print(bind_response.status_code)
    # print(bind_response.json())


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
    # product_id =
    bind_response = requests.delete(f'https://api.moltin.com/v2/products/{id_product}/relationships/files', headers=headers,
                             json=json_data)
    # print(bind_response.status_code)
    # print(bind_response.json())


def delete_image(id_image):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/files/{id_image}', headers=headers)
    # print(response.status_code)


def add_product_cart(id_product,quantity):
    headers = get_token()
    product_data = {
        'data':
            {
                "id": id_product,
                "type": 'cart_item',
                "quantity": quantity
            }
    }
    add_cart_response = requests.post(f'https://api.moltin.com/v2/carts/c56089fe-6d36-4f6e-9686-9cbac5389bc3/items', headers=headers,
                                      json=product_data)
    print(add_cart_response.status_code)
    print(add_cart_response.json())

def main():
    print(access_token)
    env = Env()
    env.read_env()
    key = env('CLIENT_ID')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    product_response = requests.get('https://api.moltin.com/pcm/products/', headers=headers)
    product = product_response.json()
    for i in product['data']:
        print(i['attributes']['name'])
    # data_cart = {'data':
    #                   {
    #                       "name": "My cart",
    #                       "description": "For fish"
    #                   }
    #             }
    # product_data = {
    #     'data':
    #         {
    #             "id": product['id'],
    #             "type": 'cart_item',
    #             "quantity": 1
    #         }
    # }
    # cart_response = requests.get('https://api.moltin.com/v2/carts/746f3d6b-5ee5-4200-8310-6733c72178c6', headers=headers)
    # #add_cart_response = requests.post('https://api.moltin.com/v2/carts/746f3d6b-5ee5-4200-8310-6733c72178c6/items', headers=headers, json=product_data)
    # print(cart_response.status_code)
    # print(cart_response.json())


def create_product(id_product):
    headers = get_token()
    url = f'https://api.moltin.com/v2/products/{id_product}'
    data = {
        'data':
            {
                "id": id_product,
                "type": "product",
                "name": "Камчатский краб",
                "slug": "crab",
                "sku": "5",
                "description": "прямиком с камчатки",
                "manage_stock": False,
                "price": [
                    {
                        "amount": 900,
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
    print(create_response.status_code)
    print(create_response.json())


def create_inventory(id_product):
    headers = get_token()
    data = {
        'data': {
            'type': 'stock-transaction',
            'action': 'increment',
            'quantity': 2100,
        },
    }
    response = requests.post(f'https://api.moltin.com/v2/inventories/{id_product}/transactions', headers=headers,json=data)
    print(response.json())
    print(response.status_code)


def create_cart():
    headers = get_token()
    data = {
        'data':
            {
            "name": "Fish Cart",
            "description": "For Fish",
        }

    }
    response = requests.post('https://api.moltin.com/v2/carts',headers=headers,json=data)
    response.raise_for_status()
    print(response.json())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    env = Env()
    env.read_env()
    client_id = env('CLIENT_ID')
    client_secret = env('CLIENT_SECRET')
    #create_file_product()
    #get_product('805755e7-892a-4527-b122-c230bfc728ae')
    #get_product('98b4bc7d-660c-4baa-bab1-486ad0d9bfbe')
    #create_product('98b4bc7d-660c-4baa-bab1-486ad0d9bfbe')
    # create_product()
    #get_all_product()
    #get_all_files()
    #bind_product_image('805755e7-892a-4527-b122-c230bfc728ae')
    # get_file_product()
    #get_id_file('49212a9f-df95-4b7b-93e0-b5cca63114fb')
    #download_file('805755e7-892a-4527-b122-c230bfc728ae')
    #delete_image_relationship('49212a9f-df95-4b7b-93e0-b5cca63114fb')
    #delete_image('dc40a640-222b-46e2-82bc-13514c9c1988')
    get_cart('c56089fe-6d36-4f6e-9686-9cbac5389bc3')
    # add_product_cart('805755e7-892a-4527-b122-c230bfc728ae')
    #create_inventory('49212a9f-df95-4b7b-93e0-b5cca63114fb')
    #create_cart()