# Amazon Price Tracker

A python script that uses BeautifulSoup to scrape the current price of user defined products on amazon and compare it 
to a target price. If the current price is below the target price, an email alert is sent with the price and link.



Usage: `main.py [-h] {add,delete,list,check}`
- `add` adds a product to the list
- `delete` deletes a product from the list
- `list` lists the products being tracked
- `check` checks all products in the list for price drops
