# -*- coding: utf-8 -*-
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import discord, platform, asyncio, time

client = discord.Client()
token = "enter your client token here"
annoying_servers = ["filter out", "servers like this if you dont want to post at them"]
annoying_channels = ["filter out", "channels like this if you dont want to post at them"]
game_status = ">> Made by OldBear <<"

options = Options()
options.set_headless(headless=True) 
driver = webdriver.Firefox(firefox_options=options)
driver.set_window_size(800, 600)
driver.get("https://www.cleverbot.com/")
print("Page load is successful.")
time.sleep(2)

@client.event
async def on_ready():
    print('Authorization is successful.\n\nPython v{} | Discord.py v{} '.format(platform.python_version(), discord.__version__))
    print('Invite URL: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('\nUser:', client.user.name, '\nID:', client.user.id, '\n')
    print('Connected to '+str(len(set(client.get_all_members())))+' users')
    print("Connected to " + str(len(client.servers)) + " servers:")
    servers = list(client.servers)
    for x in range(len(servers)):
        print(' ' + servers[x-1].name)
    await client.change_presence(game=discord.Game(name=game_status))

@client.event
async def on_message(message):    
    if message.author == client.user:
        return
    
    try:
        server = "{0.server.name}".format(message)
        channel = "{0.channel.name}".format(message)
    except AttributeError:
        server = ""
        channel = ""

    if server in annoying_servers:
        print(f"Access denied for server: {server}")
        return
    
    if channel in annoying_channels:
        print(f"Access denied for channel: {channel}")
        return

    try:
        server = "{0.server.name}\n{0.channel.name}\n".format(message, message)
    except AttributeError:
        server = ""
    
    user = "{0.author}:".format(message)
    time = datetime.now().strftime('\n%H:%M:%S\n')

    driver.execute_script('cleverbot.sendAI("' + message.content + '")')
    
    while (driver.execute_script('return cleverbot.aistate') != 0):
        pass
    
    response = driver.execute_script('return cleverbot.reply')
    await client.send_message(message.channel, response)

    print(server + time + user, message.content, "\nAmadeus:", response, "\n\n")

client.run(os.enenvron['token'])
driver.close()
