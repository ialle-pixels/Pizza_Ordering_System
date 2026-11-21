
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -------------------- MENU AND PRICES --------------------

pizza_prices = {
    "Diavola": 250,
    "Cheesy Spinach": 280,
    "Margherita": 220,
    "Quatro Formaggio": 300
}

size_prices = {
    "Small": 0,
    "Medium": 50,
    "Large": 100
}

topping_prices = {
    "Extra Cheese": 30,
    "Mushrooms": 40,
    "Bacon": 50
}

# -------------------- MAIN WINDOW --------------------

window = tk.Tk()
window.title("Pizza Ordering System")
window.geometry("760x800")
window.minsize(500, 400)
window.configure(bg="#eaf4ff")

# -------------------- WINTER BLUE COLORS --------------------

BG = "#eaf4ff"
PANEL = "#d6eaff"
BLUE = "#2878c7"
DARK_BLUE = "#17456b"
MUTED = "#6489aa"
LIGHT_BLUE = "#b9dcf7"
WHITE = "#ffffff"

# -------------------- SCROLLABLE WINDOW --------------------

main_container = tk.Frame(window, bg=BG)
main_container.pack(fill="both", expand=True)

canvas = tk.Canvas(
    main_container,
    bg=BG,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    main_container,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

content_frame = tk.Frame(canvas, bg=BG)

canvas_window = canvas.create_window(
    (0, 0),
    window=content_frame,
    anchor="nw"
)

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

def resize_content(event):
    canvas.itemconfig(canvas_window, width=event.width)

content_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_content)

# Mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# -------------------- VARIABLES --------------------

pizza_var = tk.StringVar(value="Diavola")
size_var = tk.StringVar(value="Small")
quantity_var = tk.StringVar(value="1")

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

# -------------------- STYLES --------------------

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Pizza.TCombobox",
    fieldbackground="#f7fbff",
    background="#f7fbff",
    foreground=DARK_BLUE,
    padding=7
)

style.map(
    "Pizza.TCombobox",
    fieldbackground=[("readonly", "#f7fbff")],
    foreground=[("readonly", DARK_BLUE)]
)

# -------------------- HELPER FUNCTION --------------------

def add_section_label(parent, text):
    tk.Label(
        parent,
        text=text,
        font=("Arial", 12, "bold"),
        bg=PANEL,
        fg=DARK_BLUE
    ).pack(anchor="w", pady=(12, 5))


# -------------------- CALCULATE TOTAL --------------------

def calculate_total():

    pizza = pizza_var.get()
    size = size_var.get()

    # Validate quantity
    try:
        quantity = int(quantity_var.get())

        if quantity < 1 or quantity > 50:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a whole number between 1 and 50."
        )
        return

    # Confirm order
    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    # Get prices
    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    # Get selected toppings
    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

    # Calculate total
    total_per_pizza = pizza_price + size_price + topping_price
    total = total_per_pizza * quantity

    # Display receipt
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)

    receipt_text.insert(tk.END, "              PIZZA ORDER RECEIPT\n")
    receipt_text.insert(tk.END, "=" * 48 + "\n")

    receipt_text.insert(
        tk.END,
        f"Date: {datetime.now().strftime('%B %d, %Y  %I:%M %p')}\n"
    )

    receipt_text.insert(tk.END, "-" * 48 + "\n")
    receipt_text.insert(tk.END, f"Pizza Flavor:       {pizza}\n")
    receipt_text.insert(tk.END, f"Pizza Size:         {size} (+P{size_price})\n")
    receipt_text.insert(tk.END, f"Base Pizza Price:   P{pizza_price:,.2f}\n")

    receipt_text.insert(tk.END, "\nEXTRA TOPPINGS\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"  {topping:<20} P{topping_prices[topping]:,.2f}\n"
            )
    else:
        receipt_text.insert(tk.END, "  No extra toppings\n")

    receipt_text.insert(tk.END, "-" * 48 + "\n")

    receipt_text.insert(
        tk.END,
        f"Price per Pizza:    P{total_per_pizza:,.2f}\n"
    )

    receipt_text.insert(tk.END, f"Quantity:           {quantity}\n")
    receipt_text.insert(tk.END, "=" * 48 + "\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT:       P{total:,.2f}\n")
    receipt_text.insert(tk.END, "=" * 48 + "\n")

    receipt_text.insert(
        tk.END,
        "       Thank you for ordering with us!\n"
    )

    receipt_text.config(state="disabled")

    # Automatically scroll to receipt
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)


# -------------------- RESET ORDER --------------------

