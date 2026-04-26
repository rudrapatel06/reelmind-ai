import os
import time
import re
from playwright.sync_api import sync_playwright

SESSION_DIR = "session_data"
STATE_PATH = os.path.join(SESSION_DIR, "state.json")

def process_and_save_reel(url: str) -> dict:
    """Navigate to the reel, click the Save button, and extract the caption."""
    if not os.path.exists(STATE_PATH):
        raise FileNotFoundError(f"Session state not found at {STATE_PATH}. Please run login.py first.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=STATE_PATH,
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            
            # 1. EXTRACT REAL CAPTION
            print("Scraping caption...")
            raw_caption = ""
            try:
                caption_selectors = ['h1', 'article [dir="auto"]', 'meta[property="og:title"]']
                for selector in caption_selectors:
                    if selector.startswith('meta'):
                        el = page.locator(selector).first
                        if el.count() > 0:
                            raw_caption = el.get_attribute('content')
                    else:
                        el = page.locator(selector).first
                        if el.count() > 0:
                            raw_caption = el.text_content()
                    if raw_caption and len(raw_caption) > 10:
                        break
                if not raw_caption: raw_caption = page.title()
            except: 
                raw_caption = page.title()
            
            # 2. CLICK THE SAVE BUTTON
            print("Clicking Save...")
            save_btn = page.locator('svg[aria-label="Save"]').first
            status = "unknown"
            
            if save_btn.count() > 0:
                save_btn.locator("..").click()
                print("Successfully saved!")
                status = "success"
                page.wait_for_timeout(1000)
            else:
                already_saved = page.locator('svg[aria-label="Remove"]').first
                if already_saved.count() > 0:
                    print("Reel was already saved.")
                    status = "success"
                else:
                    return {"status": "error", "error": "Could not find Save button"}

            return {
                "status": status,
                "caption": raw_caption,
                "url": url
            }

        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error", "error": str(e)}
        finally:
            browser.close()

def unsave_reel(url: str) -> bool:
    """Navigate to the reel and ensure it is unsaved."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=STATE_PATH,
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            remove_btn = page.locator('svg[aria-label="Remove"]').first
            if remove_btn.count() > 0:
                remove_btn.locator("..").click()
                print(f"Unsaved {url}")
                page.wait_for_timeout(1000)
                return True
            return True
        except Exception as e:
            print(f"Unsave error: {e}")
            return False
        finally:
            browser.close()
