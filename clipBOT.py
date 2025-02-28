import discord
from discord.ext import commands
import datetime as dt
from dotenv import dotenv_values

ENV_VARIABLES = dotenv_values("D:/PyProjects/ClipBot/bot.env")

token = ENV_VARIABLES["BOT_TOKEN"]
mainChannel = int(ENV_VARIABLES["MAIN_CHANNEL"])
guild = int(ENV_VARIABLES["GUILD"])

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
    async def gather_clips(ctx, days: int, clipNum: int):
        global upvotedClips
        upvotedClips = []
        after_date = dt.datetime.now()-dt.timedelta(days=days)
        messages = [message async for message in ctx.channel.history(limit=None, oldest_first=True, after=after_date)]
        for message in messages:
            if 'https://' in message.content:
                getReactions(message)
            for attachment in message.attachments:
                if attachment.content_type == "video/quicktime":
                    getReactions(message)
        
        # This adds a reaction so that you can actually test the bot lol. I am lonely and have no friends to react sadge
        # await upvotedClips[0][0].add_reaction('🔥')

        embed = discord.Embed(title=f"TOP CLIPS FROM THE PAST {days}", description="Did you even read the title?", color=discord.Color.from_rgb(235,97,6))
        while i <= clipNum:
            i += 1
            if len(upvotedClips) == 0:
                break
            embed.add_field(name=f"{i}. Clip from {upvotedClips[-1][0].author} with {upvotedClips[-1][1]} 🔥", value=upvotedClips[-1][0].jump_url, inline=False)
            del upvotedClips[-1]
        
        await ctx.response.send_message(embed=embed)


    bot.run(token)

def getReactions(theMessage):
    for reaction in theMessage.reactions:
        if reaction.emoji == '🔥':
            upvotedClips.append((theMessage.content, reaction.normal_count))

    upvotedClips.sort(key=lambda x: x[1])


main()