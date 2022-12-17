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
    #expires_token = token_response.json()['expires']
    #print(token_response.json())
    return token_response.json()


def get_all_product():
    authentication_data = get_token()
    access_token = authentication_data['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    product_response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    # print(product_response.json())
    return product_response.json()


def get_product(id_product):
    authentication_data = get_token()
    access_token = authentication_data['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    url = 'https://api.moltin.com/v2/products/'
    product_response = requests.get(url+str(id_product), headers=headers)
    #print(product_response.content)
    return product_response.json()


def get_cart():
    cart_url = 'https://api.moltin.com/v2/carts/:reference'
    headers = {
        'Authorization': f'Bearer 0949b84e34ea992b9af450a7849faebd858c1441',
    }
    cart_response = requests.get(cart_url,headers=headers)
    print(cart_response.json())

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
def create_product():
    authentication_data = get_token()
    access_token = authentication_data['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        }
    url = 'https://api.moltin.com/v2/products'
    data = {
        'data':
            {
                "type": "product",
                "name": "Red Fish",
                "slug": "red-fish",
                "sku": "4",
                "description": "прямиком из мурманска",
                "manage_stock": True,
                "price": [
                    {
                        "amount": 700,
                        "currency": "USD",
                        "includes_tax": True
                    }
                ],
                "status": "live",
                "commodity_type": "physical"
            }
        }
    create_response = requests.post(url, headers=headers, json=data)
    print(create_response.status_code)
    print(create_response.content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    env = Env()
    env.read_env()
    client_id = env('CLIENT_ID')
    client_secret = env('CLIENT_SECRET')
    get_token()
    # get_product('d13b8eff-6cc9-4ca3-b17b-0d54bcd9bf03')
    #get_product('49212a9f-df95-4b7b-93e0-b5cca63114fb')
    # create_product()

