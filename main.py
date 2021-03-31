import json
import smtplib
import requests
from bs4 import BeautifulSoup
import os
import lxml
import argparse

MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')
TARGET_EMAIL = os.getenv('TARGET_EMAIL')


def send_email(to_address, subject, message):
    # Sends an email message using the email server info provided in config.py
    #
    # args:
    #   to_address: email address of the recipient
    #   subject: subject of email
    #   message: message to send
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=to_address,
            msg=f"Subject: {subject}\n\n{message}".encode('utf-8')
        )


def get_product_info(product_address):
    """
    Checks for the name and current price for the Amazon product at the web address provided.
    :param product_address: Web Address of the Amazon product to check
    :return: Returns the product name and current price as a tuple
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(product_address, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    product_title = soup.find("span", id="productTitle").get_text(strip=True)

    if soup.find("span", id="priceblock_saleprice") is not None:
        current_price = float(soup.find("span", id="priceblock_saleprice").get_text().split("$")[1])
    else:
        current_price = float(soup.find("span", id="priceblock_ourprice").get_text().split("$")[1])

    return product_title, current_price


def add_product(product_address, target_price):
    """
    Adds the Amazon product at the provided address to the list of items to track with the provided target price.
    :param product_address: Amazon web address for product to track
    :param target_price: The target price to watch for
    :return: None
    """
    product_info = get_product_info(product_address)
    product_name = product_info[0]
    current_price = product_info[1]

    print(product_name)
    print(f"Current Price: {current_price}")
    user_input = input(f"Save? (Y/N): ").lower()

    if user_input == 'y' or user_input == 'yes':
        new_data = {
            product_name: {
                'link': product_address,
                'target_price': target_price
            }
        }

        try:
            with open("products.json", 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            print('products.json not found, creating new file')
            with open('products.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
            print('Product Added')
        else:
            data.update(new_data)
            with open('products.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
            print("Product Added")


def list_products():
    """
    Lists products currently being track
    :return: None
    """
    try:
        with open("products.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print("products.json not found, you are not tracking any products.")
    else:
        print("------------------------------------------------------------------")
        for index, product in enumerate(data):
            print(f"#{index}")
            print(f"Name: {product}")
            print(f"Address: {data[product]['link']}")
            print(f"Target Price: {data[product]['target_price']}")
            print("------------------------------------------------------------------")


def remove_product():
    """
    Lists products being tracked then prompts user for a product to delete from the list.
    :return: None
    """
    try:
        with open("products.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print('products.json not found, there are no products saved.')
    else:
        product_list = [product for product in data]
        for index, product in enumerate(product_list):
            print(f"{index}: {product}")
        user_input = int(input("Which product do you want to remove? (Number): "))
        if user_input in range(len(product_list)):
            del data[product_list[user_input]]

            with open('products.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
            print("Product Removed.")


def check_prices():
    try:
        with open("products.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print("products.json not found, you are not tracking any products.")
        return False
    message = "Price Alerts:\n"
    alerts_exist = False
    for index, product in enumerate(data):
        product_info = get_product_info(data[product]['link'])
        print(f"#{index} - {product}")
        print(f"Target Price: {data[product]['target_price']} Current Price: {product_info[1]}")

        if product_info[1] <= data[product]['target_price']:
            alerts_exist = True
            message += f"{product}\n" \
                       f"{data[product]['link']}\n" \
                       f"Target Price: {data[product]['target_price']} Current Price: {product_info[1]}"
    if alerts_exist:
        send_email(to_address=TARGET_EMAIL, subject="Price Drop Alert", message=message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="The action to perform.", choices=['add', 'delete', 'list', 'check'])

    args = parser.parse_args()

    if args.action == 'add':
        product_link = input("Paste the address of the Amazon product you want to track: ")
        target_price = float(input("Input the target price to watch for: "))
        add_product(product_link, target_price)
    elif args.action == 'delete':
        remove_product()
    elif args.action == 'list':
        list_products()
    elif args.action == 'check':
        check_prices()


if __name__ == '__main__':
    main()
