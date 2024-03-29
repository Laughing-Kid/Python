#This is program that automates the feedback for the 4th semester CS dept

import sys, os, time
import random
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


#    _______ _            _                       _     _               _  ___     _ 
#   |__   __| |          | |                     | |   (_)             | |/ (_)   | |
#      | |  | |__   ___  | |     __ _ _   _  __ _| |__  _ _ __   __ _  | ' / _  __| |
#      | |  | '_ \ / _ \ | |    / _` | | | |/ _` | '_ \| | '_ \ / _` | |  < | |/ _` |
#      | |  | | | |  __/ | |___| (_| | |_| | (_| | | | | | | | | (_| | | . \| | (_| |
#      |_|  |_| |_|\___| |______\__,_|\__,_|\__, |_| |_|_|_| |_|\__, | |_|\_\_|\__,_|
#                                            __/ |               __/ |               
#                                           |___/               |___/ 

feedbackType = 0
def check_element(element):
    if is_firefox:
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, element)))
        except TimeoutException:
            print ("Loading took too much time!")

if __name__ == "__main__":

    #Take students registration number and password
    studentId = input("Enter your registration number: ")
    studentPassword = input("Enter your password: ")
    is_firefox = False
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--hide-scrollbars')
    #options.add_argument('--disable-gpu')
    
    if getattr(sys, 'frozen', False): 
    # executed as a bundled exe, the driver is in the extracted folder
        try:
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            browser = Chrome(chromedriver_path,options=options)
            
        except WebDriverException:
            geckodriver_path = os.path.join(sys._MEIPASS, "geckodriver.exe")
            browser = Firefox(executable_path=geckodriver_path)
            is_firefox = True
            delay = 5
    else:
    # executed as a simple script, the driver should be in `PATH`
        try:
            browser = Chrome(options=options)
        except WebDriverException:
            browser = Firefox()
            is_firefox = True
            delay = 5

    browser.get("http://111.68.99.200/SRA-n/")

    #NOTE: I am continuously using find_by_element instead of storing it in a variable
    #because our universities bad coding practices resest the entire DOM and makes the
    #variable invalid
    
    check_element('ddlDegreeProg')
    # navigate to the page
    select = Select(browser.find_element_by_id("ddlDegreeProg"))
    print("Please select your department")
    for text in range(len(select.options) - 1):
        print(str(text + 1)+".",select.options[text + 1].text)
       
    # print ([o.text for o in select.options]) # these are string-s
    deptNumber = input("Enter option number: ")
    print(type(deptNumber))
    select.select_by_index(int(deptNumber))

    id = browser.find_element_by_id("txtRegNo")
    id.send_keys(studentId)
    
    password = browser.find_element_by_id("a63542B5")
    password.send_keys(studentPassword,Keys.RETURN)
    
    check_element('cmdViewTranscript')
    
    print("Do you want to do basic feedback or detailed feedback?")
    feedbackType = int(input("Press 1 for basic and 2 for detailed feedback: "))

    (browser.find_element_by_id("cmdViewTranscript")).send_keys(Keys.RETURN)
    check_element('btnfeedback')
    (browser.find_element_by_id("btnfeedback")).send_keys(Keys.RETURN)
    
    check_element('_ctl0_ContentPlaceHolder1_ddlCourse')
    course_id = Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse"))
    courses = course_id.options
    
    if feedbackType == 1:
        #Loops through the entire feedback and sets a random value for every question
        for name in range(len(courses) - 1):
            (Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse"))).select_by_index(name)
            
            contributor_id = Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor"))
            contributors = contributor_id.options
            num_of_cont = len(contributors)-1
            
            if num_of_cont > 1:
                _course = Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse"))
                _course_options = _course.options
                
                print("Course", _course_options[name].text ,"has multiple contributors. Kindly select one: ")
                
                for con_id in range(num_of_cont):
                    print(con_id, ". ", contributors[con_id].text, sep="")
                    
                num = input("Enter option number: ")
                (Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor"))).select_by_index(num)
                
            else:     
                (Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor"))).select_by_index(0)

            for i in range(0,18):
                score = "_ctl0_ContentPlaceHolder1_txt" + (chr(ord('A') + i))
                randNumber = random.randrange(1,6)
                (browser.find_element_by_id(score)).send_keys(randNumber)#You can change the value here and set it between 1-5

        #Writes the messages in the two text areas. You can change the messages
            (browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txtComments")).send_keys("""No Comment""")
            (browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txtCommentsCourse")).send_keys("""No Comment""")

            (browser.find_element_by_id("_ctl0_ContentPlaceHolder1_cmdSubmit")).send_keys(Keys.RETURN)
            (browser.find_element_by_id("_ctl0_ContentPlaceHolder1_cmdReset")).send_keys(Keys.RETURN)
            
    elif feedbackType == 2:
        teachers = []
        boxId = ("A1","A2","A3","A4","B2","B3","B4","C1","C2","C3","C4","C5","D1","D2","D3",\
        "D4","D5","E1","E2","E3","E4","F1","F2","F3","F4","G1","G2","G3","G4","H1","H2","H3","I1","I2")
        
        for name in range(len(courses) - 1):
            (Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse"))).select_by_index(name)
            
            contributor_id = Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor"))
            contributors = contributor_id.options
            num_of_cont = len(contributors) - 1
            
            if num_of_cont > 1:
                _course = Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse"))
                _course_options = _course.options
                print("Course", _course_options[name].text ,"has multiple contributors. Kindly select one: ")
                
                for con_id in range(num_of_cont):
                    print(con_id, ". ", contributors[con_id].text, sep="")
                    
                num = input("Enter option number: ")    
                teachers.append(Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor")).options[int(num)].text)
            else:
                teachers.append(Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlContributor")).options[0].text)
        print(teachers)
        browser.find_element_by_id("_ctl0_ContentPlaceHolder1_cmdCourseEvaluation2").send_keys(Keys.RETURN)
        courseLength = len(Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse")).options)
        
        for i in range(courseLength):
            Select(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCourse")).select_by_index(i)
            browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txtfnames").send_keys(teachers[i])
            (browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txtB1")).send_keys("5")
            
            for run in range(len(boxId)):
                currentElement = browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txt"+boxId[run])
                randNumber = random.randrange(1,6)
                if(currentElement.tag_name == "textarea"):
                    currentElement.send_keys("No comment")
                else:
                    browser.find_element_by_id("_ctl0_ContentPlaceHolder1_txt"+boxId[run]).send_keys(randNumber)
                    
            #(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_cmdSubmit")).send_keys(Key.RETURN)
            #(browser.find_element_by_id("_ctl0_ContentPlaceHolder1_cmdReset")).send_keys(Key.RETURN)
        print("Done!!")
            
    else:
        print("Invalid option Entered")
        browser.quit()