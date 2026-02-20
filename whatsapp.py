import pywhatkit
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER = os.getenv("PHONE_NUMBER")

def send_whatsapp(message):
    # Fastest path: try attaching to a running Chrome with remote debugging (requires Chrome started with --remote-debugging-port=9222)
    attached = False
    try:
        attached = send_whatsapp_attach(message)
    except Exception:
        attached = False
    if attached:
        return True

    now = datetime.datetime.now()
    # Next-fastest: PyWhatKit instant send (may take ~5-7s depending on machine)
    try:
        pywhatkit.sendwhatmsg_instantly(PHONE_NUMBER, message, wait_time=6, tab_close=True, close_time=1)
        print("✅ WhatsApp message sent (pywhatkit instant).")
        return True
    except Exception as e:
        print(f"⚠️ Instant send failed: {e}. Falling back to scheduled send (robust scheduling).")
        try:
            # Schedule at least 120 seconds in the future to avoid negative sleep inside pywhatkit
            target = now + datetime.timedelta(seconds=120)
            send_hour = target.hour
            send_minute = target.minute
            # Use a small wait_time for pywhatkit (seconds it waits after opening WhatsApp Web)
            wait_time = 5
            pywhatkit.sendwhatmsg(PHONE_NUMBER, message, send_hour, send_minute, wait_time=wait_time)
            print("✅ WhatsApp message scheduled (pywhatkit fallback).")
            return True
        except Exception as e2:
            print(f"❌ Scheduled fallback also failed: {e2}")
            return False


# --- Selenium fast-send fallback -------------------------------------------------
# This attempts an almost-instant send by reusing your Chrome profile (logged-in)
# Set CHROME_PROFILE_PATH in your .env to your Chrome user data directory, e.g.
# C:\Users\<you>\AppData\Local\Google\Chrome\User Data
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import urllib.parse
    import time
except Exception:
    webdriver = None


def send_whatsapp_fast(message):
    """Attempt to send within ~5s using Selenium and an existing Chrome profile.

    Requires CHROME_PROFILE_PATH in .env pointing to your Chrome user data dir.
    """
    if webdriver is None:
        print("⚠️ Selenium or webdriver-manager not installed. Fast send unavailable.")
        return False

    profile = os.getenv("CHROME_PROFILE_PATH")
    options = webdriver.ChromeOptions()
    # Keep the Chrome window open after the WebDriver session ends
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # Reuse existing Chrome profile: pass user-data-dir=parent_dir and profile-directory=basename
    if profile:
        profile = os.path.normpath(profile)
        parent = os.path.dirname(profile)
        basename = os.path.basename(profile)
        # If user provided the top-level 'User Data' folder, use it directly
        if basename.lower() == 'user data':
            options.add_argument(f"--user-data-dir={profile}")
        else:
            options.add_argument(f"--user-data-dir={parent}")
            options.add_argument(f"--profile-directory={basename}")
    # Start in a new window to avoid homepage/extension interceptors
    options.add_argument("--new-window")

    # Build URL to open chat with prefilled text
    url = f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}&text={urllib.parse.quote(message)}"

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"❌ Could not start Chrome with the provided profile. Ensure all Chrome windows are closed and try again. Error: {e}")
        return False
    driver.get(url)
    # Some Chrome setups redirect homepage/open-tab; force navigation via JS
    try:
        driver.execute_script("window.location.href = arguments[0];", url)
    except Exception:
        pass

    sent = False
    try:
        # Fast path: wait up to 5s for the message input to appear
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab]"))
        )
        box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab]")
        box.send_keys(Keys.ENTER)
        sent = True
    except Exception:
        # Retry navigation once more (force) and extend wait
        try:
            driver.execute_script("window.location.href = arguments[0];", url)
            WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab]"))
            )
            box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab]")
            box.send_keys(Keys.ENTER)
            sent = True
        except Exception:
            # Not ready yet — check if QR/login is shown
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label], div[data-testid='qrcode']"))
                )
                print("❌ WhatsApp Web requires login (QR shown). Please log into WhatsApp Web in this profile and retry.")
            except Exception:
                # Try clicking send button as another fallback
                try:
                    send_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']"))
                    )
                    send_btn.click()
                    sent = True
                except Exception:
                    # Give diagnostics
                    try:
                        current = driver.current_url
                        title = driver.title
                        print(f"❌ Fast-send failed. URL: {current} | Title: {title}")
                    except Exception:
                        print("❌ Fast-send failed and diagnostics unavailable.")

    # Optionally quit the driver to close the browser instance
    try:
        driver.quit()
    except Exception:
        try:
            driver.close()
        except Exception:
            pass

    if sent:
        print("✅ WhatsApp message sent (selenium fast-send).")
    else:
        print("❌ Selenium fast-send failed within 10s.")
        try:
            print(f"URL: {driver.current_url} | Title: {driver.title}")
        except Exception:
            pass

    return sent


