from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def append_data(file_path, name, document_number, number_of_pages, recorded_date, idate, page, consideration, cities, status
):
    fieldnames = ['Name', 'Document_Number', 'Number_of_Pages','Recorded_Date', 'IDate', 'Page', 'Consideration', 'Cities', 'Status']

    with open(file_path, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow({
            "Name": name,
            "Document_Number": document_number,
            "Number_of_Pages": number_of_pages,
            "Recorded_Date": recorded_date,
            "IDate": idate,
            "Page": page,
            "Consideration": consideration,
            "Cities": cities,
            "Status": status

})



driver = webdriver.Firefox()
driver.set_page_load_timeout(10000)
url = "https://bexar.tx.publicsearch.us/results?department=RP&docTypes=ACKNOW&limit=250&recordedDateRange=17530101%2C20181217&searchType=advancedSearch"

driver.get(url)
driver.implicitly_wait(50) 
delay = 50
for i in range(0,1000):
    try:
        myElem = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='page']/div[3]/div/div[2]/div[1]/table")))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time internet connection is slow!"
    thirdrd_ele = driver.find_element_by_xpath(
        "// *[@id='page']/div[3]/div/div[2]/div[1]/table/tbody")
    rows = thirdrd_ele.find_elements_by_tag_name("tr")
    driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div/div[2]/div/button[1]").click()
    for i in rows:
        a = i.find_elements_by_tag_name("td")
        a[3].click()
        driver.implicitly_wait(3)
        try:
            driver.find_element_by_xpath("//*[@id = 'content']/main/div[2]/div[1]/div/div/div/div/header/div/ul/li[2]").click()
            driver.implicitly_wait(3)
            head_ele = driver.find_element_by_xpath("//*[@id='content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[1]").text
            # head = head_ele.get_attribute("h2")
            print head_ele
            number = driver.find_element_by_xpath("//*[@id = 'content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[1]/li[1]/span[2]").text
            print number
            num_of_pages = driver.find_element_by_xpath("//*[@id = 'content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[1]/li[2]/span[2]").text
            print num_of_pages
            
            redate = driver.find_element_by_xpath("//*[@id='content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[1]/li[3]/span[2]").text
            print redate
            book = driver.find_element_by_xpath("//*[@id = 'content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[2]/li[1]/span[2]").text
            print book
            indate = driver.find_element_by_xpath("//*[@id='content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[2]/li[2]/span[2]").text
            print indate
            consderation = driver.find_element_by_xpath("//*[@id='content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/ul[2]/li[3]/span[2]").text
            print consderation
            parties = driver.find_element_by_xpath("//*[@id = 'content']/main/div[2]/div[1]/div/div/div/div/div/div[2]/div[3]/div")
            parlist = parties.find_elements_by_tag_name("li")
            print "i am here"
            for i in parlist:
                b = i.find_element_by_tag_name("a")
                city = b.text
                f = i.find_element_by_tag_name("span")
                gov = f.text
                print city, gov
            append_data("Result.csv", head_ele, number,num_of_pages, redate, indate, book, consderation, city, gov)
        except:
            pass

        try:
            myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[1]/div/div/button[1]")))
            print "now going for next"
        except:
            pass
        try:
            driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/div/div/button[1]").click()
            sleep(2)
        except:
            pass
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    driver.find_element_by_xpath(
        "//*[@id='page']/div[3]/div/div[2]/div[2]/nav/div/button[12]").click()
    driver.implicitly_wait(15)
    


