#!/usr/bin/env python3
# coding: utf-8
""" TODO """

# Note : Built-in imports
from typing import Dict

# Note : Discord API
from discord_api import DiscordClient

# Note : Open Meteo API
from bot_ariss import BotAriss
#from ariss.const import ALERTS_THRESHOLD, AlertType

# Note : Functions definition
def send_discord_notification(message: str):
    """ TODO

    Args:
        status:

    Returns:

    """

    if message:
        message_header = f"TEST TEST TEST\n"
        message_body   = f"{message}\n"

        message_footer = "Pour plus de détails, veuillez vous référer\n" \
                         "- [ARISS calendar](https://www.amsat-on.be/ariss-calendar-with-scheduled-contacts-by-the-ariss-operation-team/)\n" \

        concatenated_message = "".join([message_header, message_body, message_footer])
        print(f"DBG \n" \
              f"{concatenated_message}")

        # Note : Envoi
        DiscordClient().send_discord_message("🛰️ **ALERTE** 🛰️ ",  # Note : L'emoji "gyrophare" est référencé 1F6A8 sur la page : https://www.w3schools.com/charsets/ref_emoji.asp
                                             concatenated_message)

def main():
    """ Main entry point

    Returns: Nothing
    """

    bot     = BotAriss()
    message = bot.send_msg()
    send_discord_notification(message)

if __name__ == '__main__':
    main()
