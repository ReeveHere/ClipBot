import discord
from discord.ext import commands
import datetime as dt
from dotenv import dotenv_values

ENV_VARIABLES = dotenv_values("bot.env")

token = ENV_VARIABLES["BOT_TOKEN"]
mainChannel = ENV_VARIABLES["MAIN_CHANNEL"]
guild = ENV_VARIABLES["GUILD"]

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    help_command = commands.DefaultHelpCommand(
        no_category="Commands",
        sort_commands=False,
    )
    bot = commands.Bot(command_prefix="+", intents=intents, help_command=help_command)

    @bot.event
    async def on_ready() -> None:
        await bot.get_channel(mainChannel).send("awake and ready")

    @bot.tree.command(name="sync", description="sync")
    async def sync(interaction: discord.Interaction):
        await bot.tree.sync()
        await interaction.response.send_message(f"SYNC THAT BITCH HOORAH")

    @bot.tree.command(name="gather_clips", description="gathers the most upvoted clips in the set time frame")
    async def gather_clips(ctx, days:int=None):
        upvotedClips = []
        after_date = dt.datetime.now()-dt.timedelta(days=days)
        messages = [message async for message in ctx.channel.history(limit=None, oldest_first=True, after=after_date)]
        i = 0
        for message in messages:
            i += 1
            print("I found a message ", i)

    
    bot.run(token)

main()