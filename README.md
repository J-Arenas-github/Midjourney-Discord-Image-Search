# Midjourney Search Website


## Project Overview:
The Midjourney Image Search website allows users to search for images on the Midjourney public Discord server.
The website prompts users to input their Discord token, keywords, date range, and the number of images they want to request. 
After submitting the search query, the website displays the retrieved images.
The user can change the number of images per column, and their associated prompts with (if any) Midjourney links in a grid format.


### How to Run

To run the website, ensure you have Python installed on your system.
Open a terminal or command prompt, and run the following command: 
```bash
streamlit run  "C:\path\to\file\Final Project V7.py"
```


### Dependencies Needed
- Python 3.x 
- streamlit 
- time
- datetime
- requests
- json
- re
- concurrent.futures


## Interacting with the Website:
### Here's how users can interact with the website:

### Search Form
- Users are prompted to enter the following information in the search form:
  - **Discord Token:** Users need to input their Discord account token. A guide on obtaining the token is provided with a link to a tutorial video.
  - **Keywords:** Users can enter 1-10 keywords separated by commas to search for relevant images.
  - **Images per Search:** Users can specify the number of images they want to retrieve per search, ranging from 10 to 10,000. A recommended range of 150-5500 images is suggested for optimal performance.
  - **Date Range:** Users can select a date range to narrow down the search results. A default range of the past week is recommended due to the large number of images.
- After entering the required information, users can click the "Search" button to initiate the image search request.

### Image Display
- Once the search is initiated, the website retrieves image metadata based on the user's input parameters.
- The retrieved images are displayed in a grid format, with the option to adjust the number of columns for better viewing.
- Users can choose to display prompts and Midjourney links associated with each image by toggling a checkbox.

### Error Handling
- The website provides error messages to users in case of any issues, such as unauthorized access or rate limiting.
- Clear instructions are provided to guide users on resolving common issues and pop-ups will be displayed if there are issues.


## Backend Code Explanation:
### The backend code (located in the `Midjourney_Images_Metadata.py` file) is responsible for handling the image search functionality. Here's an overview of how it works:

### Image Metadata Class
- The `Image_metadata` class is used to create image metadata objects containing information such as image URL, Midjourney URL, timestamp, and prompt text.

### Image Search Function
- The `image_search` function retrieves image metadata from the Midjourney Discord server based on the provided parameters, including the Discord token, keywords, date range, and maximum number of messages to request.
- It uses multithreading with ThreadPoolExecutor to process messages from multiple channels, improving efficiency but more importantly speed.
- The `retrieve_messages` function retrieves messages from a given Discord channel URL, filters them based on the provided keywords, and extracts relevant image metadata.
- The `fetch_midjourney_url` function is a recursive helper function to extract the Midjourney URL from nested message components. Since the url is not always in the same place.
- The `process_channel` function initiates the message retrieval process for each Discord channel.
