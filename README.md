# Voice_bill_genrator_project


# 🛒 Voice-Based Bill Generator 🗣️🧾

A Python-based voice-controlled billing system for grocery stores. This project allows users to generate bills simply by speaking the names of items. The system recognizes the item, adds it to the bill, calculates the total, and displays the final amount — all using voice input!

---

## 📌 Abstract

The Voice-Based Bill Generator is a smart, user-friendly billing solution designed to simplify billing operations in small retail and grocery stores. It uses voice recognition to identify grocery items and automates the billing process, saving time and reducing manual errors.

---

## 🎯 Aim

To develop a voice-activated billing system that helps users generate grocery bills efficiently and accurately using Python and speech recognition.

---

## 🎯 Objectives

- To recognize and process user voice input.
- To map spoken item names to predefined prices.
- To calculate the total cost dynamically.
- To display and store the final bill.

---

## 🛠️ Methodology

1. **Speech Recognition**:  
   Uses the `speech_recognition` library to capture and convert voice input into text.

2. **Item Mapping**:  
   The recognized item is matched against a predefined dictionary containing item names and prices.

3. **Billing Logic**:  
   Each recognized item is added to the bill, and the total is updated accordingly.

4. **Output Display**:  
   Final bill including items and total is printed in a user-friendly format.

---

## 🧪 Results

- Successfully recognized spoken item names using a microphone.
- Accurately mapped items to prices and calculated totals.
- Displayed a final bill with all added items and overall cost.
- Improved billing speed and ease for users unfamiliar with traditional input devices.

---

## ✅ Conclusion

The Voice-Based Bill Generator provides an intuitive way to handle grocery billing using voice commands. It is especially useful for people with accessibility needs or small shops where traditional billing methods can be time-consuming. With minimal setup, it can be customized and deployed to enhance daily operations.

---

## 📚 Technologies Used

- Python
- `speech_recognition`
- `pyaudio`
- `os`, `datetime` modules

---

## 📂 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kgt392/voice-bill-generator.git
