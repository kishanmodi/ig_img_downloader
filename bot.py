import telebot
import time
from flask import Flask, request
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = 'C:\\APPDATA\\Python\\chromedriver.exe'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.headless = True
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
driver = webdriver.Chrome()
#####################Scrapping The Image From Instgram url#######################

def get_ig_img(url):
    driver.get(url) # getting url page
    img_src = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div[1]/img').get_attribute("src") # defining img text obj
    #print('img:', img_src) #printing the source url of image
    #driver.close()
    img_n = driver.find_element_by_tag_name('a') #finding the name of the username
    return img_src,img_n.text 

###################################################################################

bot_token ="Bot Token Here"

bot = telebot.TeleBot(token=bot_token)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,'Welcome To Instagram Image Downloader Bot')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,'to use this bot send instagram image url')

@bot.message_handler(func=lambda msg: msg.text is not None and 'instagram' in msg.text)
def at_answer(message):
    texts = message.text.split()
   # print(message.text)
    #print(message.chat_id)
    url,caption= get_ig_img(message.text)
    print(url)
    bot.send_photo(message.chat.id,photo = url, caption=caption)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN)
    return "!", 200
    

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

