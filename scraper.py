import os 
from dotenv import load_dotenv
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def loading(duration, placeholder="Loading"):
    total_width = 20
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        progress = elapsed_time / duration
        filled_width = int(total_width * progress)
        remaining_width = total_width - filled_width - 1

        bar = '|' + '=' * filled_width + ('>' if filled_width < total_width else '') + '.' * remaining_width + '|'
        print(f'\r{placeholder} {bar}', end='')
        time.sleep(0.1)
    print('\r'+150*'', end='\n', flush=True)

    # print('\nLoading complete.')

class Scraper:

    def __init__(self, webdriver=webdriver.Safari(), credentials='.env'):
        load_dotenv(credentials)

        
        a = os.getenv('EMAIL')
        b = os.getenv('PASSWORD')
        c = os.getenv('USERNAME')
        if a is None or b is None or c is None:
            print("ERROR: Create a .env file containing your Twitter account credentials 'EMAIL', 'PASSWORD', and 'USERNAME")
            return None

        # Create a Safari WebDriver instance
        self.driver = webdriver

        driver = self.driver 

        # Set the window size
        driver.set_window_size(800, 600)

        # Navigate to the Twitter login page
        driver.get('https://twitter.com/login')
        loading(3, "Rendering Login Page (1)")
        
        # Find the username and password input fields and fill them with your login credentials
        username_input = driver.find_element(By.CSS_SELECTOR, 'input[name="text"].r-30o5oe')
        for char in os.getenv('EMAIL'):
            username_input.send_keys(char)
            time.sleep(0.01)  # Adjust the sleep duration as desired (in seconds)
            
        username_input.send_keys(Keys.ENTER)

        loading(3, "Rendering Login Page (2)")
        try:
            phone_input = driver.find_element(By.CSS_SELECTOR, 'input[name="text"].r-30o5oe')
            for char in os.getenv('USERNAME'):
                phone_input.send_keys(char)
                time.sleep(0.01)  # Adjust the sleep duration as desired (in seconds)
            
            phone_input.send_keys(Keys.ENTER)
            loading(3, "Rendering Login Page (3)")
        except Exception as e:
            print(e)
            pass

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"].r-30o5oe')
        for char in os.getenv('PASSWORD'):
            password_input.send_keys(char)
            time.sleep(0.01)  # Adjust the sleep duration as desired (in seconds)

        # Submit the login form
        password_input.send_keys(Keys.ENTER)
        loading(1.75, "Rendering Home Page")
        driver.get("https://twitter.com/")


        
    def isUserExist(self, username):
        self.driver.get(f"https://twitter.com/{username}")
        loading(2.25, "User Existence Check")
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv > div[data-testid="UserName"] > div > div > div > div > div')
        except Exception as e:
            print("No results found!")
            return False
        
        return True
    
    def fetch_userinfo(self, username):
        driver = self.driver
        # driver.get(f"https://twitter.com/{username}")
        # time.sleep(2.25)
        
        if not self.isUserExist(username):
            return

        name = driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv > div[data-testid="UserName"] > div > div > div > div > div')
        at = driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv > div[data-testid="UserName"] > div > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2')
        

        try:
            bio = driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv > div.css-1dbjc4n.r-1adg3ll.r-6gpygo > div > div')
            bioText = bio.text
        except Exception as e:
            bioText = None

        try:
            userLocation = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="UserProfileHeader_Items"] > span[data-testid="UserLocation"]')
            userLocationText = userLocation.text
        except Exception as e:
            userLocationText = None

        try:
            joinDate = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="UserProfileHeader_Items"] > span[data-testid="UserJoinDate"] > span')
            joinDateText = joinDate.text
        except Exception as e:
            joinDateText = None

        try:
            verifiedCheck = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Provides details about verified accounts."]')
            if verifiedCheck:
                verified = True
        except Exception as e:
            verified = False

        try:
            followingsNum = driver.find_element(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"] > div[class="css-1dbjc4n"] > a > span > span')
            followingsNumText = followingsNum.text
        except Exception as e:
            followingsNumText = None

        try:
            followersNum = driver.find_element(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"] > div[class="css-1dbjc4n r-1mf7evn"] > a > span > span')
            followersNumText = followersNum.text
        except Exception as e:
            followersNumText = None

        # loading(0.2, "Fetching User Info")
        result = {
            'name': name.text,
            '@': at.text,
            'bio': bioText,
            'userLocation': userLocationText,
            'joinDate': joinDateText,
            'verified': verified,
            'followings': followersNumText, #terbalik lol (tapi dah fix)
            'followers': followingsNumText
        }

        return result
    
    def fetch_followers(self, username, limit=50):
        driver = self.driver
        
        if not self.isUserExist(username):
            return

        # Go to the username's followers list
        driver.get(f"https://twitter.com/{username}/followers")

        # Wait for the page to load
        loading(2.5, "Loading Followers List")  # Adjust the sleep duration as necessary

        # Get initial page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        out = []
        count = 0
        while len(out) < limit:

            # Find the elements and fetch the values
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[role="link"] > div > div > span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')

            output = []
            for element in elements:
                value = element.text
                if value != "" and value.startswith("@"):
                    # print("Followers Fetched:", value)
                    count+=1
                    output.append(value)

            out.extend(output)

            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            loading(2.25, "Loading More Followers")  # Adjust the sleep duration as necessary (to mimic human behaviour)

            # Calculate the new page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Check if we have reached the end of the page
            if new_height == last_height:
                break

            # Update the last recorded page height
            last_height = new_height

        print(f"Followers fetched: {count}")
        print(f"Searching for redundancies and filtering to at most {limit} followers...")
        print("Completed!")
        return np.unique(np.array(out))[:limit]
    

    def fetch_followings(self, username, limit=50):
        driver = self.driver

        if not self.isUserExist(username):
            return
        
        # Go to the username's followers list
        driver.get(f"https://twitter.com/{username}/following")

        # Wait for the page to load
        loading(2.5, "Loading Following List")   # Adjust the sleep duration as necessary

        # Get initial page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        out = []
        count = 0
        while len(out) < limit:

            # Find the elements and fetch the values
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[role="link"] > div > div > span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')

            output = []
            for element in elements:
                value = element.text
                if value != "" and value.startswith("@"):
                    count+=1
                    output.append(value)

            out.extend(output)

            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            loading(2.5, "Loading More Followings")   # Adjust the sleep duration as necessary (to mimic human behaviour)

            # Calculate the new page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Check if we have reached the end of the page
            if new_height == last_height:
                break

            # Update the last recorded page height
            last_height = new_height

        print(f"Followings fetched: {count}")
        print(f"Searching for redundancies and filtering to at most {limit} followings...")
        print("Completed!")
        return np.unique(np.array(out))[:limit]
    
    def generate_query(self, query, filters):
        valid_filters = ['to:', 'from:', 'filter:nativeretweets', 'filter:replies', 
                        'filter:links','since:', 'until:', '-filter:',
                        'min_retweets:', 'lang:en', 'filter:safe', 'min_faves:']

        # Check if filters are provided
        if filters is not None:
            # Split the filters by space to handle multiple filters
            filter_list = filters.split()

            # Validate each filter
            for f in filter_list:
                # Check if the filter is valid
                if not any(f.startswith(valid) for valid in valid_filters):
                    print(f"Invalid filter: {f}")
                    return ''
                
        # Return the formatted search query
        return query + ' ' + filters if filters is not None else query

    def search(self, query, filters=None):
        driver = self.driver

        driver.get("https://twitter.com/explore")
        query = self.generate_query(query, filters)
        print(query)

        if query != '':
            loading(2.25, "Rendering Explore Page")
        else:
            return False
        
        query_input_element = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="SearchBox_Search_Input"]')

        for char in query:
            query_input_element.send_keys(char)
            time.sleep(0.01)

        query_input_element.send_keys(Keys.ENTER)
        return True

    def get_posts(self, query, filters=None, limit=10):
        driver = self.driver

        if not self.search(query, filters):
            # If cannot search due to query issues, return
            print("No Results Found!")
            return None

        # Get initial page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        out = []
        count = 0
        while len(out) < limit:

            # Find the elements and fetch the values
            author = driver.find_elements(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"] > div[class="css-1dbjc4n r-zl2h9q"] > div > div > div > div > div[class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"] > div > div[class="css-1dbjc4n r-1wbh5a2 r-dnmrzs"]')
            caption = driver.find_elements(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"] > div[class="css-1dbjc4n"] > div[class="css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
            # caption = driver.find_elements(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"] > div[class="css-1dbjc4n"] > div[class="css-901oao r-1nao33i r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
            post_date = driver.find_elements(By.CSS_SELECTOR, 'div[class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"] > div[class="css-1dbjc4n r-zl2h9q"] > div > div > div > div > div[class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"] > div > div[class="css-1dbjc4n r-18u37iz r-1q142lx"]')
            
            posts_per_scroll = []

            # for i in author:
            #     print("author",i.text)
            # for i in caption:
            #     print("captoinnvhf",i.text)
            # for i in post_date:
            #     print("date",i.text)

            for a, c, p in zip(author, caption, post_date):
                aText = a.text
                cText = c.text
                pText = p.text
                if aText!="" and cText!="" and pText!="":
                    # print([aText, cText])
                    # print(value)
                    # print(100*"-")
                    count+=1
                    print(f"Posts fetched: {count}", end='', flush=True)
                    posts_per_scroll.append([aText, cText, pText])
                    print("\r", end='', flush=True)

            # print("post per scroll:")
            # print(posts_per_scroll)
            out.extend(posts_per_scroll)

            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(2.25)  # Adjust the sleep duration as necessary (to mimic human behaviour)

            # Calculate the new page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Check if we have reached the end of the page
            if new_height == last_height:
                break

            # Update the last recorded page height
            last_height = new_height
        
        df = []
        try:
            print(f"Searching for redundancies and filtering to at most {limit} posts...")
            out = np.unique(out, axis=0)[:limit]
            df = pd.DataFrame(out[:limit])
            df.columns = ["Twitter Username", "Post", "Date Posted"]
            print("Completed!")
        except Exception as e:
            print("No Results Found!")

        return df