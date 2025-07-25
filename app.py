import streamlit as st

# Set page config
st.set_page_config(page_title="Lead Capture Demo", page_icon="📋", layout="centered")

# Welcome section
st.title("Welcome to the Lead Capture Demo")
st.write("""
This demo showcases how a Zoho Webform can be embedded inside a Streamlit app.
You can use this page to simulate how leads can be collected from external websites or landing pages.
""")

# Embed the Zoho form
st.subheader("Embedded Zoho Lead Form")
st.components.v1.html(
    '<iframe src="https://mahin200405.github.io/zoho-webform/" width="100%" height="700" style="border:none;"></iframe>',
    height=720,
)