def reset_order():

    pizza_var.set("Diavola")
    size_var.set("Small")
    quantity_var.set("1")

    for variable in topping_vars.values():
        variable.set(False)

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.config(state="disabled")

    canvas.yview_moveto(0)


# -------------------- TITLE --------------------

tk.Label(
    content_frame,
    text=" PIZZA ORDERING SYSTEM ",
    font=("Arial", 23, "bold"),
    bg=BG,
    fg=BLUE
).pack(pady=(20, 5))

tk.Label(
    content_frame,
    text="Build your pizza, choose your favorites, and place your order!",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
).pack(pady=(0, 15))


# -------------------- CUSTOMER MENU / PRICE LIST --------------------

menu_frame = tk.Frame(
    content_frame,
    bg=PANEL,
    padx=28,
    pady=20
)

menu_frame.pack(padx=30, fill="x", pady=(0, 12))

tk.Label(
    menu_frame,
    text="❄ MENU & PRICE LIST ❄",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=DARK_BLUE
).pack(pady=(0, 8))

tk.Label(
    menu_frame,
    text="PIZZA FLAVORS",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=DARK_BLUE
).pack(anchor="w")

for flavor, price in pizza_prices.items():

    tk.Label(
        menu_frame,
        text=f"• {flavor}  -  P{price:,.2f}",
        font=("Arial", 10),
        bg=PANEL,
        fg=DARK_BLUE
    ).pack(anchor="w")


# -------------------- ORDER FORM --------------------

order_frame = tk.Frame(
    content_frame,
    bg=PANEL,
    padx=28,
    pady=20
)

order_frame.pack(padx=30, fill="x")

# Pizza flavor
add_section_label(order_frame, "1. Select Pizza Flavor")

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Arial", 11),
    style="Pizza.TCombobox"
)

pizza_dropdown.pack(fill="x", pady=(0, 5))


# -------------------- PIZZA SIZE --------------------

add_section_label(order_frame, "2. Select Pizza Size")

for size, price in size_prices.items():

    tk.Radiobutton(
        order_frame,
        text=f"{size}  (+P{price})",
        variable=size_var,
        value=size,
        font=("Arial", 10),
        bg=PANEL,
        fg=DARK_BLUE,
        selectcolor=LIGHT_BLUE,
        activebackground=PANEL,
        activeforeground=DARK_BLUE,
        highlightthickness=0,
        cursor="hand2"
    ).pack(anchor="w")


# -------------------- EXTRA TOPPINGS --------------------

add_section_label(order_frame, "3. Add Extra Toppings")

for topping, price in topping_prices.items():

    tk.Checkbutton(
        order_frame,
        text=f"{topping}  (+P{price})",
        variable=topping_vars[topping],
        font=("Arial", 10),
        bg=PANEL,
        fg=DARK_BLUE,
        selectcolor=LIGHT_BLUE,
        activebackground=PANEL,
        activeforeground=DARK_BLUE,
        highlightthickness=0,
        cursor="hand2"
    ).pack(anchor="w")


# -------------------- QUANTITY --------------------

add_section_label(order_frame, "4. Quantity (1–50)")

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 11),
    width=10,
    bg="#f7fbff",
    fg=DARK_BLUE,
    buttonbackground=LIGHT_BLUE
)

quantity_spinbox.pack(anchor="w")


# -------------------- ACTION BUTTONS --------------------

button_frame = tk.Frame(content_frame, bg=BG)
button_frame.pack(pady=16)

place_order_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1d5f9e",
    activeforeground=WHITE,
    width=18,
    relief="flat",
    cursor="hand2",
    command=calculate_total
)

place_order_button.grid(row=0, column=0, padx=8, ipady=7)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg="#9bc9ed",
    fg=DARK_BLUE,
    activebackground="#83b8e3",
    activeforeground=DARK_BLUE,
    width=12,
    relief="flat",
    cursor="hand2",
    command=reset_order
)

reset_button.grid(row=0, column=1, padx=8, ipady=7)


# -------------------- ORDER RECEIPT --------------------

tk.Label(
    content_frame,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=BLUE
).pack(pady=(5, 7))

receipt_text = tk.Text(
    content_frame,
    height=14,
    width=65,
    font=("Consolas", 10),
    bg="#f7fbff",
    fg=DARK_BLUE,
    insertbackground=DARK_BLUE,
    relief="flat",
    padx=12,
    pady=10
)

receipt_text.pack(
    padx=30,
    pady=(0, 20),
    fill="both",
    expand=True
)

receipt_text.config(state="disabled")


# -------------------- START PROGRAM --------------------

window.mainloop()
