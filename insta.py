import streamlit as st


st.set_page_config(page_title="Instagram Messenger", layout="centered")

page_bg_img = """
<style>
body {
background-image: url("https://images.unsplash.com/photo-1549921296-3a4b61d8fc58");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}

.stApp {
background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent overlay */
padding: 2rem;
border-radius: 12px;
}

h1, h2, h3, .stTextInput, .stTextArea, .stButton {
color: white !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


st.header("📩 Send Instagram Message")



instagram_username = st.text_input("Recipient Instagram Username")
instagram_message = st.text_area("Instagram Message")

if st.button("Send Instagram Message"):
    st.info("This is a placeholder. Real Instagram integration requires API permissions.")
