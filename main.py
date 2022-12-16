import requests
from environs import Env



def get_token():
    data = {
        'client_id': 'X4LDXp0FYnwuOy4uY8Ic9ES42uopJeUqoVkke5BDZi',
        'client_secret': 'O2qmHZ2zM0eR0lqywNeYdCR7STCOMZ7RTNYjRVGyTu',
        'grant_type': 'client_credentials',
    }
    token_response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    print(token_response.content)




def main():
    env = Env()
    env.read_env()
    key = env('CLIENT_ID')
    access_token = '8046af19091400c3e5bcab8ec1232419182f0c04'
    headers = {
        'Authorization': f'Bearer 8046af19091400c3e5bcab8ec1232419182f0c04',
        'Content-Type': 'application/json',
    }
    product_response = requests.get('https://api.moltin.com/pcm/products/', headers=headers)
    product = product_response.json()['data'][0]
    print(product)
    data_cart = {'data':
                      {
                          "name": "My cart",
                          "description": "For fish"
                      }
                }
    product_data = {
        'data':
            {
                "id": product['id'],
                "type": 'cart_item',
                "quantity": 1
            }
    }
    cart_response = requests.get('https://api.moltin.com/v2/carts/746f3d6b-5ee5-4200-8310-6733c72178c6', headers=headers)
    add_cart_response = requests.post('https://api.moltin.com/v2/carts/746f3d6b-5ee5-4200-8310-6733c72178c6/items', headers=headers, json=product_data)
    print(add_cart_response.status_code)
    print(add_cart_response.json())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

