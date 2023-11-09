from voltage.ext.commands import (
    CommandsClient,
    CommandContext,
    Cog
)

from voltage import (
    Member,
    File,
    SendableEmbed
)

import config

from io import BytesIO
from PIL import Image, ImageOps

from time import time

def setup(client: CommandsClient) -> Cog:

    image = Cog('Image Manipulation', 'self explanatory.')

    @image.command(description = "Gentoo my beloved")
    async def gentoo(ctx, member: Member = None):
        if member is None:
            member = ctx.author
        
        start = time()
        mask = Image.open("assets/gentoo.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0)
            end = time()
        
            return await ctx.reply(embed=SendableEmbed(
                description = f":alarm_clock: Took {int((end - start) * 1000)}ms\n\n",
                media = File(
                    f = data.read(),
                    filename = "gentoo.png"
                ),
                color = config.accentcolor
            ))
    
    @image.command(description = "The worst OS ever")
    async def windows(ctx, member: Member = None):
        if member is None:
            member = ctx.author

        start = time()
        mask = Image.open("assets/windows.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0) 
            end = time()

            return await ctx.reply(embed=SendableEmbed(
                description = f":alarm_clock: Took {int((end - start) * 1000)}ms\n\n",
                media = File(
                    f = data.read(),
                    filename = "windows.png"
                ),
                color = config.accentcolor
            ))
    @image.command(description = "")
    async def void(ctx, member: Member = None):
        if member is None:
            member = ctx.author

        start = time()
        mask = Image.open("assets/void.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0) 
            end = time()

            return await ctx.reply(embed=SendableEmbed(
                description = f":alarm_clock: Took {int((end - start) * 1000)}ms\n\n",
                media = File(
                    f = data.read(),
                    filename = "void.png"
                ),
                color = config.accentcolor
            ))

    @image.command(description = "i uSe aRcH BtW")
    async def arch(ctx, member: Member = None):
        if member is None:
            member = ctx.author

        start = time()
        mask = Image.open("assets/arch.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")

        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0) 
            end = time()

            return await ctx.reply(embed=SendableEmbed(
                description = f":alarm_clock: Took {int((end - start) * 1000)}ms\n\n",
                media = File(
                    f = data.read(),
                    filename = "arch.png"
                ),
                color = config.accentcolor
            ))



    return image
