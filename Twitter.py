import streamlit as st
import tweepy

twitter_api_key = "xxxxxxx"
twitter_api_secret = "xxxxxxxxx"
twitter_access_token = "xxxxxxxxxxxx"
twitter_access_secret = "xxxxxxxxxxx"

st.set_page_config(page_title="Tweet Poster", page_icon="🐦", layout="centered")

st.markdown("<h1 style='text-align: center;'>🐦 Post a Tweet via Streamlit</h1>", unsafe_allow_html=True)
st.write("Use the form below to publish a tweet using your Twitter account.")

with st.form("tweet_form"):
    tweet_content = st.text_area("📝 What's happening?", placeholder="Type your tweet here...", max_chars=280, height=150)
    submitted = st.form_submit_button("📤 Post Tweet")


if submitted:
    if not tweet_content.strip():
        st.warning("⚠️ Tweet content cannot be empty.")
    else:
        try:
            
            auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
            auth.set_access_token(twitter_access_token, twitter_access_secret)
            api = tweepy.API(auth)

            
            api.verify_credentials()
            api.update_status(tweet_content)
            st.success("✅ Your tweet has been posted successfully!")

        except tweepy.errors.TweepyException as e:
            st.error(f"❌ Twitter API error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")


st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Made with ❤️ using Streamlit & Tweepy</p>", unsafe_allow_html=True)
