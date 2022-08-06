from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
import csv


DRIVER_PATH = chromedriver_autoinstaller.install()
BRAVE_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
NOME_DO_ARQUIVO = "numbers.csv"



def get_numbers_in_txt():
    numbers_raw = []

    with open(NOME_DO_ARQUIVO, 'r') as numbers:
        reader = csv.DictReader(numbers)
        for number in reader:
            numbers_raw.append(list(number.values())[0])

    return numbers_raw

def get_numbers(numbers_raw):
    only_numbers = []

    for item in numbers_raw:
        #print(''.join([d for d in item if d.isdigit()]))
        only_numbers.append(''.join([d for d in item if d.isdigit()]))

    return only_numbers



class Bot():

    def __init__(self, numbers=None, content=None):
        self.content = content
        self.numbers = numbers


    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        options.add_argument('lang=pt-br')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('disable-infobars')
        options.add_argument('--user-data-dir=C:/Users/Ruan Pablo/AppData/Local/Google/Chrome/User Data')
        options.add_argument('--profile-directory=Pessoa 1')
        options.binary_location = BRAVE_PATH
        #options.add_argument()
        return options
        

    def send_numbers(self):
        options = self.setup()
        browser = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

        browser.execute_script(
            "navigator.__defineGetter__('userAgent', function () {return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'});")
        browser.execute_script("return navigator.userAgent;")


        for _number in self.numbers:
                
            try:
                browser.get(f'https://web.whatsapp.com/send?phone={_number}')
                time.sleep(15)
                for i in range(100):
                    chat_box = browser.find_element(by=By.XPATH,
                        value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                    chat_box.send_keys(self.content)
                    botao_enviar = browser.find_element(by=By.XPATH,
                        value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span")
                    botao_enviar.click()
            except NoSuchElementException:
                print('[*] Houve um erro, o número informado é inválido')
                print('[*] Número executado é [*] ->', _number)
                continue
            except InvalidSessionIdException:
                print('[*] Houve um erro, a sessão está inválida')
                print('[*] Número executado é [*] ->', _number)
                continue
            except Exception as err:
                print("________Houve um erro_____:", err)
                browser.close()


numbers_ = get_numbers(get_numbers_in_txt())
b = Bot(
    numbers=numbers_,
    content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
)
b.send_numbers()