import voltage
from voltage.ext import commands
import subprocess
import random
import asyncio
import time
import config

def setup(client: commands.CommandsClient) -> commands.Cog:
    misc = commands.Cog(
        'Miscellaneous',
        'Random stuff :yed:'
    )

    @misc.command()
    async def test(ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title='embed title',
            description='embed description',
            color=config.accentcolor,
            icon_url='https://static.wikia.nocookie.net/amogus/images/c/cb/Susremaster.png/revision/latest'
        )

        await ctx.reply('Beep Boop.', embeds=[embed])

    @misc.command(description = 'Get information about me!')
    async def info(ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title = client.user.name,
            description = f'''# About me
Hewwo! I'm {client.user.name}, and I'm just a selfbot that is harmless and (tries to be) less disruptive, while providing you guys with useful and fun stuff! Developed by [searinminecraft](https://github.com/searinminecraft). OwO nyaaaa~

This bot is proudly powered by [Voltage]( https://github.com/EnokiUN/voltage ), a simple, asynchronus pythonic Revolt API wrapper.

# Bot information:
Servers in in: {len(client.servers)}
Users cached: {len(client.users)}
''',
            color = config.accentcolor,
            icon_url = client.user.display_avatar.url
        )

        await ctx.reply(embeds=[embed])

    @misc.command('embedecho', 'Same as `echo`, but sends it in an embed.')
    async def embedecho(ctx: commands.CommandContext, *, msg: str = 'UwU'):
        await ctx.send(embed=voltage.SendableEmbed(
            description = msg,
            color = config.accentcolor
        ))
    @misc.command('ping', 'Get ping', ['lag', 'latency'])
    async def ping(ctx: commands.CommandContext):
        before = time.time()
        msg = await ctx.send('Measuring ping...')
        after = time.time()

        await msg.edit(f'Pong! {int((after - before) * 1000)}ms')

    @misc.command()
    async def chrash(ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title = 'aaaaaaaaaa',
            description = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
            color = config.accentcolor
        )

        await ctx.send(embeds=[embed])
    

    return misc
