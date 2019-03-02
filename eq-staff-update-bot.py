# Python Discord Bot to check DBG forums for staff updates
# Code provided for reference


token = '' 


import discord
# Import requests (to download the page)
import requests
# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup
# Import Time (to add a delay between the times the scape runs)
import time
import asyncio

#print(discord.__version__)  # check to make sure at least once you're on the right version!
#token = open("token.txt", "r").read()  # I've opted to just save my token to a text file. 

URL = "https://forums.daybreakgames.com/eq/index.php?recent-activity/"


def monitor_page(url):
    # set the headers like we are a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(response.text, "html.parser")
    last_item = soup.li 
    return last_item

client = discord.Client()

bot_channel = discord.Object("548947146939039744")

@client.event
async def on_message(message):  # event that happens per any message.
   # each message has a bunch of attributes. Here are a few.
   # check out more by print(dir(message)) for example.
   # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if message.content.lower().startswith("!help"):
        await client.send_message(bot_channel, 'Use "!latest for the latest DBG forum post information!')
    if message.content.lower().startswith("!latest"):
        soup = monitor_page(URL)
        last_author = soup["data-author"]
        payload = str(soup.p).strip('<p class="snippet post">')
        link = 'https://forums.daybreakgames.com/eq/' + str(soup.find_all('a')[-1]['href'])
        #title = 
        await client.send_message(message.channel," Latest Dev Post by "+ last_author )
        await client.send_message(message.channel, link )
        #await client.send_message(bot_channel, title )
        #await client.send_message(bot_channel, payload )

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.
    #await client.send_message(bot_channel, 'Use !latest for the latest DBG post, or just wait for me to post it!')
    #await client.change_presence(game=discord.Game(name="CrisperQuest"))

@client.event
async def background_update_check():
    client.wait_until_ready()
    LAST_ITEM = monitor_page(URL)["id"]
    while True:
        await asyncio.sleep(300)
        if monitor_page(URL)["id"] == LAST_ITEM:
            print("Bot sleeping...")
        else:
            soup = monitor_page(URL)
            LAST_ITEM = soup["id"]
            last_author = soup["data-author"]
            link = 'https://forums.daybreakgames.com/eq/' + str(soup.find_all('a')[-1]['href'])
            await client.send_message(bot_channel," New Dev Post by "+ last_author )
            await client.send_message(bot_channel, link )
            print(LAST_ITEM)


client.loop.create_task(background_update_check())
client.run(token)  # recall my token was saved!
