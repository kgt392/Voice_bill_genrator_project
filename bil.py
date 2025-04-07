import csv
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import threading
from tabulate import tabulate

# Load items from CSV
def load_items_from_csv(filename="items.csv"):
    products = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products[row["item"].lower()] = float(row["price_per_kg"])
    return products

products = load_items_from_csv()

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

unit_conversions = {
    "grams": 0.001, "g": 0.001, "kg": 1, "kilogram": 1,
    "liters": 1, "l": 1, "ml": 0.001, "milliliters": 0.001,
    "half": 0.5, "quarter": 0.25, "one-fourth": 0.25
}

bill = {}
listening = False 

def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            status_label.config(text="Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            text = recognizer.recognize_google(audio).lower()
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None
    except sr.WaitTimeoutError:
        return None

def add_to_bill(item, quantity, unit):
    if item in products:
        if unit in unit_conversions:
            quantity *= unit_conversions[unit]
        total_price = products[item] * quantity
        
        if item in bill:
            bill[item]["quantity"] += quantity
        else:
            bill[item] = {"price_per_kg": products[item], "quantity": quantity}

        messagebox.showinfo("Item Added", f"Added {quantity} kg/l of {item}: ₹{total_price:.2f}")
    else:
        messagebox.showerror("Error", "Item not found!")

def continuous_listening():
    global listening
    listening = True
    while listening:
        text = recognize_speech()
        if text:
            if "check out" in text:
                generate_receipt()
                break
            # words = text.split()
            # if len(words) >= 3:
            #     item = words[0]
            #     quantity = float(words[1]) if words[1].replace('.', '', 1).isdigit() else unit_conversions.get(words[1], 1)
            #     unit = words[2] if len(words) > 2 else "kg"
            #     add_to_bill(item, quantity, unit)
            words = text.split()
            if len(words) >= 3:
                item = " ".join(words[:-2])  # Combine all words except the last two
                quantity = float(words[-2]) if words[-2].replace('.', '', 1).isdigit() else unit_conversions.get(words[-2], 1)
                unit = words[-1] if len(words) > 2 else "kg"
                add_to_bill(item, quantity, unit)

            else:
                messagebox.showerror("Error", "Invalid format. Say: 'item quantity unit'")


def start_listening():
    threading.Thread(target=continuous_listening, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="Listening Stopped.")

# def generate_receipt():
#     stop_listening()
#     receipt_text = "\n===== FINAL BILL =====\n"
#     bill_data = []
#     total_amount = 0
    
#     for item, details in bill.items():
#         total = details["price_per_kg"] * details["quantity"]
#         total_amount += total
#         bill_data.append([item.capitalize(), f"{details['quantity']:.2f}", details["price_per_kg"], f"{total:.2f}"])
    
#     receipt_text += tabulate(bill_data, headers=["Item", "Qty (kg/l)", "Price per kg/l", "Total"], tablefmt="grid")
#     receipt_text += f"\n\nTOTAL AMOUNT: ₹{total_amount:.2f}\n======================"
#     speak(f"The total bill amount is {total_amount} rupees")
#     messagebox.showinfo("Final Bill", receipt_text)

def generate_receipt():
    stop_listening()
    
    receipt_text = "===== FINAL BILL =====\n"
    bill_data = []
    total_amount = 0
    
    for item, details in bill.items():
        total = details["price_per_kg"] * details["quantity"]
        total_amount += total
        bill_data.append([item.capitalize(), f"{details['quantity']:,.2f}", f"{details['price_per_kg']:.2f}", f"{total:,.2f}"])
    
    receipt_text += tabulate(bill_data, headers=["Item", "Qty (kg/l)", "Price per kg/l", "Total"], tablefmt="psql")
    receipt_text += f"\n\nTOTAL AMOUNT: ₹{total_amount:,.2f}\n======================"
    
    # Speak total amount
    speak(f"The total bill amount is {total_amount} rupees")
    
    # Create a new window for the receipt
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Final Bill")
    receipt_window.geometry("700x400")

    text_area = tk.Text(receipt_window, wrap="none", font=("Courier", 12))  
    text_area.insert(tk.END, receipt_text)
    text_area.config(state="disabled") 
    text_area.pack(expand=True, fill="both")

    close_button = tk.Button(receipt_window, text="Close", command=receipt_window.destroy)
    close_button.pack(pady=5)


def exit_app():
    root.quit()

# GUI Setup
root = tk.Tk()
root.title("Voice-Based Bill Generator")
root.geometry("400x300")

title_label = tk.Label(root, text="Voice-Based Bill Generator", font=("Arial", 14))
title_label.pack(pady=10)

status_label = tk.Label(root, text="Click 'Start Listening' to begin", font=("Arial", 10))
status_label.pack()

listen_button = tk.Button(root, text="Start Listening", command=start_listening, font=("Arial", 12))
listen_button.pack(pady=10)

checkout_button = tk.Button(root, text="Checkout", command=generate_receipt, font=("Arial", 12))
checkout_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app, font=("Arial", 12))
exit_button.pack(pady=10)

root.mainloop()
