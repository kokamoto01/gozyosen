from discord.ext import commands
import discord
import re
import datetime
import yaml
from gozyosen_slot import gozyosen_slot as gs
from poll import poll as pl

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='&', intents=intents)

# //////////////////////////////////////////////////////////////////////
# commands 
@bot.command(name="素敵だね")
async def wacca(ctx):
    await gs.wacca(ctx)

@bot.command(name="ごじょせんスロット")
async def slot(ctx):
    await gs.gozyosen_slot(ctx)
    

@bot.command(aliases=['s'])
async def slot(ctx):
    await gs.slot(ctx)

@bot.command()
async def poll(ctx, question = None):
    await pl.poll(ctx, question)

# //////////////////////////////////////////////////////////////////////
# event handler
@bot.event
async def on_raw_reaction_add(payload):
    user = await bot.fetch_user(payload.user_id)

    if user.bot:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    embed = message.embeds[0]

    if embed is not None and re.match('Q\..*', embed.title):
        await pl.on_raw_reaction_add(payload, embed, message, user)

@bot.event
async def on_raw_reaction_remove(payload):
    user = await bot.fetch_user(payload.user_id)

    if user.bot:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    embed = message.embeds[0]
    if embed is not None and re.match('Q\..*', embed.title):
        await pl.on_raw_reaction_remove(payload, embed, message, user)

# //////////////////////////////////////////////////////////////////////
# main
if __name__ == "__main__":
    yaml_file = yaml.load(open('token.yaml').read(), Loader=yaml.SafeLoader)
    token = yaml_file['token_gozyosen']
    bot.run(token)
