from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import shutil
from selenium.common.exceptions import TimeoutException
import pandas as pd
from time import sleep


def scrape_reviews(url):
# make chrome log requests
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
    options = webdriver.ChromeOptions()
    # options = webdriver.FirefoxOptions()
    
    # Chrome will start in Headless mode
    options.add_argument('--headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"} )
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')     
    # options.set_capability("goog:loggingPerfs", {'browser': 'ALL'})
    # options.set_capability("goog:loggingPerfs", {'client': 'ALL'})
    # options.set_capability("goog:loggingPerfs", {'driver': 'ALL'})
    # options.set_capability("goog:loggingPerfs",{'server': 'ALL'})
    # options.log.level = "trace"
    # options.set_capability("moz:firefoxOptions", {"log": {"level": "trace"}})
    # options.set_capability("marionette", False)
    
    driver = webdriver.Chrome(
        # service = Service(ChromeDriverManager().install()),
        # service=Service(ChromeDriverManager().install()),
        options=options,
        # desired_capabilities=desired_capabilities
    )

    # fetch a site that does xhr requests
    # driver.get("https://www.tiket.com/review?product_type=TIXHOTEL&searchType=INVENTORY&inventory_id=infinity8-bali-506001655965152937&reviewSubmitColumn=RATING_SUMMARY&hideToolbar=null")
    driver.get(url)
    sleep(5)  # wait for the requests to take place

    # extract requests from logs
    page_class = "Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold"
    l = 0
    for page in driver.find_elements(By.XPATH, "//*[@class='Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold']"):
        try :
            l = int(page.text)
        except : 
            print("Error occur! page_text =", page.text)
    i = 0
    print("total pages:",l)

    total_reviews = int(driver.find_element(By.XPATH, "//*[@class='HcPVsG_text HcPVsG_variant_lowEmphasis HcPVsG_size_b3 HcPVsG_weight_regular']").text.split(" ")[1])
    print("total reviews:",total_reviews)

    driver.find_element(By.XPATH, "//*[@class='Filter_desktop_filter_text__GQYAq HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_regular']").click()
    for sortby in WebDriverWait(driver,12).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='CollapseComponent_filter_option_container__3akFB']"))):
        if sortby.text == 'Review Terbaru':
            sortby.click()
            break
    
    dict_name = url.split('&')[2][13:]
    if os.path.exists(dict_name):  
        shutil.rmtree(dict_name)
    os.makedirs(dict_name)
    return dict_name, driver, total_reviews, l



def scrape_pages(dict_name, driver, l):
    try:
        for n in range(2,l+1):
        
            if n == 7:
                for page in driver.find_elements(By.XPATH, "//*[@class='Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold']"):
                    if int(page.text) == 1:
                        sleep(3)
                        page.click()
                        break
                for page in driver.find_elements(By.XPATH, "//*[@class='Pagination_page_number__iJiI3']"):
                    sleep(3)
                    page.click()
                
            page_btn = EC.presence_of_all_elements_located((By.XPATH, "//*[@class='Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold']"))

            for page in WebDriverWait(driver,12).until(page_btn):
                try :
                    if int(page.text) == n:
                        sleep(1.2)
                        page.click()
                        print(f"page {n} clicked!")
                        break
                    # elif int(page.text) % 6 == 0:

                except :
                    print("Error! page name =",page.text)
            # sleep(2.5)

            logs_raw = driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

            def log_filter(log_):
                return (
                    # is an actual response
                    log_["method"] == "Network.responseReceived"
                    # and json
                    and "json" in log_["params"]["response"]["mimeType"]
                )
            
            for i,log in enumerate(filter(log_filter, logs)):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                f_name = f"{n}-{i}.json"
                with open(os.path.join(dict_name,f_name), "w") as f:
                    try :
                        data1 = json.loads(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body'])['data']
                        f.write(json.dumps(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']))
                    except :
                        print("An error occur!")
            
    except TimeoutException as e:
        print("Timeout detected!")
    
    finally :
        return n
    
def scrape_one_page(dict_name, driver, n):
    
    if n == 7:
        for page in driver.find_elements(By.XPATH, "//*[@class='Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold']"):
            if int(page.text) == 1:
                # sleep(10)
                try :
                    ActionChains(driver).move_to_element(page).perform()
                except:
                    print("Target Out of Bound!")
                # print('yoauw')
                
                driver.execute_script("arguments[0].click();", page)
                break
        print("kndamldnak")
        for nmn in WebDriverWait(driver,21).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class, 'Pagination_page_number__iJiI3')]"))):
            print(nmn.text)
            if nmn.text == '':
                driver.execute_script("arguments[0].click();", nmn.find_element(By.XPATH, ".."))
                break
            else :
                print("LAMAO")
            # sleep(10)
            # page.click()
            # break
        
    page_btn = EC.presence_of_all_elements_located((By.XPATH, "//*[@class='Pagination_page_number__iJiI3 HcPVsG_text HcPVsG_size_b2 HcPVsG_weight_bold']"))
    try :
        for page in WebDriverWait(driver,21).until(page_btn):
            try :
                if int(page.text) == n:
                    # sleep(5)
                    try :
                        ActionChains(driver).move_to_element(page).perform()
                    except :
                        print('target out of boundS!')
                    # print("CLLLLLALA")
                    try :
                        driver.execute_script("arguments[0].click();", page)
                    except:
                        print("UNCLICKABLE!")
                    print(f"page {n} clicked!")
                    break
                # elif int(page.text) % 6 == 0:
            except :
                print("Error! page name =",page.text)
    except :
        print("TimeoutException!")
        raise TimeoutException()
    # sleep(2.5)

    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
        )
    
    for i,log in enumerate(filter(log_filter, logs)):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        f_name = f"{n}-{i}.json"
        with open(os.path.join(dict_name,f_name), "w") as f:
            try :
                a = json.loads(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body'])['data']
                f.write(json.dumps(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']))
            except :
                print("An error occur!")
    return n
        
    # except TimeoutException as e:
    #     print("Timeout detected!")
        
    #     raise Exception
    
    # finally :
    #     # driver.quit()
    #     return n