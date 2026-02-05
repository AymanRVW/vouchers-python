# source .venv/bin/activate
# streamlit run app.py
# pip install -r requirements.txt

import streamlit as st
import requests
import os
print("CWD:", os.getcwd())
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Untitled_Artwork.png")
# IMAGE_PATH = os.path.join(os.path.dirname(__file__), "ww-logo-shoeteria.png")


st.set_page_config(page_title="VoucherPOC", page_icon="🧾", layout="centered")

st.title("Online Voucher Redemption")
st.caption("Quick Streamlit UI scaffold")
st.logo(IMAGE_PATH)
# st.image(IMAGE_PATH, width=120)

st.write("Hello! App running in a virtual environment.")

st.subheader("Redeem Voucher")

voucher_code = st.text_input("Voucher Code", placeholder="Enter voucher code")
if st.button("Submit", type="primary"):
    with st.spinner("Checking voucher..."):
        try:
            print(f"Checking voucher: {voucher_code}")
            response = requests.get(
                f"https://bipedal-whistlingly-kaycee.ngrok-free.dev/api/ext/voucher-lookup/{voucher_code}",
                params={"shopDomain": "ayman-teststore-plus-2.myshopify.com"},
                timeout=15,
            )
            print('🤡 response:', response.json())
            response.raise_for_status()
            data = response.json() 
            print('🤡 data:', data)
            voucher = data["data"]

            st.session_state["voucher"] = voucher
            st.session_state["voucher_code"] = voucher_code

            st.switch_page("pages/voucher_details.py")


            print("First name:", voucher["firstName"])
            print("Voucher code:", voucher["voucherCode"])
            st.write(f"First name: {voucher['firstName']}")
            st.write(f"Voucher code: {voucher['voucherCode']}")
            st.write(f"Status: {voucher['status']}")
            st.write(f"Value remaining: {voucher['valueRemaining']}")
        except requests.exceptions.HTTPError:
            st.error(
                f"Check voucher failed with status {response.status_code}: {response.text}"
            )
        except requests.exceptions.RequestException as exc:
            st.error(f"Network error: {exc}")


# if st.button("Redeem"):
#     with st.spinner("Redeeming voucher..."):
#         try:
#             response = requests.post(
#                 "https://bipedal-whistlingly-kaycee.ngrok-free.dev/api/ext/redeem-voucher/redeem",
#                 timeout=15,
#             )
#             response.raise_for_status()
#             data = response.json() if response.content else {}
#             st.success("Voucher redeemed successfully.")
#             if data:
#                 st.json(data)
#         except requests.exceptions.HTTPError:
#             st.error(
#                 f"Redeem failed with status {response.status_code}: {response.text}"
#             )
#         except requests.exceptions.RequestException as exc:
#             st.error(f"Network error: {exc}")
