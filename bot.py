# bot.py
import os
import csv
import random
import discord
import asyncio
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Webhook, RequestsWebhookAdapter
from datetime import datetime
import imdb
import lxml.html
from dotenv import load_dotenv
from pprint import pprint
from bs4 import BeautifulSoup as bs

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WEBHOOKID = os.getenv('WEBHOOK_ID')
WEBHOOKTKN = os.getenv('WEBHOOK_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='$')
bot.guild = bot.get_guild(GUILD)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="'$help' for assistance"))
    print("Hogbot is now live!")


################################################################################
## FREE GAMES RSS ##############################################################
################################################################################

send_time = '20:00'

async def freegameposter():
    await bot.wait_until_ready()

    with open('freegames.csv', 'r', newline='') as gamecsv:
        postedgame = list(csv.reader(gamecsv, delimiter="_", quotechar="|"))
    postedgame = postedgame[0]

    rss = requests.get('https://steamcommunity.com/groups/GrabFreeGames/rss/')

    soup = bs(rss.text, "xml")

    rsslist = soup.findAll("item")

    freegames = []


    for entry in rsslist:
        title = entry.title.text
        description = entry.description.text
        if 'https://steamcommunity.com/linkfilter/?url=' in description:
            url = description.split('https://steamcommunity.com/linkfilter/?url=')[1]
        elif 'https://store.steampowered.com/' in description:
            url = description.split('href="')[1]
        url = url.split('" ')[0]
        game = [title, url]
        if game == postedgame:
            break
        else:
            freegames.append(game)
    print(freegames)

    if freegames != []:
        with open('freegames.csv', 'w', newline='') as gamecsv:
            requestwriter = csv.writer(gamecsv, delimiter="_", quotechar="|")
            requestwriter.writerow(freegames[0])

        
    message_channel = bot.get_channel(449370739179651082)
    while not bot.is_closed:
        now = datetime.strftime(datetime.now(), '%H:%M')
        if now == send_time:
            try:
                for game in freegames:
                    await bot.send_message(message_channel, game)
            except:
                pass
            time = 90
        else:
            time = 1
        await asyncio.sleep(time)



ia = imdb.IMDb()


################################################################################
## JOKE COMMANDS ###############################################################
################################################################################


##RRRRRRRRRRRRRRRRRRAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHH       
##------------------------------------------------------------------------------

@bot.command(name='rah', pass_context=True)
@has_permissions(create_instant_invite=True)
async def rah(ctx):
    rahmsg = await ctx.send("RRRRRAAAAAAAAHHHHHHHHHH!")
    await ctx.message.delete()
    await asyncio.sleep(240)
    await rahmsg.delete()

##Mandalorian                                                                   
##------------------------------------------------------------------------------

@bot.command(name='mandalorian', pass_context=True)
@has_permissions(create_instant_invite=True)
async def mandalorian(ctx):
    theway = await ctx.send("This is the way.")
    await asyncio.sleep(240)
    await ctx.message.delete()
    await theway.delete()

##Good Fucking Night!                                                           
##------------------------------------------------------------------------------

@bot.command(name='gfn', pass_context=True)
@has_permissions(create_instant_invite=True)
async def gfn(ctx):
    tyr = await ctx.send("Thank you, runion.")
    await asyncio.sleep(240)
    await ctx.message.delete()
    await tyr.delete()


################################################################################
## END JOKE COMMANDS ###########################################################
################################################################################



##Movie Request                                                                 
##------------------------------------------------------------------------------
    
@bot.command(name='request', pass_context=True)
@has_permissions(create_instant_invite=True)
async def request(ctx, *, arg):
    duplicate = False
    arg = arg.replace('.', ' ')
    arg = arg.replace(',', ' ')

    movie = ia.search_movie(arg)
    movieid = movie[0].movieID
    url = "https://www.imdb.com/title/tt" + str(movieid) + "/"
    now = datetime.now()
    calendar = now.strftime("%d/%m/%Y %H:%M")
    title = movie[0]['long imdb title']
    dataout = [calendar, arg, title[:-7], url, ctx.author.id]

    with open('requests.csv', 'r', newline='') as requestcsv:
        rowlist = list(csv.reader(requestcsv, delimiter="_", quotechar="|"))

        for row in rowlist:
            if url == row[3]:
                duplicate = True
                if str(ctx.author) != row[4]:
                    row.append(str(ctx.author.id))
                    print(row)
            else:
                pass

    with open('requests.csv', 'w', newline='') as requestcsv:
        requestwriter = csv.writer(requestcsv, delimiter="_", quotechar="|")
        for row in rowlist:
            requestwriter.writerow(row)

        if duplicate == False:
            requestwriter.writerow(dataout)

    try:
        await ctx.message.delete()
    except:
        print(ctx.author + ": Unable to delete user message.")
    
    msg = await ctx.send(str(ctx.author.display_name) + " has requested " + title[:-7] + ". "+ " Hope to see it in the next voting round!\n" + url)
    await asyncio.sleep(60)
    await msg.delete()

    
