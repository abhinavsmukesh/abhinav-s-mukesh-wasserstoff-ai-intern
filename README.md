# LinkedIn Profile Scraper

This script is a Python-based LinkedIn profile scraper that uses Selenium WebDriver to automate the process of logging into LinkedIn, navigating to the "My Network" page, and scraping up to 200 profile names and URLs. The scraped data is saved in a JSON file.

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (compatible with your Chrome browser version)
- Selenium package

## Installation

1. **Install the required Python packages:**

    ```bash
    pip install selenium
    ```

2. **Download and install ChromeDriver:**

## Usage

1. **Update the script with your LinkedIn credentials:**

    Replace the `USERNAME` and `PASSWORD` variables in the script with your LinkedIn login credentials.

    ```python
    USERNAME = "your-email@example.com"
    PASSWORD = "your-password"
    ```

2. **Run the script:**

    Execute the script using Python.

    ```bash
    python linkedin_scraper.py
    ```

    The script will:
    - Open a headless Chrome browser.
    - Log in to LinkedIn using the provided credentials.
    - Navigate to the "My Network" page.
    - Click the "Show All" button.
    - Scrape up to 200 profiles (names and URLs).
    - Save the scraped profiles to a JSON file (`profiles.json`).

## Script Details

- **Setup:**

    The script sets up Selenium WebDriver using ChromeDriver in headless mode to avoid opening a visible browser window.

    ```python
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
    ```

- **Login:**

    The script logs into LinkedIn using the provided credentials.

    ```python
    driver.get("https://linkedin.com/uas/login")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(USERNAME)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(PASSWORD)
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    sign_in_btn.click()
    driver.maximize_window()
    ```

- **Navigate and Scrape:**

    The script navigates to the "My Network" page and scrapes profile names and URLs. It handles clicking the "Load More" button to load additional profiles.

    ```python
    while scraped_profiles < 200:
        profile_links = driver.find_elements(By.XPATH, '//a[contains(@href, "linkedin.com/in/")]')
        for link in profile_links:
            if scraped_profiles >= 200:
                break
            profile_url = link.get_attribute("href")
            try:
                profile_name = link.find_element(By.XPATH, './div/div/p[1]').text
            except:
                profile_name = "Unknown"
            if profile_url not in [profile['url'] for profile in profiles]:
                profiles.append({'name': profile_name, 'url': profile_url})
                scraped_profiles += 1
                print(f"Scraped: {profile_name} - {profile_url}")

        load_more_button_xpath = "//span[contains(text(), 'Load more')]"
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, load_more_button_xpath))
            )
            load_more_button.click()
            time.sleep(3)
            print("Clicked Load More")
        except StaleElementReferenceException:
            print("StaleElementReferenceException: Reloading Load More button...")
            time.sleep(2)
        except Exception as e:
            print("Error clicking 'Load More':", e)
            break
    ```

- **Save Data:**

    The scraped profiles are saved to a JSON file.

    ```python
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)
    ```

- **Close Browser:**

    The browser is closed after scraping.

    ```python
    driver.quit()
    ```

## Benefits

- **Automation:** Automates the tedious process of manually browsing and collecting LinkedIn profiles, saving time and effort.
- **Headless Operation:** Uses a headless Chrome browser, allowing the script to run without opening a visible browser window, making it ideal for running in the background or on servers.
- **Scalability:** Capable of scraping up to 200 profiles in one run, making it suitable for small to medium-scale data collection tasks.
- **Customizable:** The script can be easily modified to include additional data points or to change the scraping logic as per the user's requirements.
- **JSON Output:** Saves the scraped profiles in a JSON file, which is a widely used format for data interchange and can be easily processed or imported into other applications.

## Notes

- **Update XPath/HTML:** LinkedIn's web structure may change over time, causing the XPath or CSS selectors used in this script to become outdated. If the script fails to find elements, you may need to update the XPath/HTML selectors. The areas to update include:
    - `show_all_button` selector:
        ```python
        show_all_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/main/div/div/main/div/div[1]/div/div[2]/section/div/div[1]/div/button'))
        )
        ```
    - `profile_links` selector:
        ```python
        profile_links = driver.find_elements(By.XPATH, '//a[contains(@href, "linkedin.com/in/")]')
        ```
    - `load_more_button_xpath` selector:
        ```python
        load_more_button_xpath = "//span[contains(text(), 'Load more')]"
        ```

    Update these selectors by inspecting the current LinkedIn web elements using browser developer tools.
