import streamlit as st
import time
import Midjourney_Images_Metadata as imag_retriever
import datetime as dt



# ---- HEADER SECTION ----
st.set_page_config(page_title="Midjourney Image Search", layout="wide")

with st.container():
    st.subheader("Final Project V7 - Jesus Arenas")
    st.title("Midjourney Image Search")

st.write(
    """
    This website is designed to help you search for images on the Midjourney public discord server. This is how it works:
    - You will need to access your Discord account token. [Learn How To Get Your Discord Token](https://youtu.be/LnBnm_tZlyU?si=OckIHtXnKMQY4-Hw)
    - Note that your discord token is highly sensitive and is not saved to the website. 
    It will be deleted once you close the tab. However, use a burner account if you have one and/or reset your password once you're done searching
    - Enter your discord token, keywords, images per search, date range, and click search
    - Once you click search, the website will search for images with the keywords in their prompt and display them in a grid
    """)
st.markdown("---")


# ---- SEARCH FORM ----
with st.form("Search Info"):
    st.write("Enter your Discord token: ")
    token_input = st.text_input("Do NOT include the quotation marks", type="password")
    st.write("")

    st.write("Enter 1-10 keywords for images you want to search for, separated by commas: ")
    keywords_input = st.text_input("Example: house, european style, sunset, city")
    st.write("")

    st.write("Enter the number of images you want per search: ")
    images_per_search = st.number_input("Up to 10,000 images per search. Between 150-5500 is recommended, more images will take longer. ",
                                        min_value=10,
                                        max_value=10000,
                                        value=150)

    st.write("Enter the date range you want to search for: ")
    time_range = st.date_input("Due to the large amount of images, a 1 week date range is recommended.",
                               value=(dt.date.today() - dt.timedelta(days=7), dt.date.today()),
                               min_value=dt.date(2022, 2, 1),
                               max_value= dt.date.today(),
                               format="MM-DD-YYYY",
                               )

    submitted = st.form_submit_button("Search")


# ---- SESSION STATE, Keeps states between pages ----
if 'image_metadata_list' not in st.session_state:
    st.session_state.image_metadata_list = []
if 'num_columns' not in st.session_state:
    st.session_state.num_columns = 4


# ---- Display Images & Timestamps Conversion -----
def display_images():
    st.write("## Images")

    num_columns_widget = st.number_input("Number of columns", min_value=1, max_value=7, value=st.session_state.num_columns, key="num_columns_widget")
    show_captions = st.checkbox("Show prompts and Midjourney links", value=False)

    st.write(f'Total images found: {len(st.session_state.image_metadata_list)}')
    st.markdown("---")

    for row_start_index in range(0, len(st.session_state.image_metadata_list), num_columns_widget):
        cols = st.columns(num_columns_widget)
        time.sleep(.5)
        for col_index in range(num_columns_widget):
            image_index = row_start_index + col_index
            if image_index < len(st.session_state.image_metadata_list):
                with cols[col_index]:
                    st.image(st.session_state.image_metadata_list[image_index].image_url, use_column_width=True)
                    if show_captions:
                        if st.session_state.image_metadata_list[image_index].midjourney_url:
                            prompt_text = ', '.join(st.session_state.image_metadata_list[image_index].prompt_text)
                            st.markdown(f"[{prompt_text}]({st.session_state.image_metadata_list[image_index].midjourney_url})")
                        else:
                            prompt_text = ', '.join(st.session_state.image_metadata_list[image_index].prompt_text)
                            st.caption(prompt_text)


def timestamp_to_snowflake(timestamps):
    start_timestamp = dt.datetime.combine(timestamps[0], dt.time.min)
    end_timestamp = dt.datetime.combine(timestamps[1], dt.time.max)

    # Convert the start and end dates to snowflake timestamps
    start_snowflake_timestamp = (int(start_timestamp.timestamp() * 1000) - 1420070400000) << 22
    end_snowflake_timestamp = (int(end_timestamp.timestamp() * 1000) - 1420070400000) << 22
    # 1420070400000 must be subtracted to the snowflake and the timestamp must be shifted by 22 bits to match the snowflake format
    # see https://discord.com/developers/docs/reference#snowflakes for more details

    return start_snowflake_timestamp, end_snowflake_timestamp


# ---- Search Request ----
if submitted:
    token = token_input
    keywords = keywords_input

    # Check if token or keywords are empty
    if not token or not keywords:
        st.warning("Please enter both your Discord token and keywords before submitting.")
    else:
        image_metadata_list = []
        images_per_search = images_per_search
        max_messages = images_per_search
        timestamps = time_range

        # All backend code is in Midjourney_Images_Metadata.py
        start_snowflake_timestamp, end_snowflake_timestamp = timestamp_to_snowflake(timestamps)
        image_metadata_list, error_code = imag_retriever.image_search(token, keywords, max_messages, start_snowflake_timestamp, end_snowflake_timestamp)

        if error_code != 0:
            if error_code == 401:
                st.warning("Unauthorized request. Please check your token and try again.")
            elif error_code == 429:
                st.warning("Rate limit exceeded. Please wait and try again later.")
            else:
                st.warning("Request returned an error code: ", error_code)
        else:
            st.session_state.image_metadata_list = image_metadata_list
            display_images()
else:
    display_images()