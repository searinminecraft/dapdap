from voltage.ext.commands import (
    CommandsClient,
    CommandContext,
    Cog
)
from voltage import SendableEmbed

from helper import log
import config

import sys
def setup(client: CommandsClient) -> Cog:
    t = Cog('Testing', ':trol:')

    @t.command()
    async def aea(ctx: CommandContext, value = None):
        sys.exit(0)

    return t
