import streamlit as st
import requests
import os

print("CWD:", os.getcwd())
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "../Untitled_Artwork.png")

st.set_page_config(page_title="Voucher Details", page_icon="🧾")

voucher = st.session_state.get("voucher")

if not voucher:
    st.warning("No voucher loaded.")
    st.switch_page("app.py")

st.title("Voucher Details")
st.logo(IMAGE_PATH)
# st.metric("Voucher Code: ", voucher["voucherCode"])
col1, col2 = st.columns(2)
with col1:
    st.write("Voucher Code: ")
    st.badge(voucher["voucherCode"], icon=":material/check:")
with col2:
    st.write("Status: ")
    st.badge(voucher["status"], icon=":material/check:", color="green")
(
    col1,
    col2,
) = st.columns(2)

st.write("Email: ", voucher["distEmailAddress"])
with col1:
    st.write("Value Remaining: ", f"${float(voucher['valueRemaining']):.2f}")

program = voucher.get("program", {})

st.subheader("Program")
st.write("Name:", program.get("name"))
st.write("Subsidy Type:", program.get("subsidyType"))
st.write("Discount Amount:", f"${float(program.get('discountAmount')):.2f}")

st.divider()


# -------------------------
# Eligible Products
# -------------------------

st.subheader("Shop Eligible Products:")

DUMMY_PRODUCTS = [
    {"id": "sku-1", "name": "Work Gloves", "price": 19.99},
    {"id": "sku-2", "name": "Safety Helmet", "price": 49.99},
    {"id": "sku-3", "name": "Boots", "price": 129.99},
]

# Init cart
if "cart" not in st.session_state:
    st.session_state["cart"] = {}

for product in DUMMY_PRODUCTS:
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.write(f"**{product['name']}**")
        st.caption(f"${product['price']:.2f}")

    with col2:
        qty = st.session_state["cart"].get(product["id"], {}).get("qty", 0)
        st.write(f"Qty: {qty}")

    with col3:
        if st.button("Add", key=f"add-{product['id']}"):
            st.session_state["cart"][product["id"]] = {
                "product": product,
                "qty": qty + 1,
            }


st.divider()
st.subheader("Cart")

cart = st.session_state["cart"]

if not cart:
    st.info("Cart is empty")
else:
    total = 0

    for item in cart.values():
        product = item["product"]
        qty = item["qty"]
        line_total = product["price"] * qty
        total += line_total

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(product["name"])
        with col2:
            st.write(f"x{qty}")
        with col3:
            st.write(f"${line_total:.2f}")

    st.divider()
    st.write(f"**Subtotal:** ${total:.2f}")

st.divider()
st.subheader("Payment / Shipping")

number = st.number_input("Enter Subsidy Amount")
print("🤡 number:", number)
if st.button("Redeem", type="primary"):
    with st.spinner("Redeeming voucher..."):
        try:
            response = requests.post(
                "https://bipedal-whistlingly-kaycee.ngrok-free.dev/api/ext/redeem-voucher/redeem",
                timeout=15,
                json={"amount": number},
            )
            # add number tto the request body

            response.raise_for_status()
            data = response.json() if response.content else {}
            print("🤡 data from redeem:", data)
            payment_url = data["data"]["paymentURL"]
            st.write("🥝🥝🥝🥝🥝 Payment Link:", payment_url)

            # payment = data.data["payment"]
            # print("🤡 payment:", payment)
            st.success("Voucher redeemed successfully.")
            if data:
                st.json(data)
                print("🤡 data from redeem:", data)
                # st.write("Payment Link: ", data["paymentURL"])
        except requests.exceptions.HTTPError:
            st.error(
                f"Redeem failed with status {response.status_code}: {response.text}"
            )
        except requests.exceptions.RequestException as exc:
            st.error(f"Network error: {exc}")


with st.form("my_form"):
    st.write("Shipping Info")

    addressInput = st.text_input("Address")
    col1, col2, col3 = st.columns(3)
    with col1:
        cityInput = st.text_input("City")
    with col2:
        stateInput = st.text_input("State")
    with col3:
        zipInput = st.text_input("Zip")
    countryInput = st.text_input("Country")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("City: ", cityInput)
        st.write("State: ", stateInput)
        st.write("Zip: ", zipInput)
        st.write("Country: ", countryInput)

if st.button("Back", type="primary"):
    st.switch_page("app.py")
