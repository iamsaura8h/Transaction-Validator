import tkinter as tk
from tkinter import filedialog
import easyocr
import re

def upload_image():
    global image_path
    image_path = filedialog.askopenfilename()

def extract_transaction_id(file_path):
    # Create a reader for English language
    reader = easyocr.Reader(['en'])

    # Read from the image file
    result = reader.readtext(image_path)

    # Initialize an empty string to store all detected text
    text = ''

    # Append all detected text to the string
    for detection in result:
        text += detection[1] + ' '

    # Search for the transaction ID
    match = re.search(r'UPI transaction ID: (\d+)', text)
    if match:
        transaction_id = match.group(1)
        transaction_id_label.config(text='Transaction ID: ' + transaction_id)

        # Check if the transaction ID is already in the file
        with open(file_path, 'r') as file:
            if transaction_id in file.read():
                print('Transaction ID is repeated.')
            else:
                # If not, append it to the file
                with open(file_path, 'a') as file:
                    file.write(transaction_id + '\n')
    else:
        transaction_id_label.config(text='Transaction ID not found in the image.')

root = tk.Tk()
root.geometry("200x200")
root.title("Transaction Validator")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

submit_button = tk.Button(root, text="Submit", command=lambda: extract_transaction_id('transaction_ids.txt'))
submit_button.pack()

transaction_id_label = tk.Label(root, text='')
transaction_id_label.pack()

root.mainloop()
