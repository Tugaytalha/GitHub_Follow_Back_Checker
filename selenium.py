import gradio as gr
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
GITHUB_BASE_URL = "https://github.com"

# Adjust these XPaths or use alternative selectors as needed
FOLLOWER_XPATH = "//span[@class='Link--secondary']"
FOLLOWING_XPATH = "//span[@class='Link--secondary']"

# Some pages might have a "Next" button. Adjust as needed.
NEXT_PAGE_XPATH = "//a[contains(@class,'next_page')]"


# ---------------------------------------------------------------------
# Scraping Functions
# ---------------------------------------------------------------------
def get_usernames_in_tab(driver, username, tab_type):
    """
    Scrape all usernames from a given tab_type ('followers' or 'following')
    for the specified username.
    """
    all_usernames = set()
    page_num = 1

    while True:
        url = f"{GITHUB_BASE_URL}/{username}?page={page_num}&tab={tab_type}"
        driver.get(url)
        time.sleep(2)  # Adjust or remove with explicit waits if needed

        # Collect the usernames from the current page
        elements = driver.find_elements(By.XPATH, FOLLOWER_XPATH if tab_type == 'followers' else FOLLOWING_XPATH)
        if not elements:
            break  # No more users found, probably an empty or invalid page

        for elem in elements:
            nickname = elem.text.strip()
            if nickname:
                all_usernames.add(nickname)

        # Check if there's a "Next" page
        next_buttons = driver.find_elements(By.XPATH, NEXT_PAGE_XPATH)
        if not next_buttons:
            break  # No next page, we can stop
        page_num += 1  # Move to next page

    return all_usernames


def find_non_mutual_follows(username):
    """
    Returns the list of users that 'username' follows but who do not follow back.
    """
    # Initialize WebDriver
    service = Service("chromedriver")  # Adjust path if needed
    driver = webdriver.Chrome(service=service)

    try:
        followers = get_usernames_in_tab(driver, username, 'followers')
        following = get_usernames_in_tab(driver, username, 'following')

        # Users that the username follows but aren't in its followers
        not_following_back = following - followers
        return sorted(not_following_back)

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        driver.quit()


# ---------------------------------------------------------------------
# Gradio Interface
# ---------------------------------------------------------------------
def check_follows(username):
    if not username.strip():
        return "Please provide a valid GitHub username."

    result = find_non_mutual_follows(username)
    if isinstance(result, str) and result.startswith("Error"):
        return result
    if not result:
        return "Everyone you follow follows you back, or the lists are empty."
    return "\n".join(result)


# Create Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("# GitHub Follow Checker")
    gr.Markdown("Find out who you follow but doesn't follow you back on GitHub.")

    with gr.Row():
        username_input = gr.Textbox(label="GitHub Username", placeholder="Enter GitHub username...")
        result_output = gr.Textbox(label="Results", lines=10)

    check_button = gr.Button("Check")
    check_button.click(check_follows, inputs=username_input, outputs=result_output)

# Run the Gradio App
app.launch()
