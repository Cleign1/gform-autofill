import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# IMPORTANT:
# For Windows, the filename is likely 'geckodriver.exe'
# For macOS or Linux, it's likely just 'geckodriver'
GECKODRIVER_PATH = './geckodriver.exe' # <-- CHANGE TO './geckodriver' if on macOS/Linux

def fill_questionnaire_form():
    """Initializes the Firefox driver, fills the form with a neutral-to-slightly-positive bias, and submits it."""

    # --- ✨ New: Weights adjusted for a more subtle positive bias ---
    # The highest probabilities are now on '3' (Neutral) and '4' (Agree).
    # '5' (Strongly Agree) is now less likely, to avoid an obvious positive bias.
    answer_weights = [5, 13, 35, 40, 15]  # [Rating 1, Rating 2, Rating 3, Rating 4, Rating 5]

    try:
        service = FirefoxService(executable_path=GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service)
        
        url = "https://docs.google.com/forms/d/e/1FAIpQLSeJPwYStsJRrA3mpSw_mvyPFQOWqdZbP_eDkcWH4nRvLAfkRg/viewform"
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='radiogroup']")))

        question_blocks = driver.find_elements(By.XPATH, "//div[contains(@class, 'Qr7Oae') and .//div[@role='radiogroup']]")
        print(f"Found {len(question_blocks)} questions to answer.")

        for i, block in enumerate(question_blocks):
            choices = block.find_elements(By.XPATH, ".//label[contains(@class, 'T5pZmf')]")
            
            if choices and len(choices) == 5: # Ensure it's a 5-point scale question
                # Use the new weighted random selection
                random_choice = random.choices(choices, weights=answer_weights, k=1)[0]
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_choice)
                time.sleep(0.2)
                
                random_choice.click()
                print(f"  - Answered Question {i+1} with a neutral/slightly positive rating: {choices.index(random_choice) + 1}")
            else:
                print(f"  - Could not find 5 choices for Question {i+1}, skipping.")

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Kirim']")))
        submit_button.click()
        
        print("\n✅ Form submitted successfully!")
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

# --- Run the Automation ---
if __name__ == "__main__":
    number_of_submissions = 25
    for i in range(number_of_submissions):
        print(f"\n--- Starting submission {i+1} of {number_of_submissions} ---")
        fill_questionnaire_form()
        if i < number_of_submissions - 1:
            time.sleep(2)