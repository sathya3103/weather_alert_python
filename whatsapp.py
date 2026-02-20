
import pywhatkit
import datetime
import os
import urllib.parse
import time
import socket
import traceback
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure console supports UTF-8 for emojis
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

PHONE_NUMBER = os.getenv("PHONE_NUMBER")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception:
    webdriver = None

_driver_path = None

def get_driver_path():
    global _driver_path
    if _driver_path is None:
        try:
            # Check if chromedriver.exe is in current directory first
            local_driver = os.path.join(os.getcwd(), "chromedriver.exe")
            if os.path.exists(local_driver):
                _driver_path = local_driver
                return _driver_path
                
            print("📦 Syncing with ChromeDriver...")
            # Use a slightly more direct install to avoid complex manager logic hangs
            _driver_path = ChromeDriverManager().install()
        except Exception as e:
            print(f"❌ Driver sync failed: {e}")
    return _driver_path

def is_port_open(host, port):
    try:
        # socket.create_connection is smarter on Windows; it handles IPv4/IPv6 automatically
        with socket.create_connection((host, port), timeout=2.0):
            return True
    except:
        return False

def send_whatsapp(message):
    if not PHONE_NUMBER:
        print("❌ Error: PHONE_NUMBER not found in .env")
        return False

    print(f"\n📲 Preparing alert for {PHONE_NUMBER}...")

    # We check multiple variations of the debug address
    found_port = False
    print(f"🔍 Checking for open debug port 9222...")
    for addr in ['127.0.0.1', 'localhost', '::1']:
        try:
            if is_port_open(addr, 9222):
                print(f"🔗 Success! Detected browser on {addr}:9222. Attaching...")
                if send_whatsapp_attach(message, f"{addr}:9222"):
                    print("✅ Delivered via Active Browser session.")
                    return True
                found_port = True
                break
            else:
                print(f"➖ No browser found on {addr}:9222")
        except Exception as e:
            print(f"⚠️ Error checking {addr}: {e}")
    
    if found_port:
        print("⚠️ Attachment succeeded but message sending failed. Trying automation...")

    print("🕵️ Starting Selenium Automation...")
    if send_whatsapp_fast(message):
        print("✅ Delivered via Selenium.")
        return True

    print("📲 Falling back to PyWhatKit Instant...")
    try:
        pywhatkit.sendwhatmsg_instantly(PHONE_NUMBER, message, wait_time=15, tab_close=True, close_time=3)
        print("✅ Delivered via PyWhatKit.")
        return True
    except Exception as e:
        print(f"❌ Instant hand-off failed: {e}")
        try:
            now = datetime.datetime.now()
            target = now + datetime.timedelta(seconds=90)
            print(f"⏰ Final fallback: Scheduling for {target.strftime('%H:%M')}...")
            pywhatkit.sendwhatmsg(PHONE_NUMBER, message, target.hour, target.minute, wait_time=20)
            return True
        except Exception:
            return False

def send_whatsapp_fast(message):
    if webdriver is None:
        print("❌ Selenium missing.")
        return False

    driver_path = get_driver_path()
    if not driver_path: 
        print("❌ Could not locate ChromeDriver.")
        return False

    profile_path = os.getenv("CHROME_PROFILE_PATH")
    options = webdriver.ChromeOptions()
    
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1200,900")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    profile_applied = False
    if profile_path:
        profile_path = os.path.normpath(profile_path)
        data_dir = os.path.dirname(profile_path)
        profile_name = os.path.basename(profile_path)
        
        if profile_name.lower() in ['default', 'profile 1', 'profile 2']:
             options.add_argument(f"--user-data-dir={data_dir}")
             options.add_argument(f"--profile-directory={profile_name}")
        else:
             options.add_argument(f"--user-data-dir={profile_path}")
        profile_applied = True

    driver = None
    try:
        print(f"🖥️  Launching Browser {'(with your profile)' if profile_applied else '(guest)'}...")
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
        clean_num = PHONE_NUMBER.replace("+", "").strip()
        url = f"https://web.whatsapp.com/send?phone={clean_num}&text={urllib.parse.quote(message)}"
        driver.get(url)
        
        print("⏳ Waiting for WhatsApp Web Interface...")
        wait = WebDriverWait(driver, 60)
        
        locators = [
            (By.XPATH, "//div[@contenteditable='true' and @data-tab]"),
            (By.CSS_SELECTOR, "div[title='Type a message']"),
            (By.CSS_SELECTOR, "div.lexical-rich-text-input div[contenteditable='true']")
        ]
        
        box = None
        for locator in locators:
            try:
                box = wait.until(EC.presence_of_element_located(locator))
                if box: break
            except:
                continue
        
        if not box:
            raise Exception("Input box not found. Check if you need to scan the QR code.")
            
        time.sleep(5)
        box.send_keys(Keys.ENTER)
        print("📡 Send command executed.")
        
        time.sleep(7)
        driver.quit()
        return True
    except Exception as e:
        error_msg = str(e).lower()
        # Only report as a lock issue if the error message specifically mentions locks or already in use
        if profile_applied and ("locked" in error_msg or "already in use" in error_msg):
            print("\n🚨 CRITICAL: YOUR CHROME PROFILE IS LOCKED")
            print("--------------------------------------------------")
            print("This happens because Chrome is currently running.")
            print("\n✅ FIX: Close ALL Chrome windows or use Option 1 below.")
            
            userDataDir = os.path.dirname(profile_path) if profile_applied else "C:\\Temp\\Chrome"
            print("\n✅ OPTION 1: Starting Chrome in 'Debug Mode' first:")
            print(f'   & "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="{userDataDir}"')
            print("--------------------------------------------------")
        else:
            # Show the real error for transparency
            print(f"\n❌ Automation Error: {e}")
            if "exited" in error_msg:
                print("💡 Suggestion: Try deleting 'chromedriver.exe' in the project folder to force a sync.")
        
        if driver:
            try: driver.quit()
            except: pass
        return False

def send_whatsapp_attach(message, debugger_address='127.0.0.1:9222'):
    if webdriver is None: return False
    driver_path = get_driver_path()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", debugger_address)
    
    try:
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
        clean_num = PHONE_NUMBER.replace("+", "").strip()
        url = f"https://web.whatsapp.com/send?phone={clean_num}&text={urllib.parse.quote(message)}"
        driver.get(url)
        
        # We don't quit the driver here because we are attached
        wait = WebDriverWait(driver, 45)
        input_xpath = "//div[@contenteditable='true' and @data-tab]"
        wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        
        time.sleep(3)
        box = driver.find_element(By.XPATH, input_xpath)
        box.send_keys(Keys.ENTER)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Attachment Sending Error: {e}")
        return False

def send_whatsapp_debug(message, screenshot_path='whatsapp_debug.png'):
    return send_whatsapp_fast(message)
