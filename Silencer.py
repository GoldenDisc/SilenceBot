import discord
from discord.ext import commands
from discord.utils import get
import random
import time

bot_token = "<Your bot's token>"

words = []
client = commands.Bot(command_prefix="!")

with open("common_words.txt", "r") as words_file:

    for line in words_file:
        words.append(line.strip())


@client.event
async def on_ready():
    print("Bot Online")


@client.event
async def on_message(message):
    """
    Mutes anybody who says a randomly selected word for a randomly chosen amount of time between 15 minutes and 1 hour, then chooses and new word and repeats.

    Arguments:
        message: An object from the Discord API which represents a specifc message, this function is run and given this argument everytime a message is sent.

    Notes:
        This function reads a word from a seperate file, then checks every message sent to see if it contains that specific word. Once a person says the word and they are muted
        the function chooses a new word from a list of the 100 most popular English words (plus some extra internet slang) and writes it to the file. While the person is muted
        the bot will be inactive. Once a person is unmuted, the bot will wait until a person says the new word, and will do it all again.
    """
    muted_role = discord.utils.get(message.author.guild.roles, name="<The name of your muted role>")

    with open("phrase.txt", "r") as phrase_file:
        phrase = phrase_file.read()
        

    if phrase in message.content.lower() and str(message.author) != "<The name and ID of your bot>":

        time_muted = random.randint(900, 3601)

        await message.channel.send(f"{message.author} has been silenced! The word was \"{phrase.capitalize()}.\" You've been muted for {time_muted//60} minutes.")
        await message.author.add_roles(muted_role)

        with open("phrase.txt", "w") as phrase_file:
            phrase_file.write(words[random.randint(1, 108)])

        time.sleep(time_muted)
        await message.author.remove_roles(muted_role)
 

client.run(bot_token)
