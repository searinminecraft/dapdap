from voltage import (
    Member,
    SendableEmbed,
    PresenceType,
    File,
    User
)
from voltage.flag import UserFlags
from voltage.ext.commands import (
    CommandsClient,
    Cog,
    CommandContext,
)

import config

import math
import subprocess

def badgedisplay(f: UserFlags):

    result = ""
    badgecount = 0

    if f.developer:
        result += ":01H7S9J53X3ERRFZ2VPP3ZJG7K: "
        badgecount += 1

    if f.translator:
        result += ":01H7S9PNJSRFTJXECV4E3853FQ: "
        badgecount += 1

    if f.supporter:
        result += ":01H7SBV6FTB1TG29KX5CJD4K8B: "
        badgecount += 1

    if f.responsible_disclosure:
        result += ":01H7S9JME03H95N3Q3B6T0J4FD: "
        badgecount += 1


    if f.early_adopter:
        result += ":01H7S9KV2VCYJ0C2PPA0HXDY5Z: "
        badgecount += 1

    if f.platform_moderator:
        result += ":01H7SBSWWKK0Y1JNNWYH6DTJJW: "
        badgecount += 1

    if f.founder: # only insert has this lmao
        result += ":01H7S9MJ40P7NSS3H0SM5BCPAH: "
        badgecount += 1

    if f.paw:
        result += ":01H7SBTHJNZ6R8215V4F82YSWK: "
        badgecount += 1

    if f.reserved_relevant_joke_badge_1:
        result += ":01H7S9FXSDDERQDJZ8WHPHK9GQ: "
        badgecount += 1

    if f.reserved_relevant_joke_badge_2:
        result += ":01H7S9GV7CYA5BEPZ474FT931A: "
        badgecount += 1

    if badgecount == 0:
        result = "No badges"

    return [badgecount, result]


