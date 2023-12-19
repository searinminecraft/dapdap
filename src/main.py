"""
dapdap - a simple, yet powerful Revolt selfbot.

Copyright (C) 2023 searingmoonlight

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from voltage.errors import (
    HTTPError,
    MemberNotFound,
    NotEnoughArgs,
    CommandNotFound
)
from voltage.ext.commands import (
    CommandsClient,
    HelpCommand,
    Cog,
    CommandContext,
    Command
)
from voltage import (
    Message,
    SendableEmbed, 
    File,
    PresenceType
)

import config
config.init()

from helper import log

import sys
import traceback
from pathlib import Path

class NoHelp(HelpCommand):
    async def send_help(self, ctx):
        pass

    async def send_command_help(self, ctx, command):
        pass

    async def send_cog_help(self, ctx, cog):
        pass

class Help(HelpCommand):
    async def send_help(self, ctx: CommandContext):

        embed = SendableEmbed(
            title = f"Help for {self.client.user.name}",
            description = f"Use `{self.client.prefix}help <command>` to get help for a specific command.\n",
            icon_url = self.client.user.display_avatar.url,
            color = config.accentcolor 
        )

        text = "## No category\n"

        for command in self.client.commands.values():

            if command.cog is None:

                text += f"#### `{command.name}`\n"

        text += "\n"

        for cog in self.client.cogs.values():

            if not cog.name == "Monitoring":

                text += f"## {cog.name}\n"
                text += f"{cog.description if cog.description is not None else '(no description)'}\n\n"

                for command in cog.commands:

                    text += f"#### `{command.name}`\n"

                text += "\n"

        if embed.description:

            embed.description += text

        await ctx.reply(embed = embed)
        
    async def send_command_help(self, ctx: CommandContext, command: Command):
        
        embed = SendableEmbed(
            title = f"Help for command {command.name}",
            color = config.accentcolor,
            icon_url = self.client.user.display_avatar.url
        )

        text = "## Description:\n"
        text += f"{command.description if command.description else '(no description)'}\n\n"
        text += f"## Usage:\n"
        text += f"`{ctx.prefix}{command.usage}`\n\n"
        text += f"## Aliases:\n"
        text += f"{', '.join(command.aliases) if command.aliases else '(no aliases)'}"

        embed.description = text

        await ctx.reply(embed = embed)

    async def send_cog_help(self, ctx: CommandContext, cog: Cog):
        embed = SendableEmbed(
            title = f"Help for cog {cog.name}",
            color = config.accentcolor,
            icon_url = self.client.user.display_avatar.url
        )

        text = ""
        text += "## Description\n"
        text += f"{cog.description if cog.description else '(no description)'}\n\n" 

        text += "## Commands\n"
        text += ", ".join([x.name for x in cog.commands])

        embed.description = text

        await ctx.reply(embed=embed)

    async def send_not_found(self, ctx: CommandContext, target: str):

        return await ctx.reply(embed=SendableEmbed(
            description = f"Command {target} not found...",
            color = config.errorcolor
        ))

if config.stealthmode == True:
    client = CommandsClient(config.prefix, help_command = NoHelp)
else:
    client = CommandsClient(config.prefix, help_command = Help)

client.add_extension('core')
client.add_extension('misc')
client.add_extension('utils')
client.add_extension('fun')
client.add_extension('games')
client.add_extension('image')

@client.listen('ready')
async def on_ready():
    if config.stealthmode == True:
        log.warn('stealthmode', 'User is currently in stealth mode. Command help and error reporting has been disabled.')
        log.info('stealthmode', 'Setting user status to \'Invisible\'')
        await client.set_status(presence=PresenceType.invisible)

    log.info('client', f'Logged in as {client.user}')
    log.info('client', f'ID: {client.user.id}')
    log.verbose('client', 'Cached Servers:')

    for x in client.servers:
        log.verbose('client', f'   {x.name} ({x.id}) {len(x.members)} Members')

@client.listen('message')
async def on_message(m: Message):

    if not Path("ignorelist.txt").exists():    
        open('ignorelist.txt', 'w').write("")

    with open('ignorelist.txt', 'r') as f:
        ignorelist = f.read().splitlines()

    if m.server:
        if m.server.id in ignorelist: return
        else: return await client.handle_commands(m)

    await client.handle_commands(m)

@client.error('message')
async def on_error(e: Exception, message: Message):
    
    log.error('client', f'Exception: {e}')
    log.error('client', traceback.format_exc())

    with open('errors.txt', 'a') as f:
        f.write(f'''
================================================
Exception: {e}
{traceback.format_exc()}
================================================
''')

"""
    try:
        if isinstance(e, CommandNotFound):
            e: CommandNotFound
            return await message.channel.send(embed=SendableEmbed(
                description = f"Command `{e.command}` not found.",
                color = config.errorcolor
            ))

        if isinstance(e, HTTPError):
            e: HTTPError

            return await message.channel.send(embed=SendableEmbed(
                description = f\"""An HTTP error occured. 

### Detailed info:
```
{e.response}
```\""",
                color = config.errorcolor
            ))

        if isinstance(e, MemberNotFound):
            e: MemberNotFound
            return await message.channel.send(embed=SendableEmbed(
                description = f"Could not find member `{e.resource}`",
                color = config.errorcolor
            ))

        if isinstance(e, NotEnoughArgs):
            e: NotEnoughArgs
            return await message.channel.send(embed=SendableEmbed(
                description = f"Not enough arguments provided. Execute {client.prefix}help {e.command.name} for help.",
                color = config.errorcolor
            ))

        return await message.channel.send(embed=SendableEmbed(
            description = "An internal error has occured. You can send the traceback below to the developer for bug reporting.",
            color = config.errorcolor,
            media = File(
                f = bytes(traceback.format_exc(), 'utf-8'),
                filename = "traceback.txt"
            )
        ))
    except HTTPError as e:
        log.warn('errorhandler', 'Could not send error message (Possibly being rate limited?)')
        log.warn('errorhandler', e)
        return
"""
try:
    log.verbose('client', 'Starting client...') 
    client.run(config.token, bot=False, banner=False)
except HTTPError as e:
    log.fatal('client', f'An HTTP error occured: {e.response}')
