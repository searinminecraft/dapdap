from voltage.ext.commands import (
    CommandsClient,
    Cog
)

def setup(client: CommandsClient) -> Cog:

    _ = Cog("Monitoring")

    return _
