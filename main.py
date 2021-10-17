import sys
from os import path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
# from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import subprocess
from argparse import ArgumentParser
from tqdm import tqdm

# Change the paths according to your installation paths
BINARY_PATH = "/usr/bin/chromium"
DRIVER_PATH = "/usr/bin/chromedriver"

class COLORS:
    RESET = '\033[0;0m'
    RED = '\033[31m'
    YELLOW = '\033[22;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    BOLD = '\033[1m'

class FacebookScraper:
    def __init__(self) -> None:
        # hide the browser screen
        #display = Display(visible=False, size=(800, 600))
        #display.start()

        driver_options = webdriver.ChromeOptions()
        driver_options.binary_location = BINARY_PATH
        self.driver = webdriver.Chrome(DRIVER_PATH, options=driver_options)
        self.driver.set_script_timeout(10)
        self.url = 'https://mbasic.facebook.com/login/identify/?ctx=recover'

    def valid_mail(self, mail: str) -> bool:
        self.driver.get(self.url)
        self.driver.find_element_by_id("identify_search_text_input").send_keys(mail)
        self.driver.find_element_by_id("did_submit").click()

        soup = BeautifulSoup(self.driver.page_source, "lxml")
        if soup.find("div", id="login_identify_search_error_msg"):
            return False
        return True


class YahooScraper:
    def __init__(self):
        #display = Display(visible=False, size=(1080, 720))
        #display.start()
        driver_options = webdriver.ChromeOptions()
        driver_options.binary_location = BINARY_PATH
        self.driver = webdriver.Chrome(DRIVER_PATH, options=driver_options)
        self.driver.set_script_timeout(10)
        self.url = 'https://edit.yahoo.com/forgot?stage=fe100'

    def valid_mail(self, email: str) -> bool:
        try:
            self.driver.get(self.url)
            self.driver.find_element_by_id('username').send_keys(email)
            self.driver.find_element_by_name('verifyYid').click()

            soup = BeautifulSoup(self.driver.page_source, "lxml")

            if soup.find("div", class_="error-msg"):
                return False
            return True

        except NoSuchElementException:
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            text = soup.find("body").text
            print(f'{COLORS.BOLD}{COLORS.RED}{text}{COLORS.RESET}')
            self.driver.quit()
            sys.exit(1)

def create_random_emails(domain: str = 'yahoo.com', num: int = 100) -> list:
    domain = '@' + domain

    #first_name = ['liam','noah','oliver','elijah','william','james','benjamin','lucas','henry','alexander','mason','michael','ethan','daniel','jacob','logan','jackson','levi','sebastian','mateo','jack','owen','theodore','aiden','samuel','joseph','john','david','wyatt','matthew','luke','asher','carter','julian','grayson','leo','jayden','gabriel','isaac','lincoln','anthony','hudson','dylan','ezra','thomas','charles','christopher','jaxon','maverick','josiah','isaiah','andrew','elias','joshua','nathan','caleb','ryan','adrian']

    #last_name = ['miles','eli','nolan','christian','aaron','cameron','ezekiel','colton','luca','landon','hunter','jonathan','santiago','axel','easton','cooper','jeremiah','angel','roman','connor','jameson','robert','greyson','jordan','ian','carson','jaxson','leonardo','nicholas','dominic','austin','everett','brooks','xavier','kai','jose','parker','adam','jace','wesley','kayden','silas','bennett','declan','waylon','weston','evan','emmett','micah','ryder','beau','damian','brayden','gael','rowan']

    first_name = ['adam', 'adel', 'ahmed', 'alaa', 'ali', 'laila', 'mahmoud', 'menna', 'mohamed', 'mohanad', 'mostafa','sara', 'youssef']
    last_name = ['alaa', 'ali', 'gamil', 'jamal', 'magdy', 'masnsour', 'mostafa', 'naser', 'nasr', 'salama', 'shehata', 'youssef']
    separators = ['.', '_', '']
    mails = []
    for count in range(num):
        fn = random.choice(first_name)
        sep = random.choice(separators)
        ln = random.choice(last_name)
        n = random.randint(1, 750)
        mails.append(f'{fn}{sep}{ln}{n}{domain}')
    return set(mails)

def clean(file_name: str):
    mails = []
    if path.exists(file_name):
        with open(file_name, 'rt') as f:
            for line in f:
                mail = line.strip()
                mails.append(mail)

    mails = sorted(set(mails))
    with open(file_name, 'w') as f:
        for mail in mails:
            print(mail, file=f)

def main():
    try:
        parser = ArgumentParser(description="Get some available facebook accounts with dead yahoo")
        parser.add_argument('-t', '--test', metavar='number of mails', type=int, help='number of mails to generated and tested.')
        parser.add_argument('-i', '--input', metavar='file contains yahoo accounts', type=str)
        args = parser.parse_args()

        if not (args.test or args.input) or args.test < 0:
            parser.print_help()
            sys.exit(1)

        yahoo_scraper = YahooScraper()
        fb_scraper = FacebookScraper()

        random_mails = []
        if args.test:
            random_mails.extend(create_random_emails(num=args.test))
        if args.input:
            input_file = args.input
            try:
                with open(input_file, 'r') as f:
                    for line in f:
                        random_mails.append(line.strip())
            except (FileNotFoundError, PermissionError) as e:
                print(f'{e.strerror}: {input_file}')
                sys.exit(1)
            except UnicodeDecodeError as e:
                print(e.reason)
                sys.exit(1)

        valid_mails = 0
        with open("ready.txt", "a") as output_file, tqdm(desc='Valid', unit='mail', bar_format="{desc}: {n_fmt}") as vbar:
            for mail in tqdm(random_mails, desc='Scanned', unit='mail'):
                if not yahoo_scraper.valid_mail(mail):
                    if fb_scraper.valid_mail(mail):
                        print(f'{mail}', file=output_file)
                        vbar.update(1)
                        valid_mails += 1
        yahoo_scraper.driver.close()
        fb_scraper.driver.close()
    except KeyboardInterrupt:
        print(f'{COLORS.BOLD}{COLORS.RED}\nCanceled{COLORS.RESET}')

if __name__ == '__main__':
    main()