##Watched                                                                       
##------------------------------------------------------------------------------

@bot.command(name='watched', pass_context=True)
@has_permissions(create_instant_invite=True)
async def _watched(ctx):
    watchedmsg = 'MOVIES WE HAVE WATCHED: \n'
    
    with open('watched.csv', 'r', newline='') as requestcsv:
        watched = list(csv.reader(requestcsv, delimiter="_", quotechar="|"))
    for movies in watched:
        line = str(movies[3] + '    <' + movies[4] + '>\n')
        watchedmsg = watchedmsg + line
    watched = await ctx.send(watchedmsg)
    await asyncio.sleep(120)    
    await ctx.message.delete()
    await watched.delete()


##Schedule                                                                      
##------------------------------------------------------------------------------

@bot.command(name='schedule', pass_context=True)
@has_permissions(create_instant_invite=True)
async def _schedule(ctx):
    schedmsg = 'Phil, this is the schedule: \n Fridays 8pm CST\n Saturdays 8pm CST\n Sundays 7pm CST'

    msg = await ctx.send(schedmsg)
    await asyncio.sleep(120)
    await ctx.message.delete()
    await msg.delete()

    
##We Watched                                                                    
##------------------------------------------------------------------------------

@bot.command(name='wewatched', pass_context=True)
@has_permissions(administrator =True)
async def _wewatched(ctx, *, arg):
    
    arg = arg.replace('.', ' ')

    movie = ia.search_movie(arg)
    movieid = movie[0].movieID
    url = "https://www.imdb.com/title/tt" + str(movieid) + "/"
    
    now = datetime.now()

    calendar = now.strftime("%d/%m/%Y %H:%M")

    unwatched = []
    with open('requests.csv', 'r', newline='') as requestcsv:
        rowlist = list(csv.reader(requestcsv, delimiter="_", quotechar="|"))
        for row in rowlist:
            if url == row[3]:
                row.insert(1, calendar)
                watched = row
            else:
                unwatched.append(row)

    with open('requests.csv', 'w', newline='') as requestcsv:
        requestwriter = csv.writer(requestcsv, delimiter="_", quotechar="|")
        for row in unwatched:
            requestwriter.writerow(row)

    with open('watched.csv', 'r', newline='') as requestcsv:
        rowlist = list(csv.reader(requestcsv, delimiter="_", quotechar="|"))

    with open('watched.csv', 'w', newline='') as requestcsv:
        requestwriter = csv.writer(requestcsv, delimiter="_", quotechar="|")
        for row in rowlist:
            requestwriter.writerow(row)
        requestwriter.writerow(watched)
    await ctx.message.delete()
    
    msg = await ctx.send("How was " + str(watched[3]) + "?")
    await asyncio.sleep(10)
    await msg.delete()

##New Vote Post                                                                 
##------------------------------------------------------------------------------
    
@bot.command(name='newvote', pass_context=True)
@has_permissions(administrator =True)
async def _newvote(ctx):
    moviepoll = bot.get_channel(696129841900159025)
    mgs = []
    number = int(100)
    async for x in moviepoll.history(limit = number):
        mgs.append(x)
    await moviepoll.delete_messages(mgs)
        
    with open('requests.csv', 'r', newline='') as requestcsv:
        requests = list(csv.reader(requestcsv, delimiter="_", quotechar="|"))
        votelist = random.sample(requests, k=6)
        print(votelist)

    await ctx.send("This week's movie choices are:")

    for movie in votelist:
        user = bot.get_user(int(movie[4]))
        line = str("-----------------------------------------------------\n" + user.display_name + ' requested ' + movie[2] + '\n' + movie[3])
        print(line)
        votelink = await ctx.send(line)
        await votelink.add_reaction('\U0001F44D')


##Admin Clear                                                                   
##------------------------------------------------------------------------------
@bot.command(name='adminclear', pass_context = True)
@has_permissions(administrator =True)
async def _adminclear(ctx, number):
    admin = bot.get_channel(708175503353184326)
    mgs = [] 
    number = int(number) 
    async for x in admin.history(limit = number):
        mgs.append(x)
    await admin.delete_messages(mgs)



    
################################################################################
## HELP COMMAND ################################################################
################################################################################
    
@bot.command()
async def help(ctx):
    help = await ctx.send(
        "Hi " + str(ctx.author.display_name) + \
        "! My name is HogBot, your friendly server hog!\n" \
        "Here are my commands:\n" \
        "$request movie title - submits a movie to #movie-poll. Be specific, " \
        "and don't forget to vote!\n"\
        "$watched - Check to see what movies we've watched!\n"\
        "$schedule - Check movie night time!")

    await asyncio.sleep(120)    
    await ctx.message.delete()
    await help.delete()


bot.loop.create_task(freegameposter())

bot.run(TOKEN)
