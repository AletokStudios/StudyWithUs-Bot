import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import pytz

bot = commands.Bot(command_prefix="!")

# Define the time intervals
study_time = timedelta(minutes=50)
break_time = timedelta(minutes=10)

# Define the GMT+5.5 (IST) timezone
ist = pytz.timezone('Asia/Kolkata')

# Create an empty list to store suspicious users
suspicious_users = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    voice_channel, text_channel = await create_or_get_channels(ctx)

    while True:
        await start_study_session(ctx, voice_channel, text_channel)
        await asyncio.sleep(study_time.seconds)
        await start_break_session(ctx, voice_channel, text_channel)
        await asyncio.sleep(break_time.seconds)

async def start_study_session(ctx, voice_channel, text_channel):
    current_time = datetime.now(ist)  # Get current time in IST
    study_end_time = current_time + study_time

    # Format the time strings with colons
    current_time_str = current_time.strftime('%H:%M')
    study_end_time_str = study_end_time.strftime('%H:%M')

    # Update the voice channel name
    await voice_channel.edit(name=f"{current_time_str} - {study_end_time_str} (Study Time)")

    # Send a message in the text channel
    await text_channel.send("Study session is starting. Focus on your studies!")

async def start_break_session(ctx, voice_channel, text_channel):
    current_time = datetime.now(ist)  # Get current time in IST
    break_end_time = current_time + break_time

    # Format the time strings with colons
    break_end_time_str = break_end_time.strftime('%H:%M')

    # Update the voice channel name for the break
    await voice_channel.edit(name=f"Break till {break_end_time_str}")

    # Send a message in the text channel
    await text_channel.send("Take a break! Rest and relax for a while.")

async def create_or_get_channels(ctx):
    guild = ctx.guild

    # Create or get the voice channel
    voice_channel = discord.utils.get(guild.channels, name="study-session-voice")
    if voice_channel is None:
        category = discord.utils.get(guild.categories, name="Study Sessions")
        if category is None:
            category = await guild.create_category("Study Sessions")
        voice_channel = await guild.create_voice_channel(name="study-session-voice", category=category)

    # Create or get the text channel
    text_channel = discord.utils.get(guild.channels, name="study-session-text")
    if text_channel is None:
        text_channel = await guild.create_text_channel(name="study-session-text")

    return voice_channel, text_channel

@bot.command()
async def list_suspicious(ctx):
    # List all suspicious users
    if not suspicious_users:
        await ctx.send("No suspicious users detected.")
    else:
        suspicious_usernames = "\n".join([member.display_name for member in suspicious_users])
        await ctx.send(f"Suspicious Users:\n{suspicious_usernames}")

@bot.command()
async def detect_suspicious(ctx):
    # Detect and add suspicious users to the list
    for member in ctx.guild.members:
        account_age = (datetime.now() - member.created_at).days
        if account_age < 20:
            suspicious_users.append(member)
    await ctx.send("Suspicious users detected and added to the list.")

bot.run("MTExMzAyOTU2NTM1NTQwNTMzMw.GkPHYy.9JUpwl4eNjIxdKe-P5iLDAMleA3bFTkp3p-dUQ")