def send_whatsapp_debug(message, screenshot_path='whatsapp_debug.png'):
    """Open WhatsApp Web with Selenium, save a screenshot and print diagnostics.

    Use this to see what page WhatsApp Web shows (QR/login, error page, etc.).
    """
    if webdriver is None:
        print("⚠️ Selenium not available.")
        return False

    profile = os.getenv("CHROME_PROFILE_PATH")
    options = webdriver.ChromeOptions()
    # Keep the Chrome window open after the WebDriver session ends
    options.add_experimental_option("detach", True)
    if profile:
        profile = os.path.normpath(profile)
        parent = os.path.dirname(profile)
        basename = os.path.basename(profile)
        if basename.lower() == 'user data':
            options.add_argument(f"--user-data-dir={profile}")
        else:
            options.add_argument(f"--user-data-dir={parent}")
            options.add_argument(f"--profile-directory={basename}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"❌ Could not start Chrome with the provided profile. Ensure all Chrome windows are closed and try again. Error: {e}")
        return False
    url = f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}&text={urllib.parse.quote(message)}"
    driver.get(url)

    # Wait briefly for page to load, then capture diagnostics
    time.sleep(3)
    try:
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"⚠️ Failed to save screenshot: {e}")

    try:
        title = driver.title
        current = driver.current_url
        print(f"Title: {title}")
        print(f"URL: {current}")
    except Exception:
        print("⚠️ Could not read title/url")

    # Check for QR / login
    try:
        qr = driver.find_element(By.CSS_SELECTOR, "canvas[aria-label], div[data-testid='qrcode']")
        print("❌ QR/login detected on page.")
    except Exception:
        print("ℹ️ No QR detected (session may be present).")

    # Check for message input
    try:
        box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab]")
        print("✅ Message input present.")
    except Exception:
        print("❌ Message input not found.")

    # Print a short snippet of page source for inspection
    try:
        src = driver.page_source
        snippet = src[:1000].replace('\n', ' ')
        print("Page source snippet:", snippet)
    except Exception:
        print("⚠️ Could not read page source.")

    try:
        driver.quit()
    except Exception:
        pass

    return True


def send_whatsapp_attach(message, debugger_address='127.0.0.1:9222'):
    """Attach to an already-running Chrome started with --remote-debugging-port=9222

    Steps for the user:
    1. Close all Chrome windows.
    2. Start Chrome manually with your profile and remote debugging:
       "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\nesar\\AppData\\Local\\Google\\Chrome\\User Data"
    3. Run this function (it will attach to that Chrome instance).
    """
    if webdriver is None:
        print("⚠️ Selenium not available.")
        return False

    options = webdriver.ChromeOptions()
    # When attaching to an already-running Chrome, prefer not to close it
    # Do not set the unsupported 'detach' experimental option when attaching
    options.add_experimental_option("debuggerAddress", debugger_address)
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"❌ Could not attach to Chrome at {debugger_address}: {e}")
        return False

    url = f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}&text={urllib.parse.quote(message)}"
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab]")))
        box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab]")
        box.send_keys(Keys.ENTER)
        print("✅ WhatsApp message sent (attached Chrome).")
        return True
    except Exception as e:
        try:
            print(f"❌ Failed to send via attached Chrome: {e} | URL: {driver.current_url}")
        except Exception:
            print(f"❌ Failed to send via attached Chrome: {e}")
        return False
