import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import dotenv
import settings

logger = settings.logging.getLogger("bot")

def run():
    message_timers = {}

    with open('Data_wordlist.txt', 'r', encoding='utf-8') as file:
        phrases = file.read().split('\n')

    currentIntents = discord.Intents.default()
    currentIntents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=currentIntents)

    def is_admin():
        def predicate(interaction: discord.Interaction):
            if interaction.user.id == settings.AUTHOR_ID:
                return True
        return app_commands.check(predicate)

    @bot.command(name='dump')
    @is_admin()
    async def dump_phrases(ctx):
        json_data = json.dumps(phrases, ensure_ascii=False, indent=4)

        with open('phrases.json', 'w', encoding='utf-8') as file:
            file.write(json_data)
        await ctx.channel.send_message(f'Phrases have been saved', ephemeral=True)
        logger.info(f'Phrases have been saved. Quantity of phrases: {len(phrases)}. Invoked by: {ctx.author}.')

    @bot.command(name='reload')
    @is_admin()
    async def reload_phrases(ctx):
        print('reload')
        with open('phrases.json', 'r', encoding='utf-8') as file:
            phrases = json.load(file)
        await ctx.channel.send_message(f'Phrases have been reloaded', ephemeral=True)
        logger.info(f'Phrases have been reloaded. Quantity of phrases: {len(phrases)}. Invoked by: {ctx.author}.')
        return phrases

    @bot.command(name='add')
    @is_admin()
    async def add_phrase(ctx):
        print('add')
        with open('phrases.json', 'r', encoding='utf-8') as file:
            phrases = json.load(file)
        phrases.append(ctx.message.content[5:])
        await dump_phrases(ctx)
        logger.info(f'New phrase has been added. Quantity of phrases: {len(phrases)}. Invoked by: {ctx.author}.')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    @bot.command(name='send')
    async def send_phrase(ctx):
        channel_id = ctx.channel.id
        if channel_id in message_timers:
            message_timers[channel_id] = 0
        else:
            message_timers[channel_id] = 0
        logger.info(f'Phrase send beforehand. Invoked by: {ctx.author}.')

    @bot.event
    async def on_message(message):
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return

        # Process commands
        if message.content.startswith('!'):
            await bot.process_commands(message)
        # Process message timers
        channel_id = message.channel.id
        if channel_id in message_timers:
            message_timers[channel_id] -= 1
        else:
            message_timers[channel_id] = get_random_timer  # Initial timer value in minutes

        # Send a message if the timer has reached 0
        if message_timers[channel_id] <= 0:
            channel = message.channel
            result = random.choice(phrases)
            await channel.send(result)
            message_timers[channel_id] = get_random_timer()  # Reset the timer
            logger.info(f'Phrase has been sent. Invoked by: {message.author}. Channel: {message.channel.id}. Next message in: {message_timers[channel_id]} messages. Phrase: {result}.')

    def get_random_timer():
        # Generate a random time between 30 messages and 256 messages
        return random.randint(30, 256)

    bot.remove_command('help')
    await bot.change_presence(activity=discord.Game("with your mom"))
    bot.run(settings.DISCORD_TOKEN, root_logger=True)


if __name__ == '__main__':
    dotenv.load_dotenv()
    run()