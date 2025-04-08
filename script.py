import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

# Set up the Selenium WebDriver using ChromeDriver in headless mode
options = Options()
options.add_argument("--disable-gpu")
# options.add_argument("--headless")  # Comment out for debugging
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)

# Log in to LinkedIn
driver.get("https://linkedin.com/uas/login")
USERNAME = "typehere"
PASSWORD = "typehere"
username_field = driver.find_element(By.ID, "username")
username_field.send_keys(USERNAME)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(PASSWORD)
sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
sign_in_btn.click()
driver.maximize_window()

# Navigate to the My Network page
driver.get("https://www.linkedin.com/mynetwork/")

# Wait until the "Show All" button is clickable and click it using JS if needed
retry_count = 3
while retry_count > 0:
    try:
        # Wait for the Show All button to become visible
        show_all_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Show all')]"))
        )
        driver.execute_script("arguments[0].click();", show_all_button)
        print("Show All button clicked successfully")
        break  # Exit loop if successful
    except StaleElementReferenceException:
        print("StaleElementReferenceException: Retrying...")
        retry_count -= 1
        time.sleep(2)  # Wait before retrying
    except Exception as e:
        print("Error clicking 'Show All':", e)
        break

# List to store profile names and URLs
profiles = []
scraped_profiles = 0

# Loop to scrape profiles until 200 profiles are scraped
while scraped_profiles < 200:
    # Locate all <a> tags that contain the profile links
    profile_links = driver.find_elements(By.XPATH, '//a[contains(@href, "linkedin.com/in/")]')

    # Iterate through each profile link
    for link in profile_links:
        if scraped_profiles >= 200:  # Stop if 200 profiles are scraped
            break
        profile_url = link.get_attribute("href")
        try:
            profile_name = link.find_element(By.XPATH, './div/div/p[1]').text
        except:
            profile_name = "Unknown"
        
        # Avoid duplicates by checking the profile URL
        if profile_url not in [profile['url'] for profile in profiles]:
            profiles.append({'name': profile_name, 'url': profile_url})
            scraped_profiles += 1
            print(f"Scraped: {profile_name} - {profile_url}")

    # Try to click the "Load More" button and handle stale element references
    load_more_button_xpath = "//span[contains(text(), 'Load more')]"
    retry_count = 3
    while retry_count > 0:
        try:
            # Scroll the page to make sure the button is in view
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Allow the page to load new content

            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, load_more_button_xpath))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Clicked Load More")
            break  # Exit loop if successful
        except StaleElementReferenceException:
            print("StaleElementReferenceException: Retrying...")
            retry_count -= 1
            time.sleep(2)  # Wait before retrying
        except Exception as e:
            print("Error clicking 'Load More':", e)
            break

# Save the scraped profiles to a JSON file
with open("profiles.json", "w") as file:
    json.dump(profiles, file, indent=4)

print("Profiles have been saved to profiles.json")

# Close the browser after scraping
driver.quit()