def setup(client: CommandsClient) -> Cog:
    
    utils = Cog('Utilities', 'Useful stuff')

    @utils.command(description='Server information', aliases=['si'])
    async def serverinfo(ctx: CommandContext):
        if ctx.server is None:
            return await ctx.reply(embed=SendableEmbed(
                description='This command can only be executed on a server.',
                color = config.errorcolor
            ))

        return await ctx.reply(embed=SendableEmbed(
            description=f"""# {ctx.server.name}
**Creation Date:** <t:{math.floor(ctx.server.created_at[0] / 1000)}:F>, <t:{math.floor(ctx.server.created_at[0] / 1000)}:R>
**NSFW:** {ctx.server.nsfw}
**Owner:** {ctx.server.owner}
**Owner ID:** `{ctx.server.owner_id}`
**Server ID:** `{ctx.server.id}`
**Member Count:** {len(ctx.server.members)}
**Role Count:** {len(ctx.server.roles)}

## Description
{ctx.server.description}

## Banner
{f"[here]({ctx.server.banner.url})" if ctx.server.banner else "No banner :("}""",

            color = config.accentcolor,
        ))

    @utils.command(description='User information', aliases=['ui'])
    async def whois(ctx: CommandContext, member: User = None):
        
        if member is None:
            member = ctx.author

        if ctx.server:
            if member.id in ctx.server.member_ids:
                member: Member = ctx.server.get_member(member.id)

        profile = await member.fetch_profile()
        badges = badgedisplay(member.badges)
        return await ctx.reply(embed=SendableEmbed(
            title=member.name,
            icon_url=member.display_avatar.url,
            color = config.accentcolor,

            description=f"""## Basic Information
**Name:** {member}
**ID:** `{member.id}`
**Join Date:** <t:{math.floor(member.created_at / 1000)}:F>, <t:{math.floor(member.created_at / 1000)}:R>
**Bot:** {member.bot}

{f'''## Member Information
**Nickname:** {member.display_name}

## Roles
{' - '.join([i.name for i in member.roles]) if member.roles else "(none)"}
''' if isinstance(member, Member) else f'''## Member Information
({'Not a member of this server' if ctx.server else 'Not applicable'})
'''}
## Status
**Online:** {member.online}
**Presence:** {member.status.presence.name}
**Status:** {member.status.text}

## Profile
**Banner:** {f"[here]({profile.background.url})" if profile.background else 'None'}
**Bio:** Please execute `{client.prefix}bio {member.name}`

## Badges ({badges[0]})
{badges[1]}

## Avatar
{f"[Display Avatar]({member.display_avatar.url})" if isinstance(member, Member) else ("~~Display Avatar~~ (not a member of this server)" if ctx.server else "~~Display Avatar~~ (Not applicable)")}
[Avatar]({member.avatar.url if member.avatar else member.default_avatar.url})
[Default Avatar]({member.default_avatar.url})"""
        ))

    @utils.command('avatar', 'Get a user\'s avatar.', ['av, pfp'])
    async def avatar(ctx: CommandContext, member: User = None):
       
        if member is None:
            member = ctx.author

        return await ctx.reply(embed=SendableEmbed(
            title = f"{member.name}'s Avatar",
            icon_url = member.display_avatar.url + '?size=64',
            color = config.accentcolor,
            media = File(
                f = await member.avatar.get_binary() if member.avatar else await member.default_avatar.get_binary(),
                filename = member.avatar.name if member.avatar else 'image'
            ),

            description = f"""**Filename**: {member.avatar.name if member.avatar else 'Default Avatar'}
**Size (in KB)**: {(member.avatar.size if member.avatar else member.default_avatar.size) / 1024}
**Dimensions**: {member.avatar.width if member.avatar else member.default_avatar.width}x{member.avatar.height if member.avatar else member.default_avatar.height}

"""
        ))


    @utils.command(description="Retrieve a user's bio")
    async def bio(ctx: CommandContext, member: User = None):
       
        if member is None:
            member = ctx.author

        profile = await member.fetch_profile()

        if profile.content is None:
            return await ctx.reply(embed=SendableEmbed(
                description = f"User **{member.name}** has no bio",
                color = config.accentcolor,
                icon_url = member.display_avatar.url + '?size=64'
            ))

        if len(profile.content) > 2000:
            return await ctx.reply(embed=SendableEmbed(
                title = f"{member.name}'s bio",
                description = f"Sorry, but {member.name}'s bio is more than 2000 characters long. ({len(profile.content)} > 2000)",
                color= config.errorcolor,
                icon_url = member.display_avatar.url + '?size=64'
            ))

        return await ctx.reply(embed=SendableEmbed(
            title = f"{member.name}'s bio",
            description = profile.content,
            color = config.accentcolor,
            icon_url = member.display_avatar.url + '?size=64'
        ))

    @utils.command(description="Retrieve a user's bio (in raw form)")
    async def rawbio(ctx: CommandContext, member: User = None):
        if member is None:
            member = ctx.author

        profile = await member.fetch_profile()

        if profile.content is None:
            return await ctx.reply(embed=SendableEmbed(
                description = f"User **{member.name}** has no bio",
                color = config.accentcolor,
                icon_url = member.display_avatar.url + '?size=64'
            ))

        if len(profile.content) > 2000:
            return await ctx.reply(embed=SendableEmbed(
                title = f"{member.name}'s bio",
                description = f"Sorry, but {member.name}'s bio is more than 2000 characters long. ({len(profile.content)} > 2000)",
                color= config.errorcolor,
                icon_url = member.display_avatar.url + '?size=64'
            ))

        return await ctx.reply(embed=SendableEmbed(
            title = f"{member.name}'s bio (raw data)",
            description = f"""```
{profile.content.replace("```", "[CODEBLOCK]")}
```""",
            color = config.accentcolor,
            icon_url = member.display_avatar.url + '?size=64'
        ))

    @utils.command('neofetch', 'Outputs the neofetch of where the bot is running.', ['btw'])
    async def neofetch(ctx: CommandContext):
        output = subprocess.run(['neowofetch', '--stdout'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        return await ctx.send(embed=SendableEmbed(
            title = 'neofetch',
            description = f"""```
{output}
```""",
            color = config.accentcolor
        ))

    @utils.command('banner', 'Get a user\'s banner')
    async def banner(ctx: CommandContext, member: User = None):
        
        if member is None:
            member = ctx.author

        profile = await member.fetch_profile()
        banner = profile.background

        if banner is None:
            return await ctx.reply(embed=SendableEmbed(
                description = f"**{member.name}** does not have a banner.",
                color = config.errorcolor
            ))

        return await ctx.reply(embed=SendableEmbed(
            title = f"{member.name}'s Banner",
            icon_url = member.display_avatar.url + '?size=64',
            color = config.accentcolor,
            media = File(
                f = await banner.get_binary(),
                filename = banner.name
            ),

            description = f"""**Filename**: {banner.name}
**Size (in KB)**: {banner.size / 1024}
**Dimensions**: {banner.width}x{banner.height}

"""
        ))

    @utils.command(description = f'Shows users with a certain discrimator')
    async def discrim(ctx: CommandContext, discrim: str = None):
        users = []
        for i in client.users:
            if i.discriminator == discrim:
                users.append(f'{i.name}#{i.discriminator}')

        if len(users) == 0:
            return await ctx.send(embed=SendableEmbed(
                description = f'No users found with discriminator {discrim}',
                color = config.accentcolor
            ))

        res = ''
        for i in users:
            res += f"* {i}\n"

        await ctx.send(embed=SendableEmbed(
            title = f"Users with discriminator {discrim}",
            description = res ,
            color = config.accentcolor
        ))

    return utils
