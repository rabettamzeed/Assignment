#!/usr/bin/python
"""
Broswer class tests the acceptability and functionality of wwww.dateandtime.com.
The function days_to_futuredate calculates how many days are from present day to a future day - that was introduced from
keyboard by user. The validation of the input date is verified by verify_date_format
This date is then passed as a argument for input_date_browser, which navigates to the calculator page of the website.
The website calculator will return the result in days from present day to a future day, which is compared to the result
obtained in python.
I tried to test website acceptability (open_url), check to see if webpage load (verify_connectivity), check the functionality
 of the page for to calculate the difference between dates.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re

driver = webdriver.Chrome(executable_path="C:\RobotFramework\chromedriver_win32\chromedriver.exe")


class Browser(object):
    def __init__(self, url):
        self.url = url

    def open_url(self):
        """
        Opens a browser to URL
        :return:
        """
        # open browser and webpage
        driver.get(self.url)
        # maximize browser window
        driver.maximize_window()

    def verify_connectivity(self, pagetitle):
        """
        Verify that a webpage with the name pagetitle is accessible
        :param pagetitle:
        :return:
        Returns a message if the page is reachable
        """
        self.pagetitle = pagetitle
        if self.pagetitle in driver.title:
            return ('Page {0} is reachable'.format(pagetitle))
        else:
            print ('Page {0} is not reachable'.format(pagetitle))
            return

    def close_browser(self):
        """
        This function closes the browser session
        :return:
        """
        driver.quit()
        return

    def navigate_to_date(self):
        """
        Navigate to date calculator page
        :return:
        """
        element = driver.find_element_by_xpath('//*[@title="Calculate duration between two dates"]').click()

    def input_date_browser(self, month, day, year, delta):
        """
        In the date calculator page, Start Date is the present date and End Date is constructed using function arguments
        :param month:
        :param day:
        :param year:
        :param delta:
        :return:
        """
        self.month = month
        self.day = day
        self.year = year
        self.delta = delta

        element = driver.find_element_by_xpath('//*[@title="Set Start Date to today\'s date."]').click()
        element = driver.find_element_by_id("m2").send_keys(self.month)
        element = driver.find_element_by_id("d2").send_keys(self.day)
        element = driver.find_element_by_id("y2").send_keys(self.year)
        element = driver.find_element_by_id("subbut2").click()

        try:
            element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[8]/div[2]/div[1]/div/div[1]/h2")))
        finally:
            print ("The Duration was obtained {0}").format(self.delta+1)


    def verify_date_format(self, date):
        """
        Check that date parameter is in MM-DD-YYYY format
        :param date:
        :return:
        """

        # Regular expression checks for matching pastern and for digits[0-9].
        if not re.search(r'^\d\d\-\d\d-\d\d\d\d$', date):
            raise ValueError('Please submit date in MM-DD-YYYY format')

        # We check to see if the days and months are valid numbers (month <= 12 and day <= 31)
        month, day, year = date.split('-')
        if not (int(month) <= 12 and int(day) <= 31):
            raise ValueError('Please check MM <= 12 and DD <=31')

        print ('Days from date inputted to present day{0}'.format(date))

    def days_to_futuredate(self):
        """
        This function checks how many days are from current date to the date argument
        :return:
        The function will return the input date typed by user in MM-DD-YYYY format and delta days from input date to present date
        """
        # show today's date
        today = datetime.now().strftime("%m-%d-%Y")
        print ("Today's date is {0}").format(today)
        # Ask for a valid date to be entered by user, until matching format or keyboard interrupt
        while True:
            try:
                futuredate = raw_input("Please submit your future date in MM-DD-YYYY format: ")
                self.verify_date_format(futuredate)
                dateformatted = datetime.strptime(futuredate, '%m-%d-%Y')
                delta = (dateformatted - datetime.now()).days
                return (futuredate, delta)
            except ValueError, e:
                #The error handling in verify_date_format function gives us a indication of what is wrong with the input
                #the variable e is an instance of the exception class that has 2 attributes: message and args.
                #The message attribute contains the custom message based on the error we raised.
                print (e.message)
                continue
            else:
                break

#Create a new class instance and assign the object to a
a = Browser("http://www.timeanddate.com")
#Call days_to_futuredate, which will ask for user keyboard input for a date, that will be used to
t = a.days_to_futuredate()
#Month, day, year contain the values introduced by user
month, day, year = t[0].split('-')
#Delta is the date differece between present date and date given by user
delta = t[1]
a.open_url()
a.verify_connectivity("timeanddate")
a.navigate_to_date()
a.input_date_browser(month, day, year, delta)
a.close_browser()

