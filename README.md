# Amazon Price Tracker

A python script that uses BeautifulSoup to scrape the current price of user defined products on amazon and compare it 
to a target price. If the current price is below the target price, an email alert is sent with the price and link.



Usage: `main.py [-h] {add,delete,list,check}`
- `add` adds a product to the list
- `delete` deletes a product from the list
- `list` lists the products being tracked
- `check` checks all products in the list for price drops

Required Environment Variables:
- `MY_EMAIL` = gmail address to send from
- `PASSWORD` = gmail password
- `TARGET_EMAIL` = email address to send the alert to 

*Note: In order for this to work, you must enable less secure apps for your Google account. For this reason, I **strongly** recommend using a new gmail
account rather than your main.*

[Enabling Less Secure Access in Gmail](https://bytexd.com/less-secure-apps-gmail/)
