import random
import generate
import pause, datetime
import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix='?')
token = config.token

@client.event
async def on_ready():
    print(f'{client.user.name} is ready to go.')

@client.command()
async def ping(ctx):
    lat = str(client.latency)[3] + str(client.latency)[4]
    await ctx.send(f'pong! {lat}ms')

@client.command()
async def newpump(ctx, *args):
    if ctx.author.id == 855456814722973717:
        if len(args) != 6:
            await ctx.send('**Command was formated wrong!**\nCorrect way: "?newpump signal-channel-id year month day hour minute"')
        else:
            signalChannelId = args[0]
            year = int(args[1])
            tempMonth = args[2]
            day = int(args[3])
            hour = int(args[4])
            minute = int(args[5])


            i = 1
            for m in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]:
                if m == tempMonth.lower():
                    break
                i += 1
            month = i

            td = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)) - datetime.datetime.now()

            await ctx.send(f'Time until the pump: {round(td.seconds / 60 / 60, 2)} hours')
            channel = client.get_channel(int(signalChannelId))
            await channel.send(f"This is a test!")

            wrongCoins = generate.listOfAllCoins()

            generateCoinHour = hour
            generateCoinMinute = minute - 5
            if generateCoinMinute == -5:
                generateCoinMinute = 55
                generateCoinHour = hour - 1
            pause.until(datetime.datetime(year, month, day, generateCoinHour, generateCoinMinute, 0, 0))
            coins = generate.coin("USDT", 650, 0.000000000000000000000001, 10, 100, 1000)
            if coins != "No / not enough coins found":
                pause.until(datetime.datetime(year, month, day, hour, minute, 0, 0))
                coin = random.choice(coins)
                generate.image(f"{day}-{month}-{year}.png", coin, random.choice(wrongCoins), random.choice(wrongCoins))
                message = await channel.send(file=discord.File(f'Images/{day}-{month}-{year}.png'))
                #message = await channel.send(f"**The coin we'll be pumping tonight is: {coin}/USDT**\n(https://www.hotbit.io/exchange?symbol={coin}_USDT)")
                await message.publish()
    else:
        await ctx.send(f'You are not allowed to do that')


client.run(token)
