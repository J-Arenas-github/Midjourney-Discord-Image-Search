import time
import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor

# ---- Midjourney Image Search Backend Code ----
# Class created to make image metadata objects
class Image_metadata:
    def __init__(self, image_url, midjourney_url, timestamp, prompt_text):
        self.image_url = image_url
        self.midjourney_url = midjourney_url
        self.timestamp = timestamp
        self.prompt_text = prompt_text


# Set of discord channel ids to search
discord_channel_ids = [933565701162168371,
                       941971306004504638,
                       981832774157762570,
                       984632424610824222,
                       984632500875821066,
                       984632520471633920,
                       989274712590917653,
                       989274728155992124,
                       989274745495240734,
                       989274756341706822,
                       941582479117127680,
                       995431151084773486,
                       995431172375064616,
                       995431233121161246,
                       995431473828077618,
                       995431514080813086,
                       995431544019755070,
                       995431387333152778,
                       995431305066065950,
                       995431274267279440
                       ]

def image_search(token, keywords, max_messages, start_snowflake_timestamp, end_snowflake_timestamp):
    headers = {"authorization": f"{token}"}
    params = {
        "after": start_snowflake_timestamp,
        "before": end_snowflake_timestamp,
    }

    keywords = keywords.split(", ")  # Convert keywords to a list
    image_metadata_list = []  # List to store image metadata objects

    total_images_fetched = 0  # Total images fetched
    all_messages_fetched = 0  # All messages fetched
    error_code = 0  # Error code

    def retrieve_messages(url):
        nonlocal total_images_fetched, all_messages_fetched, error_code

        r = requests.get(url, headers=headers, params=params)
        pull_data = json.loads(r.text)

        # Check if the request was successful and if not, return an error code
        if r.status_code != 200:
            if r.status_code == 401:
                print("Unauthorized request. Please check your token.")
            elif r.status_code == 429:
                print("Rate limit exceeded. Please wait and try again later.")
            else:
                print("Request returned an error code: ", r.status_code)
            error_code = r.status_code
            no_images = []
            return no_images, error_code

        while all_messages_fetched < max_messages:
            if all_messages_fetched >= max_messages:

                break  # Stop the loop if we have reached the maximum number of messages

            for message in pull_data:
                print()
                content = message['content']
                if any(word in content for word in keywords):
                    matches = re.findall(r'\*\*(.*?)\*\*', content)
                    if matches:
                        attachment = message.get('attachments', [])
                        for item in attachment:
                            image_url = item['url']
                            if image_url is not None:
                                total_images_fetched += 1

                                timestamp = message['timestamp']
                                midjourney_url = None

                                components = message.get('components', [])
                                for component in components:
                                    midjourney_url = fetch_midjourney_url(component)


                                image_metadata = Image_metadata(image_url=image_url, midjourney_url=midjourney_url,
                                                                timestamp=timestamp, prompt_text=matches)
                                print(f'New Image metadata found:',
                                      f'Prompt: {matches} \n',
                                      f'Image URL: {image_url} \n',
                                      f'Midjourney URL: {midjourney_url} \n',
                                      f'Timestamp: {timestamp} \n')

                                image_metadata_list.append(image_metadata)
                all_messages_fetched += 1  # Counts messages requested
                print(f'Total messages fetched: {all_messages_fetched}')

            if 'before' in message and total_images_fetched < max_messages:
                url = f"https://discord.com/api/v9/channels/{message['channel_id']}/messages?before={message['id']}"
                retrieve_messages(url)
                # fetches more messages if there are more messages to fetch

    def fetch_midjourney_url(data):
        # Recursive function to fetch midjourney url, since it is nested and is not always in the same place
        if isinstance(data, dict):
            if 'url' in data:
                return data['url']
            for value in data.values():
                result = fetch_midjourney_url(value)
                if result:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = fetch_midjourney_url(item)
                if result:
                    return result
        return None

    def process_channel(channel_id):
        initial_url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        retrieve_messages(initial_url)

    with ThreadPoolExecutor() as executor:
        executor.map(process_channel, discord_channel_ids)

    return image_metadata_list, error_code
