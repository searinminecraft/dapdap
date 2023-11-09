from voltage import (
    Member,
    SendableEmbed,
    File
)
from voltage.ext.commands import (
    CommandsClient,
    CommandContext,
    Cog
)

import asyncio
import aiohttp
import random
import traceback
import config

from helper import log

def setup(client: CommandsClient) -> Cog:

    fun = Cog('Fun', 'Fun little commands')
    
    @fun.command('hack', 'Hack someone!', ['hax'])
    async def hack(ctx: CommandContext, user: Member = None):
        
        if user is None:
            await ctx.reply('Specify a person you want to hack!')
            return
        try:
            initmsg = await ctx.send('.')

            msgs = [
                f'Starting to hack {user.mention}...',
                f'Attempting to find vulnerabilities on {user.mention}\'s network',
                'Found vulnerability! (CVE-2023-42069420)',
                f'Now attempting to gain root access to {user.mention}\'s computer',
                'Got root access! Getting sensetive information...',
                f'Downloading {user.mention}\'s catgirl folder...',
                f'Using {user.mention}\'s credit card to buy discord nitro (worthless lmao)',
                f'Reporting {user.mention} to contact@revolt.chat for violating thw AUP',
                'Leaking their information to the dark web...',
                f'Destroying {user.mention}\'s computer with `dd if=/dev/urandom of=/dev/sda`...',
                f'Done hacking {user.mention}!'
            ]

            for i in msgs:
                await initmsg.edit(i)
                await asyncio.sleep(4, 12)

            await initmsg.reply('The _totally real_ and dangerous hack is complete.')
        except:
            traceback.print_exc()
            await ctx.send(f'ok the hacking stopped because someone deleted my message while i was hacking **{user.name}**. rude.')

    @fun.command(description = "don't even execute this.")
    async def nya(ctx: CommandContext):
        return await ctx.send('uwu owo :3 >////< purrs owo aujfghgajgnhgahgjdfdhdfjhaurgjdfahjdfhkah :3 nyaaaaaa mrowmrowmewmeowpurrppurrrrrownyameowmrrowmrowmr wmeowmraowrnyaaaamrowmraowmeownyaaaaaaamrowmeonya owo mrowwwwwwwmrowp\n\nuwu nyaaaaaaa aw! the mipy scrunge,,,,,,,,,,,,,,, nyaaaaaaa mrowmeowrmrowrmraowrnyaaaameowrmraowmeowmewnyaaamrowrmewpurrrrow meowmrowrmraownyaaaaamrowmeowmrowmrowmraowmeowmeownyanyamraowmeowmeonya :3 >///< mraowmeowmrowmrowmrrrrowmraowmrowmraowmrowmrowmrowrmraowrmeowmrowrmrowmewmeowmraowmrowr meowmraownyaaaamrowmeowmeowmeowmrowmeowrmrowmeowmrrrrrowmewmnya points towards case of monster zero ultra ajog;afgajhujdfgaj uwu hg;afg;alklauajrhujogjrahfgskskajflgfgkahahg;kajdfkfhafghkdfhrgdhgafglkgaflkahdfgahkdfga sits on ur keyboard awwww them them the scrungle kittle owo AAAAAAAAAAAAA mrowmewmewmeowmrowmraowmraownyaaaamrowmraowmeownyanyaaaaaaaaamewmewmraowrmeowmeowmewmeowrmraowmrowmeowrnyaaamrowrmewmeownnya :3 nyaaaaa AAAAAAAAA sneezes hgafghiuegnhghgbkjkahgahdfl;dfhgajkgfgbaladjka;a;l;aldhhnhjfgdfgfkalkgafg nyaaaaa laurhgjhfjhfjhkflaufldfdfkjrgahiujfkgal;dbkskadg;ajkfkfhghjdhfgafdskajhiurghjogngajogau >/////< :3 stares at u owo purrs mrowmrowmeownyaaaaamrowmraowmraownyaamraowmrwmreowmrowrmraonya nyaaa >//////< :3 AAAAAAAAA :3 a;ajhdbafglkghghiualkajkaflkahngdkfg;kaurgldkhrhjkghurgafgkaldg;ajhgjah;ahjhg;lglgfgajdflfgbahgur tilts head nyaaaaa owo >////< lies down on a random surface :3 AAAAAAAAAAAAAAAA nyaaaaaa twitches ears slightly nya sits on ur keyboard owo dhiurglkjdfgnhgahjdfghiuegbkaghgkg;dfgjkhjhhdhrghahdfdfhrgharafgafkaujkafghjkalkjdfgskalafgnhkjfgjdhg;ajfhfglfglalskafghiufg;ahkahur aww widdle tie… lit tienpsy doo b uwu >/////< mrowrmrowmeowrmraowmraowmrowmeowmrowmeowrmeowpurrrowmraowpurrrmrrowmraowmraownyaamrrowmeownyaamrrrrmeowrmrownya nyaaaaaaa falls asleep AAAAAAAAAAAAAAA >/////< mrowrnyaamrowrnyaaaaamrowrmrowmeownyaaaaaaameowrmraowmrowmeowmrownyaameowmeowmraownyameowmrowmrowmewmeowrmeownyaaaaamrowmrowmrowmrownyanyameonya AAAAAAAAAA >///<')
    @fun.command('8ball', 'Ask the Magic 8 Ball!')
    async def eightball(ctx: CommandContext, *, question):

        print(question)

        if question is None:
            await ctx.reply('Please ask a question!')
            return

        result = random.choice(
            [
                'It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don\'t count on it.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.'
            ]
        )

        await ctx.send(embed = SendableEmbed(
            title = question,
            description = result,
            color = config.accentcolor
        ))

    @fun.command(description = "Pretend to ban someone")
    async def ban(ctx: CommandContext, user: str, *, reason: str = None):

        await ctx.reply("Operation Completed.", embed=SendableEmbed(
            title = f"{user} has been banned.",
            description = f"**Reason:** {reason if reason else 'No reason specified.'}",
            color = config.accentcolor
        ))

    @fun.command(description = "Get a comic from xkcd by comic number. Otherwise a random one")
    async def xkcd(ctx: CommandContext, num: int = None):
        async with aiohttp.ClientSession() as session:
            if num:
                log.info("xkcd", f"Retrieving info for {num}")
                async with session.get(f'https://xkcd.com/{num}/info.0.json') as resp:
                    data = await resp.json()
                log.info("xkcd", f"Downloading image of {num}...")
                async with session.get(data['img']) as resp:
                    asset = await resp.read()
            else:
                log.info("xkcd", f"Getting latest comic number...")
                async with session.get("https://xkcd.com/info.0.json") as resp:
                    latest = await resp.json()
                    log.info("xkcd", f"Latest comic number is {latest['num']}")
                log.info("xkcd", f"Getting random one... (should be successful)")
                async with session.get(f"https://xkcd.com/{random.randint(1, latest['num'])}/info.0.json") as resp:
                    data = await resp.json()
                log.info("xkcd", f"Downloading image of {data['num']}...")
                async with session.get(data['img']) as resp:
                    asset = await resp.read()

        month = data['month']
        day = data['day']
        year = data['year']
        _num = data['num']
        news = data['news']
        safe_title = data['safe_title']
        transcript = data['transcript']
        alt = data['alt']
        img = data['img']
        title = data['title']

        log.info("xkcd", "Sending image and message...")
        await ctx.reply(embed=SendableEmbed(
            title = safe_title,
            description = (transcript if transcript != '' else '') + f'\n\n**If you do not see the image, [here]({img})**',
            media = File(asset),
            color = config.accentcolor
        ))


    @fun.command("http", "Get an HTTP cat (powered by http.cat API)")
    async def httpcat(ctx: CommandContext, code: int = None):
        if not code:
            return await ctx.reply("nyaaaaa~ please specify an http code meow :3")

        async with aiohttp.ClientSession('https://http.cat') as session:
            async with session.get('/' + str(code)) as cat:
                cat.raise_for_status()
                content_type = cat.content_type
                img = await cat.read()

        await ctx.reply(attachment=File(f=img, filename=f"{code}.{content_type.split('/')[1]}"))

    @fun.command(description = "Random commit generator")
    async def commit(ctx: CommandContext):
        async with aiohttp.ClientSession('https://whatthecommit.com') as session:
            async with session.get('/index.txt') as r:
                r.raise_for_status()
                text = await r.text()

        await ctx.reply(text)

    return fun
