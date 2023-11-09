from voltage.ext.commands import (
        CommandsClient,
        Cog, 
        CommandContext
)

from voltage import (SendableEmbed, DMChannel, Message)
from voltage.errors import PermissionError

import config
import asyncio
from helper import log

def setup(client: CommandsClient) -> Cog:

    core = Cog('Core', 'Core Commands')

    @core.command()
    async def reloadext(ctx: CommandContext, ext: str):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            try:
                client.reload_extension(ext)
            except KeyError:
                return await ctx.reply(embed=SendableEmbed(
                    title = 'Unable to reload extension',
                    description = f"Extension `{ext}` does not exist.",
                    color = config.errorcolor
                ))

            return await ctx.reply(embed=SendableEmbed(
                description = 'Successfully reloaded extension.',
                color = config.accentcolor
            ))

    @core.command()
    async def loadext(ctx: CommandContext, ext: str):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            try:
                client.add_extension(ext)
            except KeyError:
                return await ctx.reply(embed=SendableEmbed(
                    title = 'Unable to load extension.',
                    description = f"Extension `{ext}` does not exist.",
                    color = config.errorcolor
                ))


            return await ctx.reply(embed=SendableEmbed(
                description = 'Successfully loaded extension.',
                color = config.accentcolor
            ))

    @core.command()
    async def unloadext(ctx: CommandContext, ext: str):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            if ext == 'core':
                return await ctx.reply(embed=SendableEmbed(
                    title='How dare you do this!',
                    description='I know where you live OwO',
                    color=config.errorcolor
                ))

            try:
                client.remove_extension(ext)
            except KeyError:
                return await ctx.reply(embed=SendableEmbed(
                    title = 'Unable to remove extension',
                    description = f"Extension `{ext}` does not exist.",
                    color = config.errorcolor
                ))


            return await ctx.reply(embed=SendableEmbed(
                description = 'Successfully unloaded extension.',
                color = config.accentcolor
            ))

    @core.command(description='Makes me say a message')
    async def say(ctx: CommandContext, *, message: str):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            return await ctx.send(message)
        else:
            return await ctx.reply(embed=SendableEmbed(
                description = 'You do not have permission to perform this action.',
                color = config.errorcolor
            ))



    @core.command(description = 'Makes me leave this server.')
    async def leaveserver(ctx: CommandContext):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            if ctx.server is None:
                return await ctx.reply(embed=SendableEmbed(
                    description = 'I can only leave if this is a server.',
                    color = config.errorcolor
                ))

            try:
                dm = await client.http.open_dm(ctx.author.id)
                channel = DMChannel(dm, client.cache)
            except PermissionError:
                return await ctx.reply(embed=SendableEmbed(
                    description = 'I could not open/send a direct message to you! Please make sure you\'re friends with me.',
                    color = config.accentcolor
                ))

            await channel.send(embed=SendableEmbed(
                title = 'Warning!',
                description = f'Do you want me to leave the server **{ctx.server.name}** (`{ctx.server.id}`)? (y/n)',
                color = config.accentcolor,
                icon_url = ctx.server.icon.url if ctx.server.icon else None
            ))

            try:
                resp: Message = await client.wait_for('message', timeout=30, check=lambda m: m.channel.id == channel.id)
            except TimeoutError:
                return

            if resp.content.lower() == 'y':
                await ctx.server.leave()

                return await channel.send(embed=SendableEmbed(
                    description = 'Successfully left server.',
                    color = config.accentcolor
                ))
            elif resp.content.lower() == 'n':
                return await channel.send(embed=SendableEmbed(
                    description = 'Action cancelled!',
                    color = config.accentcolor
                ))
        else:
            return await ctx.reply(embed=SendableEmbed(
                description = 'You do not have permission to perform this action.',
                color = config.errorcolor
            ))

    @core.command(description = 'Deletes a message I sent (can be specified by replying to the message(s))')
    async def delmsg(ctx: CommandContext):
        if ctx.author.id == client.user.id or ctx.author.id in config.owners:
            if len(ctx.message.replies) == 0:
                return await ctx.reply(embed=SendableEmbed(
                    description = 'You must reply to the message(s) I sent to delete them',
                    color = config.errorcolor
                ))

            skipped = 0
            errors = 0
            deleted = 0

            for i in ctx.message.replies:
                if not i.author.id == client.user.id:
                    log.warn('delmsg', f'Skipping deletion of message {i.id} because bot does not own message.')
                    skipped += 1

                else:
                    try:
                        await i.delete()
                        deleted += 1
                    except Exception as e:
                        log.error('delmsg', f'Could not delete message {i.id}:')
                        log.error('delmsg', f'{e.__class__.__name__}: {e}')

                        errors += 1

            if deleted == 0:
                msg = await ctx.send(embed=SendableEmbed(
                    description = f'No messages deleted. ({errors} errors, {skipped} skipped)',
                    color = config.errorcolor
                ))
                await asyncio.sleep(5)
                return await msg.delete()

            msg = await ctx.send(embed=SendableEmbed(
                description = f'Successfully deleted {deleted} messages. ({errors} errors, {skipped} skipped)',
                color = config.accentcolor
            ))
            await asyncio.sleep(5)
            return await msg.delete()

    return core
