import streamlit as st
import random

# --- Initialize session state ---
if 'step' not in st.session_state:
    st.session_state['step'] = 1

if 'cart' not in st.session_state:
    st.session_state['cart'] = {'Tomato': 0, 'Onion': 0, 'Potato': 0}

# --- Customer Form Submission ---
def submit_customer_info():
    if name and address and contact:
        st.session_state['customer_info'] = {'name': name, 'address': address, 'contact': contact}
        st.success("Customer information submitted successfully!")
        st.session_state['step'] = 2
    else:
        st.error("Please fill in all fields to proceed.")

# --- Product Update Functions ---
def add_product(product_name):
    st.session_state['cart'][product_name] += 1

def remove_product(product_name):
    if st.session_state['cart'][product_name] > 0:
        st.session_state['cart'][product_name] -= 1

# --- Generate Order ID ---
def generate_order_id():
    return f"SW{random.randint(1000,9999)}"

# --- App Layout ---
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to Sabziwala</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: green;'>Now Serving Lahore</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: red;'>We Bring Excellence in Quality Produce</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Step 1: Customer Information ---
if st.session_state['step'] == 1:
    st.header("🧑‍💼 Customer Information")

    with st.form("customer_form"):
        name = st.text_input("Name")
        address = st.text_input("Address")
        contact = st.text_input("Contact Number (e.g., 03001234567)")

        submit_button = st.form_submit_button("Proceed to Products")

        if submit_button:
            submit_customer_info()

# --- Step 2: Product Selection ---
elif st.session_state['step'] == 2:
    st.header("🛒 Available Products")

    products = [
        {"name": "Tomato", "price": 80, "image": "https://upload.wikimedia.org/wikipedia/commons/8/89/Tomato_je.jpg"},
        {"name": "Onion", "price": 60, "image": "https://upload.wikimedia.org/wikipedia/commons/7/74/Onions.jpg"},
        {"name": "Potato", "price": 60, "image": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Patates.jpg"}
    ]

    cols = st.columns(len(products))

    for idx, product in enumerate(products):
        with cols[idx]:
            with st.container(border=True):
                st.image(product["image"], width=150)
                st.markdown(f"<h4 style='text-align: center;'>{product['name']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>Rs. {product['price']} / Kg</p>", unsafe_allow_html=True)

                qty_cols = st.columns([1, 2, 1])

                with qty_cols[0]:
                    if st.button("➖", key=f"{product['name']}_minus"):
                        remove_product(product['name'])

                with qty_cols[1]:
                    st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold;'>{st.session_state['cart'][product['name']]}</div>", unsafe_allow_html=True)

                with qty_cols[2]:
                    if st.button("➕", key=f"{product['name']}_plus"):
                        add_product(product['name'])

    st.markdown("---")
    if st.button("Proceed to Order Summary"):
        st.session_state['step'] = 3

# --- Step 3: Cart Summary and Order Placement ---
elif st.session_state['step'] == 3:
    st.header("📋 Order Summary")

    total_amount = 0
    ordered_items = []

    for product_name, qty in st.session_state['cart'].items():
        if qty > 0:
            if product_name == 'Tomato':
                price = 80
            elif product_name == 'Onion':
                price = 60
            elif product_name == 'Potato':
                price = 60

            amount = qty * price
            total_amount += amount
            ordered_items.append(f"{product_name} ({qty} Kg) - Rs. {amount}")

    if ordered_items:
        for item in ordered_items:
            st.write(f"- {item}")
        st.write(f"### Total Amount Payable: Rs. {total_amount}")

        st.markdown("---")
        st.subheader("Select Payment Method")
        payment_method = st.radio("Payment Options", ["Cash on Delivery", "Bank Transfer", "Online Payment"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Return to Cart"):
                st.session_state['step'] = 2

        with col2:
            if st.button("✅ Place Order"):
                order_id = generate_order_id()

                st.success(f"🎉 Order Placed Successfully! Your Order ID: {order_id}")
                st.balloons()

                # Prepare WhatsApp message
                message = f"*Welcome to Sabziwala!*%0A%0A"
                message += f"🛒 *Order ID*: {order_id}%0A"
                message += f"👤 *Customer*: {st.session_state['customer_info']['name']}%0A"
                message += f"📍 *Address*: {st.session_state['customer_info']['address']}%0A"
                message += f"📞 *Contact*: {st.session_state['customer_info']['contact']}%0A%0A"
                message += "🧾 *Order Summary*:%0A"

                for item in ordered_items:
                    message += f"- {item}%0A"

                message += f"%0A💵 *Total Amount*: Rs. {total_amount}%0A"
                message += f"💳 *Payment Method*: {payment_method}%0A%0A"
                message += "🙏 *Thank you for choosing Sabziwala!*"

                # WhatsApp Link
                whatsapp_url = f"https://wa.me/923034123570?text={message}"

                st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='background-color:green; color:white; padding:10px; border:none; border-radius:5px;'>📩 Send Order via WhatsApp</button></a>", unsafe_allow_html=True)

    else:
        st.warning("No products added to the cart.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: grey;'>For Queries or Help, Contact: <b>0303-4123570</b> (WhatsApp Available)</p>",
    unsafe_allow_html=True
)
