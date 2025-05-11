from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime
from selenium.webdriver.chrome.options import Options
import mysql.connector
import re

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="golfdb"
)



class Slot:
    def __init__(self, timeslot, price):
        self.timeslot = timeslot
        self.price = price
    def __repr__(self):
        return f"TimeSlot(time={self.timeslot}, price={self.price})"

MathernSlots = {}
BristolSlots = {}
WoodspringSlots = {}
WoodlandsMastersSlots = {}
WoodlandsSignatureSlots = {}

# Set up the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
driver = webdriver.Chrome(options=chrome_options)
time.sleep(5)

daterange = []
# Get todays date
for i in range(7):
    newdate = datetime.date.today() + datetime.timedelta(days=i)
    daterange.append(newdate)

# create date list

# MATHERN COURSE
for date in daterange:
    siteaddress = "https://book.stpierre.marriottlifestyle.co.uk/golf?course=MAT&date=" + str(date) + "&golfers=4&holes=18"

    # Go to the golf booking site
    driver.get(siteaddress)

    # Replace time.sleep(7) with:
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".Form-sc-1vwavb0-0.kdATrV"))
    )
    time.sleep(6)
    getprices = driver.find_elements(by= By.CSS_SELECTOR, value=".TeeTimestyles__TeeTime__Copy-sc-8z9guk-2.dsYsHM")
    gettimes = driver.find_elements(by= By.CSS_SELECTOR, value=".TeeTimestyles__TeeTime__Heading-sc-8z9guk-3.liVoKP")

    pricelist = []
    timelist = []

    for x in range(len(getprices)):
        
        raw_price = getprices[x]
        clean_price = re.findall(r"\d+\.\d+", raw_price.text)
        price_str = clean_price[0] if clean_price else None
        pricelist.append(price_str)

    for x in range(len(gettimes)):
        a = gettimes[x]
        timelist.append(a.text)
    MathernSlots[date] = [Slot(t, p) for t, p in zip(timelist, pricelist)]


# THE BRISTOL COURSE
siteaddress = "https://golf.bristolgolfclub.co.uk/visitorbooking/"
     # Go to the golf booking site
driver.get(siteaddress)
for date in daterange:
    
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#container"))
    )

    gettimes = driver.find_elements(By.CLASS_NAME, "slot-time")
    getprices = driver.find_elements(By.CLASS_NAME, "slot-price")
    pricelist = []
    timelist = []
    for x in range(len(getprices)):
        raw_price = getprices[x]
        clean_price = re.findall(r"\d+\.\d+", raw_price.text)
        price_str = clean_price[0] if clean_price else None
        pricelist.append(price_str)

    for x in range(len(gettimes)):
        a = gettimes[x]
        timelist.append(a.text)

    BristolSlots[date] = [Slot(t, p) for t, p in zip(timelist, pricelist)]
    driver.find_element(By.CLASS_NAME, "fa.fa-arrow-right").click()
    time.sleep(5)
    


# WOODSPRING 18
siteaddress = "https://woodspring.intelligentgolf.co.uk/visitorbooking/"
     # Go to the golf booking site
driver.get(siteaddress)
for date in daterange:
    
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#container"))
    )

    gettimes = driver.find_elements(By.CLASS_NAME, "slot-time")
    getprices = driver.find_elements(By.CLASS_NAME, "slot-price")
    pricelist = []
    timelist = []
    for x in range(len(getprices)):
        raw_price = getprices[x]
        clean_price = re.findall(r"\d+\.\d+", raw_price.text)
        price_str = clean_price[0] if clean_price else None
        pricelist.append(price_str)

    for x in range(len(gettimes)):
        a = gettimes[x]
        timelist.append(a.text)

    WoodspringSlots[date] = [Slot(t, p) for t, p in zip(timelist, pricelist)]
    driver.find_element(By.CLASS_NAME, "fa.fa-arrow-right").click()
    time.sleep(5)

# WOODLANDS MASTERS
siteaddress = "https://woodlands.intelligentgolf.co.uk/visitorbooking/"
     # Go to the golf booking site
driver.get(siteaddress)

for date in daterange:
    
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#container"))
    )

    gettimes = driver.find_elements(By.CLASS_NAME, "slot-time")
    getprices = driver.find_elements(By.CLASS_NAME, "slot-price")
    pricelist = []
    timelist = []
    for x in range(len(getprices)):
        a = getprices[x]
        pricelist.append(a.text)

    for x in range(len(gettimes)):
        raw_price = getprices[x]
        clean_price = re.findall(r"\d+\.\d+", raw_price.text)
        price_str = clean_price[0] if clean_price else None
        pricelist.append(price_str)

    WoodlandsMastersSlots[date] = [Slot(t, p) for t, p in zip(timelist, pricelist)]
    driver.find_element(By.CLASS_NAME, "fa.fa-arrow-right").click()
    time.sleep(5)




 # WOODLANDS SIGNATURE
siteaddress = "https://woodlands.intelligentgolf.co.uk/visitorbooking/"
     # Go to the golf booking site
driver.get(siteaddress)
try:
    (driver.find_element(By.CLASS_NAME, "teetimes-today-link").click())
except:
    print("Already on todays date")

# Navigate to Sig course
driver.find_element(By.NAME, "course").click()
time.sleep(1)
driver.find_element(By.NAME, "course").send_keys("s")
time.sleep(1)
driver.find_element(By.NAME, "course").send_keys(" \
")
time.sleep(1)

for date in daterange:
    
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#container"))
    )

    gettimes = driver.find_elements(By.CLASS_NAME, "slot-time")
    getprices = driver.find_elements(By.CLASS_NAME, "slot-price")
    pricelist = []
    timelist = []
    # Woodlands give price for 2 ball
    for x in range(len(getprices)):
        raw_price = getprices[x]
        clean_price = re.findall(r"\d+\.\d+", raw_price.text)
        price_str = clean_price[0] if clean_price else None
        a = float(price_str)/2
        pricelist.append(a)

    for x in range(len(gettimes)):
        a = gettimes[x]
        timelist.append(a.text)

    WoodlandsSignatureSlots[date] = [Slot(t, p) for t, p in zip(timelist, pricelist)]
    driver.find_element(By.CLASS_NAME, "fa.fa-arrow-right").click()
    time.sleep(5)

Courses = {

"Mathern Course" : MathernSlots,
"Bristol Course" : BristolSlots,
"Woodspring Course" : WoodspringSlots,
"Woodlands Masters Course" : WoodlandsMastersSlots,
"Woodlands Signature Course" : WoodlandsSignatureSlots
}
cursor = conn.cursor()

# Clear slots
cursor.execute("DELETE FROM slots")
conn.commit()

for course_name, dates in Courses.items():
    # Insert course if it doesn't exist
    cursor.execute("INSERT IGNORE INTO courses (name) VALUES (%s)", (course_name,))
    conn.commit()

    

    # Get course_id
    cursor.execute("SELECT id FROM courses WHERE name = %s", (course_name,))
    course_id = cursor.fetchone()[0]
    
    for date_str, slot_list in dates.items():
        for slot in slot_list:
            time_str = slot.timeslot
            try: 
                price_str = slot.price.replace("£", "").strip()
            except:
                price_str = slot.price
            cursor.execute(
                "INSERT INTO slots (course_id, date, time, price) VALUES (%s, %s, %s, %s)",
                (course_id, date_str, time_str, price_str)
            )

conn.commit()

cursor.close()
conn.close()
print(Courses)
# Close the browser
driver.quit()
