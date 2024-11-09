""" TODO """

# Note : Built-in imports
from pathlib import Path

# Note : API Discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from .const import DISCORD_WEBHOOK_URL


class DiscordClient:
    """ TODO """

    def __init__(self):
        """ TODO """
        pass

    def send_discord_message(self,
                             titre: str,
                             description: str):
        """ TODO """

        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)

        # Note : "Upload" de l'image
        vignette_file_path = Path("../medias/ariss-logo.webp")
        with open(vignette_file_path, "rb") as f:
            webhook.add_file(file=f.read(), filename='ariss-logo.webp')

        # Note : create embed object for webhook
        # Note : you can set the color as a decimal (color=242424) or hex (color='03b2f8') number
        embed = DiscordEmbed(title=titre,       # Note : L'emoji "gyrophare" est référencé 1F6A8 sur la page : https://www.w3schools.com/charsets/ref_emoji.asp
                             description=description,
                             color="ff8f00")
        embed.set_thumbnail(url="attachment://ariss-logo.webp")

        # Note : add embed object to webhook
        webhook.add_embed(embed)

        response = webhook.execute()
