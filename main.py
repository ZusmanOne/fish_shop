import requests
from environs import Env
from datetime import datetime


def get_token():
    data = {
        'client_id': 'X4LDXp0FYnwuOy4uY8Ic9ES42uopJeUqoVkke5BDZi',
        'client_secret': 'O2qmHZ2zM0eR0lqywNeYdCR7STCOMZ7RTNYjRVGyTu',
        'grant_type': 'client_credentials',
    }
    token_response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    #expires_token = token_response.json()['expires']
    return token_response.json()


def get_product():
    authentication_data = get_token()
    access_token = authentication_data['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    product_response = requests.get('https://api.moltin.com/pcm/products/', headers=headers)
    print(product_response.json())
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_product()

