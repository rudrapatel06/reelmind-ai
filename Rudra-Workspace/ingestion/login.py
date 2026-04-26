import os
from playwright.sync_api import sync_playwright

SESSION_DIR = "session_data"

def login_to_instagram():
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
        
    print("Opening browser. Please log in to Instagram and press Enter in the terminal when done.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        
        input("Press Enter here after you have successfully logged in and the feed has loaded...")
        
        context.storage_state(path=os.path.join(SESSION_DIR, "state.json"))
        print(f"Session saved to {os.path.join(SESSION_DIR, 'state.json')}")
        browser.close()

if __name__ == "__main__":
    login_to_instagram()
