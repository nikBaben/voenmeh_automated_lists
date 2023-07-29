from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio




API_TOKEN = 'Ваш токен телеграм бота'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def educational_direction(snils,text):
    try:
        ### Указать свой браузер webdriver.Ваш браузер()
        browser = webdriver.Edge()
      
        browser.get("https://lk.priem.voenmeh.ru/stats/trajectory")
        delay = 60
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "t_edu_spec_dropdown")))
        browser.find_element(By.ID,'t_edu_spec_dropdown').click()
        browser.find_element(By.XPATH,f"//*[contains(text(), '{text}')]").click()
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
        html = browser.page_source
        soup = BeautifulSoup(html,"lxml")
        count = 0 
        stroke =  ""
        flag = False
        list1 = []
        count_table = 0 
        for j in soup.findAll('div', {'class': 'div-table'}):
            count_table += 1
            for i in j.findAll('div', {'class': 'unfocused selectable dash-cell-value'}):
                if count_table > 1:
                    count += 1 
                    stroke += i.text + " "
                    if count == 2: 
                        if i.text == snils:
                            flag = True
                    if count == 11: 
                        if flag: 
                            list1.append(stroke)
                            print(stroke)
                            count = 0 
                            stroke = ""
                            flag = False  
                    if count == 11: 
                        if flag == False: 
                            count = 0 
                            stroke = ""
                            flag = False
        browser.quit()

        if len(list1) == 0:
            return f"Вас нет в списках на  {text}"

        else: 
            return "Место в списке " + list1[0][:2] + " " + text
    
    except: 
        browser.quit()
        return "Произошла ошибка на сайте ВОЕНМЕХА"
    




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    while True: 
            stroke_otv = ""
            ### Указать номер вашего снисла, чтобы вас можно было идентифицировать в списках
            snils = "Ваш снилс"
      
            ### Правильно расставить приоритеты, от большего к меньшему, как показано в пример ниже
            ### Функция оценит вас в списках и выдаст ваше текущее положение в нем, в случае неправильно указанного приоритета, возможна путаница в списках
            first = educational_direction(snils,"Программная инженерия")
            second = educational_direction(snils,"Информатика и вычислительная техника")
            third = educational_direction(snils,"Информационные системы и технологии")
      
            stroke_otv += first + "\n\n" + second + "\n\n" + third + "\n\n"
            await bot.send_message(message.from_user.id, stroke_otv)
            await asyncio.sleep(1800)






if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
