import streamlit as st
import random
import time
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Shah Food Billing System", layout="wide")

# --- Custom CSS for Animation and Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5dc; /* Similar to cornsilk2 */
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px;
        font-family: 'Arial';
    }
    /* Simple Glow Animation */
    @keyframes glow {
        0% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ff00de; }
        50% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00de; }
        100% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ff00de; }
    }
    .animated-text {
        animation: glow 2s ease-in-out infinite;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Title Section ---
st.markdown("<h1 style='text-align: center; color: white; background-color: black; padding: 10px; border-radius: 10px;'>Shah Food Billing System</h1>", unsafe_allow_html=True)

# --- State Management for Calculator ---
if 'calc_input' not in st.session_state:
    st.session_state.calc_input = ""

# --- Layout Columns ---
col_menu, col_receipt = st.columns([2, 1])

with col_menu:
    st.subheader("Menu Items")
    
    # Nested columns for Drinks and Food
    col_drinks, col_food = st.columns(2)
    
    with col_drinks:
        st.markdown("### 🥤 Drinks")
        # Item: Price mapping
        drinks_prices = {
            "Sprite": 20, "Pepsi": 25, "Diet Coke": 30, "Frappe": 50,
            "Cappuccino": 60, "Fanta": 20, "Coca Cola": 30, "Cold Coffee": 50
        }
        drink_inputs = {}
        for drink, price in drinks_prices.items():
            check = st.checkbox(f"{drink} (Rs {price})", key=f"chk_{drink}")
            drink_inputs[drink] = st.number_input(f"Qty {drink}", min_value=0, value=0, step=1, disabled=not check, key=f"val_{drink}")

    with col_food:
        st.markdown("### 🍔 Food")
        food_prices = {
            "Paneer Tikka": 60, "Veg Burger": 35, "Pasta": 40, "Rice Plate": 50,
            "Sandwich": 20, "Fries": 40, "Noodles": 50, "Cake": 50
        }
        food_inputs = {}
        for food, price in food_prices.items():
            check = st.checkbox(f"{food} (Rs {price})", key=f"chk_{food}")
            food_inputs[food] = st.number_input(f"Qty {food}", min_value=0, value=0, step=1, disabled=not check, key=f"val_{food}")

    # --- Totals Calculation ---
    st.divider()
    st.subheader("Payment Information")
    
    total_drink_cost = sum(drink_inputs[d] * drinks_prices[d] for d in drinks_prices)
    total_food_cost = sum(food_inputs[f] * food_prices[f] for f in food_prices)
    service_charge = 1.59
    subtotal = total_drink_cost + total_food_cost + service_charge
    tax = subtotal * 0.15
    total_payable = subtotal + tax

    c1, c2, c3 = st.columns(3)
    c1.metric("Cost of Drinks", f"Rs {total_drink_cost:.2f}")
    c2.metric("Cost of Food", f"Rs {total_food_cost:.2f}")
    c3.metric("Service Charge", f"Rs {service_charge:.2f}")
    
    c1.metric("Paid Tax (15%)", f"Rs {tax:.2f}")
    c2.metric("Sub Total", f"Rs {subtotal:.2f}")
    c3.metric("Total Payable", f"Rs {total_payable:.2f}", delta_color="inverse")

with col_receipt:
    # --- Calculator Section ---
    st.subheader("🔢 Quick Calc")
    calc_display = st.text_input("Calculator", value=st.session_state.calc_input, key="display", label_visibility="collapsed")
    
    def add_to_calc(char):
        st.session_state.calc_input += str(char)
    
    def calculate_result():
        try:
            st.session_state.calc_input = str(eval(st.session_state.calc_input))
        except:
            st.session_state.calc_input = "Error"

    def clear_calc():
        st.session_state.calc_input = ""

    # Calculator Buttons Grid
    grid = [["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["C", "0", "=", "+"]]
    for row in grid:
        cols = st.columns(4)
        for i, char in enumerate(row):
            if char == "=":
                cols[i].button(char, on_click=calculate_result, use_container_width=True)
            elif char == "C":
                cols[i].button(char, on_click=clear_calc, use_container_width=True)
            else:
                cols[i].button(char, on_click=add_to_calc, args=(char,), use_container_width=True)

    st.divider()
    
    # --- Receipt Generation ---
    st.subheader("🧾 Receipt")
    if st.button("Generate Receipt", use_container_width=True):
        receipt_no = random.randint(10908, 500876)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        receipt_text = f"Receipt Ref: Bill{receipt_no}\nDate: {now}\n"
        receipt_text += "-"*40 + "\nItems\t\t\tQty\tPrice\n" + "-"*40 + "\n"
        
        for item, qty in {**drink_inputs, **food_inputs}.items():
            if qty > 0:
                receipt_text += f"{item[:12]:<15}\t{qty}\n"
        
        receipt_text += "-"*40
        receipt_text += f"\nCost of Drinks: Rs {total_drink_cost:.2f}"
        receipt_text += f"\nCost of Food:   Rs {total_food_cost:.2f}"
        receipt_text += f"\nTax Paid:       Rs {tax:.2f}"
        receipt_text += f"\nTotal Cost:     Rs {total_payable:.2f}"
        
        st.code(receipt_text, language="text")

# --- Animated Footer ---
st.markdown(f"""
    <div class="footer">
        <p class="animated-text">Project Created by :- Himanshu Shah</p>
        <p style="font-size: 0.8rem;">© {datetime.now().year} All Rights Reserved 2026</p>
    </div>
    """, unsafe_allow_html=True)
