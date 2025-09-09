from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import warnings
import csv
from datetime import datetime
import sys
import threading
from queue import Queue

# Logging configuration - ignore all warnings and errors
logging.basicConfig(level=logging.CRITICAL)
warnings.filterwarnings("ignore")

# Queue for collecting results
results_queue = Queue()

def worker(user_number, test_run_id):
    print(f"\n--- Starting test for user {user_number} ---")
    
    # Initial timestamp
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Chrome configuration
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gcm")
    options.add_argument("--disable-cloud-import")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-background-networking")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 1,
    })

    # Initialize browser
    service = webdriver.chrome.service.Service(log_path='NUL')  # Windows
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    try:
        # Log initial time
        results_queue.put({
            "test_run_id": test_run_id,
            "user": f"123456tester{user_number}",
            "event_type": "start",
            "timestamp": start_time,
            "time1": "",
            "time2": "",
            "time3": ""
        })

        print(f"User {user_number}: Logging in...")
        driver.get("https://jupyterhub.prz.edu.pl:8443/test/hub/")
        
        # Login
        username = wait.until(EC.presence_of_element_located((By.ID, "username_input")))
        username.send_keys(f"123456tester{user_number}")
        
        password = wait.until(EC.presence_of_element_located((By.ID, "password_input")))
        password.send_keys("haslo123")
        
        submit = wait.until(EC.element_to_be_clickable((By.ID, "login_submit")))
        submit.click()
        
        print(f"User {user_number}: Waiting for interface to load...")
        time.sleep(10)
        
        # Navigation
        print(f"User {user_number}: Clicking home folder...")
        home_folder = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.jp-BreadCrumbs-home"))
        )
        home_folder.click()
        time.sleep(3)
        
        print(f"User {user_number}: Double-clicking public folder...")
        work_folder = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'jp-DirListing-item') and contains(., 'public')]"))
        )
        actions.double_click(work_folder).perform()
        time.sleep(3)
        
        print(f"User {user_number}: Double-clicking admin folder...")
        admin_folder = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'jp-DirListing-item') and contains(., 'admin')]"))
        )
        actions.double_click(admin_folder).perform()
        time.sleep(3)
        
        # Open notebook
        print(f"User {user_number}: Opening Untitled.ipynb...")
        notebook_file = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'jp-DirListing-item') and contains(., 'Untitled.ipynb')]"))
        )
        actions.double_click(notebook_file).perform()
        time.sleep(5)
        
        # Run code
        print(f"User {user_number}: Running the notebook...")
        run_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-command='runmenu:run']"))
        )
        run_button.click()
        
        print(f"User {user_number}: Waiting for code to execute (30 seconds)...")
        time.sleep(30)
        
        # Get results
        output_cells = driver.find_elements(By.CSS_SELECTOR, ".jp-OutputArea-output")
        times = []
        
        for cell in output_cells:
            text = cell.text.strip()
            if "Czas" in text:
                for line in text.split('\n'):
                    if "Czas" in line:
                        times.append(line)
        
        # Add results to the queue
        results_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if times:
            results_queue.put({
                "test_run_id": test_run_id,
                "user": f"123456tester{user_number}",
                "event_type": "results",
                "timestamp": results_time,
                "time1": times[0].split(":")[1].strip() if len(times) > 0 else "No data",
                "time2": times[1].split(":")[1].strip() if len(times) > 1 else "No data",
                "time3": times[2].split(":")[1].strip() if len(times) > 2 else "No data"
            })
            print(f"User {user_number}: Test completed successfully")
        else:
            print(f"User {user_number}: No execution times found in results")
            results_queue.put({
                "test_run_id": test_run_id,
                "user": f"123456tester{user_number}",
                "event_type": "results",
                "timestamp": results_time,
                "time1": "No data",
                "time2": "No data",
                "time3": "No data"
            })

    except Exception as e:
        print(f"User {user_number}: An error occurred: {e}")
        driver.save_screenshot(f"error_user{user_number}.png")
        print(f"User {user_number}: Screenshot saved as error_user{user_number}.png")
        results_queue.put({
            "test_run_id": test_run_id,
            "user": f"123456tester{user_number}",
            "event_type": "error",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time1": f"Error: {str(e)}",
            "time2": f"Error: {str(e)}",
            "time3": f"Error: {str(e)}"
        })

    finally:
        # Log end time
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results_queue.put({
            "test_run_id": test_run_id,
            "user": f"123456tester{user_number}",
            "event_type": "end",
            "timestamp": end_time,
            "time1": "",
            "time2": "",
            "time3": ""
        })
        
        driver.quit()

def save_results():
    """Function to save results from the queue to a CSV file"""
    filename = "execution_times.csv"
    file_exists = False
    
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    while True:
        result = results_queue.get()
        if result is None:  # Signal to end
            # Add an end marker for the entire test
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["", "", "TEST_COMPLETED", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "", "", ""])
            break
            
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            if not file_exists:
                writer.writerow(["Test ID", "User", "Event Type", "Timestamp", "Time 1", "Time 2", "Time 3"])
                file_exists = True
                
            writer.writerow([
                result["test_run_id"],
                result["user"],
                result["event_type"],
                result["timestamp"],
                result.get("time1", ""),
                result.get("time2", ""),
                result.get("time3", "")
            ])
        
        results_queue.task_done()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <number_of_users>")
        sys.exit(1)
    
    try:
        num_users = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid number of users")
        sys.exit(1)
    
    # Unique ID for this test run
    test_run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    print(f"Starting parallel testing for {num_users} users (Test ID: {test_run_id})...")
    
    # Start the thread that saves results
    results_thread = threading.Thread(target=save_results)
    results_thread.daemon = True
    results_thread.start()
    
    # Start the test threads
    threads = []
    for i in range(1, num_users + 1):
        t = threading.Thread(target=worker, args=(i, test_run_id))
        t.start()
        threads.append(t)
        time.sleep(1)  # Small delay between browser launches
    
    # Wait for all test threads to complete
    for t in threads:
        t.join()
    
    # Signal the saving thread that it can terminate
    results_queue.put(None)
    results_thread.join()
    
    print("\nTesting complete. Results saved in execution_times.csv")
    print(f"ID of this test run: {test_run_id}")

if __name__ == "__main__":
    main()