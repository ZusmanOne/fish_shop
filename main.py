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
    #token_response.raise_for_status()
    return headers


def get_all_product():
    headers = get_token()
    product_response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    #print(product_response.json())
    return product_response.json()


def get_product(id_product):
    headers = get_token()
    url = 'https://api.moltin.com/v2/products/'
    response = requests.get(url+str(id_product), headers=headers)
    response.raise_for_status()
    #print(product_response.json())
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
    file_response = requests.get(f'https://api.moltin.com/v2/files/{id_file}',headers=headers)
    file_response.raise_for_status()
    url_image = file_response.json()['data']['link']['href']
    download_response = requests.get(url_image)
    with open(f'fish/{id_file}.jpg','wb') as file:
        file.write(download_response.content)


def get_cart(id_cart):
    cart_url = f'https://api.moltin.com/v2/carts/{id_cart}'
    headers = get_token()
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    #print(cart_response.json())
    return response.json()


def get_cart_items(id_cart):
    cart_url = f'https://api.moltin.com/v2/carts/{id_cart}/items'
    headers = get_token()
    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()
    #print(response.json())
    return response.json()


def delete_cart_item(cart_id,item_id):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/carts/{cart_id}/items/{item_id}', headers=headers)
    response.raise_for_status()
    print(response.status_code)


def get_all_files():
    headers = get_token()
    response = requests.get('https://api.moltin.com/v2/files', headers=headers)
    response.raise_for_status()
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
    file_response.raise_for_status()
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


def add_product_cart(id_cart,id_product,quantity):
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
    print(add_cart_response.status_code)
    #print(add_cart_response.json())



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


def create_cart(chat_id):
    headers = get_token()
    data = {
        'data':
            {
            "name": "Fish Cart",
            "id" : str(chat_id),
            "description": "For Fish",
        }

    }
    response = requests.post('https://api.moltin.com/v2/carts',headers=headers,json=data)
    response.raise_for_status()
    print(response.json())


def delete_cart(id_cart):
    headers = get_token()
    response = requests.delete(f'https://api.moltin.com/v2/carts/{id_cart}', headers=headers)
    print(response.status_code)


def get_customers():
    headers = get_token()
    response = requests.get(f'https://api.moltin.com/v2/customers', headers=headers)
    response.raise_for_status()
    print(response.status_code)
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
    #get_cart('305151571')
    # add_product_cart('805755e7-892a-4527-b122-c230bfc728ae')
    #create_inventory('49212a9f-df95-4b7b-93e0-b5cca63114fb')
    #create_cart(305151573)
    #delete_cart_item(305151573,'6e09329b-de85-480b-a6e3-bec35c8da19b')
    # get_cart_items(305151573)
    get_customers()