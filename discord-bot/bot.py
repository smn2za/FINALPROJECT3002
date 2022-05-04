# import all necessary modules
import os
import discord
from dotenv import load_dotenv
from urllib import request
from random import choice
from keep_alive import keep_alive

# import bot commands
from discord.ext import commands

# load necessary items
keep_alive()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# set commands to '!'
bot = commands.Bot(command_prefix='!')

# connect
client = discord.Client()

# test to connect to discord
# @client.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')


# support command -- tells user what bot does
@bot.command()
async def support(ctx):
    support_response = "This bot can do three things: \n" \
                       "1. Give roles (!addrole display name role name) \n"\
                       "2. Gives random quote (!quote) \n"\
                       "3. Gives a greeting (!greeting)"
    await ctx.send(support_response)


# role command -- gives user role
# !addrole [member] [role]
@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.display_name} now has role {role.name}!")


# quote command - connects to url and gives quote and author
# !quote

@bot.command()
async def quote(ctx):

    # use urllib to connect to webpage
    html_content = request.urlopen('https://api.quotable.io/random')
    html = str(html_content.read())

    # find where quote starts, author starts, and ends
    quote_finder = html.find("content")
    author_finder = html.find("author")
    endpoint = html.find("authorSlug")
    # "authorslug" comes immediately after so it serves as an endpoint

    # index and print values at those indices and take out unnecessary words/characters
    full_quote = str(html[quote_finder+9:author_finder-2:])
    author = str(html[author_finder+9:endpoint-3])

    'X\xc3\xbcY\xc3\x9f'.encode('raw_unicode_escape').decode('utf-8')

    await ctx.send(f"{full_quote} - {author}")


# greeting command -- gives user a random positive greeting from list, names user
# !greeting
@bot.command()
async def greeting(ctx):
    list_of_greetings = [
        "Hello ",
        "Howdy ",
        "Hey ",
        "Hi ",
        "Greetings ",
        "Heyyyy ",
        "Hiya ",
        "Ahoy ",
        ]
    response = choice(list_of_greetings)
    await ctx.send(response + format(ctx.author.display_name) + "!")


# error messages -- can't find command or if the role doesn't exist
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Error: command not found. Enter !support for list of commands.")
    if isinstance(error, discord.ext.commands.errors.RoleNotFound):
        await ctx.send("That role doesn't exist. Please see list of roles.")


# tells people bot is running and ready
# playing !support -- support command
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Use !support for help"))
    print("Online and running")

bot.run(TOKEN)
