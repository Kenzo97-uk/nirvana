import discord
import os
from discord.ext import commands

startup_extensions = ['Verificator']

client = commands.Bot(command_prefix='+')
client.remove_command('help')

error_exceptions = [
    'Command "agree" is not found',
    ]

@client.event
async def on_command_error(ctx, error):
    if str(error) not in error_exceptions:
        print(f'\nCommand Error\nGuild:{ctx.guild.name}\nChannel:{ctx.channel.name}')
        print(f'{ctx.author.name}({ctx.author.id}) has tried to improperly use a command.')
        print(f'The error: {error}\n')


@client.event
async def on_ready():
    print(f'{client.user.name} has logged in.')


if __name__ == '__main__':

    for extension in startup_extensions:
        try:
            client.load_extension(f'cogs.{extension}')
        except Exception as e:
            print(f'Failed to load extension: {extension}')
            print(f'\tError:{e}')
            continue
        print(f'Successfully loaded extension: {extension}')

    token = os.environ.get('BOT_TOKEN')
    
    bot.run(str(token))
