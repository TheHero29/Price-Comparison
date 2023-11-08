import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def compare_products():
    amazon_url = amazon_entry.get()
    snapdeal_url = snapdeal_entry.get()

    amazon_info = get_amazon_product_info(amazon_url)
    snapdeal_info = get_snapdeal_product_info(snapdeal_url)

    # Clear any previous results
    for row in result_tree.get_children():
        result_tree.delete(row)

    # Insert the comparison results into the table
    result_tree.insert('', 'end', values=("Website", "Amazon", "Snapdeal"))
    result_tree.insert('', 'end', values=("Product Name", amazon_info["name"], snapdeal_info["name"]))
    result_tree.insert('', 'end', values=("Price", amazon_info["price"], snapdeal_info["price"]))
    result_tree.insert('', 'end', values=("Rating", amazon_info["rating"], snapdeal_info["rating"]))

def get_amazon_product_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        name_element = soup.find('span', {'id': 'productTitle'})
        price_element = soup.find('span', {'class':'a-price-whole'})
        rating_element = soup.find('span', {'data-hook':'rating-out-of-text'})

        name = name_element.text.strip() if name_element else "Product name not found"
        price = price_element.text.strip() if price_element else "Price not found"
        rating = rating_element.text.strip() if rating_element else "Rating not found"
        rating=rating[:3]
        price="₹"+price[:-1]
        return {"name": name, "price": price, "rating": rating}
    else:
        get_amazon_product_info(url)

def get_snapdeal_product_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        name_element = soup.find('h1', itemprop='name')
        price_element = soup.find('span', {'class': 'payBlkBig'})
        rating_element = soup.find('span', itemprop='ratingValue')

        name = name_element.text.strip() if name_element else "Product name not found"
        price = price_element.text.strip() if price_element else "Price not found"
        rating = rating_element.text.strip() if rating_element else "Rating not found"

        price="₹"+price
        return {"name": name, "price": price, "rating": rating}
    else:
        return {"name": "Failed to retrieve Snapdeal info", "price": "", "rating": ""}

# Create the main application window
root = tk.Tk()
root.title("Product Comparison")

# Increase the window size
root.geometry("600x400")

# Create and arrange input elements
amazon_label = tk.Label(root, text="Amazon URL:")
amazon_entry = tk.Entry(root, width=50)
snapdeal_label = tk.Label(root, text="Snapdeal URL:")
snapdeal_entry = tk.Entry(root, width=50)
compare_button = tk.Button(root, text="Compare Products", command=compare_products)

amazon_label.pack()
amazon_entry.pack()
snapdeal_label.pack()
snapdeal_entry.pack()
compare_button.pack()

# Create the result table
result_tree = ttk.Treeview(root, columns=('Field', 'Amazon', 'Snapdeal'), show='headings')
result_tree.heading('Field', text='Field')
result_tree.heading('Amazon', text='Amazon')
result_tree.heading('Snapdeal', text='Snapdeal')
result_tree.pack()

# Start the GUI main loop
root.mainloop()

