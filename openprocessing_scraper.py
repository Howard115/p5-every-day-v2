from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
driver = webdriver.Chrome(options=chrome_options)
action_chains = ActionChains(driver)


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




def download_first_sketch():
    # Wait for the sketch elements to be present
    sketch_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.sketchLi.col-xs-4.col-sm-3.col-lg-2"))
    )

    # Click the first sketch element
    if sketch_elements:
        first_sketch = sketch_elements[0]
        first_sketch.click()
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



def process_downloaded_zip(sketch_folder_name):
    import os
    import shutil
    import zipfile

    # Get the default download directory
    download_dir = os.path.expanduser("~/Downloads")

    # Find the most recently downloaded zip file
    zip_files = [f for f in os.listdir(download_dir) if f.endswith('.zip')]
    if zip_files:
        latest_zip = max([os.path.join(download_dir, f) for f in zip_files], key=os.path.getmtime)
        # Check if the zip file name contains "sketch"
        if "sketch" not in os.path.basename(latest_zip).lower():
            raise ValueError("Can't find sketchzip")
        
        # Create downloadZIP folder if it doesn't exist
        download_zip_dir = os.path.join(os.getcwd(), "downloadZIP")
        os.makedirs(download_zip_dir, exist_ok=True)
        
        # Move the zip file to downloadZIP folder
        destination = os.path.join(download_zip_dir, os.path.basename(latest_zip))
        shutil.move(latest_zip, destination)
        print(f"Moved {latest_zip} to {destination}")

        # Create downloadFOLDER if it doesn't exist
        download_folder = os.path.join(os.getcwd(), "downloadFOLDER")
        os.makedirs(download_folder, exist_ok=True)

        # Create the sketch-specific folder inside downloadFOLDER
        sketch_folder = os.path.join(download_folder, sketch_folder_name)
        os.makedirs(sketch_folder, exist_ok=True)

        # Extract the contents of the zip file to the sketch-specific folder
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(sketch_folder)

        print(f"Extracted contents of {os.path.basename(destination)} to {sketch_folder}")

        # Remove the original zip file after extraction
        os.remove(destination)
        print(f"Removed original zip file: {destination}")
    else:
        print("No zip file found in the download directory")

# Navigate to the OpenProcessing trending page
driver.get("https://openprocessing.org/discover/#/trending")

sign_in()

driver.get("https://openprocessing.org/discover/#/trending")

download_first_sketch()
time.sleep(1)
process_downloaded_zip("sketch_001")

driver.quit()


