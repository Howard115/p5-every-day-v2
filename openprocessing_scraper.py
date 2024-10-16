from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import shutil
import zipfile
import random


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode

    # Use webdriver_manager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action_chains = ActionChains(driver)
    
    return driver, action_chains

# Use the function to initialize the driver
driver, action_chains = initialize_driver()


def sign_in():
    # press tab for 7 times ,then press enter
    for _ in range(7):
        action_chains.send_keys(Keys.TAB).perform()
    action_chains.send_keys(Keys.ENTER).perform()
    # Wait for the sign-in link to be clickable
    sign_in_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/signin"]'))
    )
    sign_in_link.click()
    time.sleep(1)
    # Enter email
    action_chains.send_keys("anxgzmcrnld@gmail.com").perform()
    
    # Tab once
    action_chains.send_keys(Keys.TAB).perform()
    
    # Enter password
    action_chains.send_keys("0000000000").perform()
    
    # Tab three times
    for _ in range(3):
        action_chains.send_keys(Keys.TAB).perform()
    
    # Press Enter
    action_chains.send_keys(Keys.ENTER).perform()

    time.sleep(3)    




def download_random_sketch():
    # Wait for the sketch elements to be present
    sketch_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.sketchLi.col-xs-4.col-sm-3.col-lg-2"))
    )

    # Randomly choose one sketch element
    if sketch_elements:
        random_sketch = random.choice(sketch_elements)
        random_sketch.click()
    else:
        print("No sketch elements found")
        return

    # Wait for the share button to be clickable
    share_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.icon.icon_share.white"))
    )
    # Click the share button
    share_button.click()

    # Wait for the download link to be clickable
    download_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#downloadLink'))
    )
    # Click the download link
    download_link.click()
    
    # Wait for the file to be downloaded
    wait_for_download()

def wait_for_download():
    download_dir = os.path.expanduser("~/Downloads")
    timeout = 60  # Maximum wait time in seconds
    interval = 1  # Check interval in seconds
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        zip_files = [f for f in os.listdir(download_dir) if f.endswith('.zip')]
        if zip_files:
            latest_zip = max([os.path.join(download_dir, f) for f in zip_files], key=os.path.getmtime)
            if "sketch" in os.path.basename(latest_zip).lower():
                # Wait a bit more to ensure the download is complete
                time.sleep(2)
                return
        time.sleep(interval)
    
    raise TimeoutError("Download timeout: No sketch zip file found within the specified time.")

def process_downloaded_zip():
    # Clear all folders in downloadFOLDER
    download_folder = os.path.join(os.path.dirname(__file__), "downloadFOLDER")
    if os.path.exists(download_folder):
        for item in os.listdir(download_folder):
            item_path = os.path.join(download_folder, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed folder: {item_path}")

    # Get the default download directory
    download_dir = os.path.expanduser("~/Downloads")

    # Find the most recently downloaded zip file
    zip_files = [f for f in os.listdir(download_dir) if f.endswith('.zip')]
    if zip_files:
        latest_zip = max([os.path.join(download_dir, f) for f in zip_files], key=os.path.getmtime)
        # Check if the zip file name contains "sketch"
        if "sketch" not in os.path.basename(latest_zip).lower():
            raise ValueError("Can't find sketchzip")
        
        # Extract the sketch ID from the zip file name
        sketch_folder_name = os.path.splitext(os.path.basename(latest_zip))[0]
        sketch_id = sketch_folder_name.split('sketch')[-1]
        
        # Create downloadZIP folder if it doesn't exist
        download_zip_dir = os.path.join(os.path.dirname(__file__), "downloadZIP")
        os.makedirs(download_zip_dir, exist_ok=True)
        
        # Move the zip file to downloadZIP folder
        destination = os.path.join(download_zip_dir, os.path.basename(latest_zip))
        shutil.move(latest_zip, destination)
        print(f"Moved {latest_zip} to {destination}")

        # Create downloadFOLDER if it doesn't exist
        download_folder = os.path.join(os.path.dirname(__file__), "downloadFOLDER")
        os.makedirs(download_folder, exist_ok=True)

        # Create the sketch-specific folder inside downloadFOLDER
        sketch_folder = os.path.join(download_folder, 'sketch')
        os.makedirs(sketch_folder, exist_ok=True)

        # Extract the contents of the zip file to the sketch-specific folder
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(sketch_folder)

        print(f"Extracted contents of {os.path.basename(destination)} to {sketch_folder}")

        # Remove the original zip file after extraction
        os.remove(destination)
        print(f"Removed original zip file: {destination}")
        
        return sketch_id  # Return the sketch ID
    else:
        print("No zip file found in the download directory")
        return None

# Navigate to the OpenProcessing trending page
driver.get("https://openprocessing.org/discover/#/trending")

sign_in()

driver.get("https://openprocessing.org/discover/#/trending")

download_random_sketch()
sketch_id = process_downloaded_zip()
if sketch_id:
    print(f"Processed sketch: {sketch_id}")
else:
    print("Failed to process sketch")

driver.quit()

