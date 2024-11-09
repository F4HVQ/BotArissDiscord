""" TODO """

# Note : Built-in imports
from typing import Dict
import argparse
from pathlib import Path
import re
import sys

try:
    from constants.constants import Constants
    from discord_api import DiscordClient
    from bot_ariss import BotAriss

except ImportError as err:
    print("[IMPORT ERROR]\t\t{} : {}".format(__file__, err))
    sys.exit()


# Note : Functions definition
def send_discord_notification(message: str,
                              testing=False):
                              # type (str, bool):

    if testing:
        message_header = f"TEST TEST TEST\n"
        message_body   = f"Ceci est un test régulier, effectué NORMALEMENT tous les 3 mois\n" \
                         f"Les critères de recherche des evennements ARISS sont les suivantes :\n" \
                         f"- Europe\n" \
                         f"- SSTV\n"
        message_footer = "\nFIN TEST\n"

        message = "".join([message_header, message_body, message_footer])
        print(message)

        # Note : Envoi
        DiscordClient().send_discord_message("🛰️ **ALERTE** 🛰️ ",  # Note : L'emoji "gyrophare" est référencé 1F6A8 sur la page : https://www.w3schools.com/charsets/ref_emoji.asp
                                             message)
    else:
        if message is not None:
            message_header = f"\n"
            message_body   = f"{message}\n"

            message_footer = "Pour plus de détails, veuillez vous référer\n" \
                             "- [ARISS calendar](https://www.amsat-on.be/ariss-calendar-with-scheduled-contacts-by-the-ariss-operation-team/)\n" \

            concatenated_message = "".join([message_header, message_body, message_footer])
    #        print(f"DBG \n" \
    #              f"{concatenated_message}")

            # Note : Envoi
            DiscordClient().send_discord_message("🛰️ **ALERTE** 🛰️ ",  # Note : L'emoji "gyrophare" est référencé 1F6A8 sur la page : https://www.w3schools.com/charsets/ref_emoji.asp
                                                 concatenated_message)

def check_parameters(args):
    # type () -> bool
    """ Check input parameters """

    print("[INFO] Checking parameters ...")

    if args.DAYS_FUTURE is not None:
        if args.DAYS_FUTURE < 0:
            print("[ERROR] Argument '{}' is NOT a valid time period --days option".format(args.DAYS_FUTURE))
            return Constants.EXIT_FAILURE

    print("[OK] Checking parameters completed")


if __name__ == '__main__':

    # Specify command arguments
    epilog_msg = '''\
    See above examples :
    - ariss_main.py -n 14
    - ariss_main.py -n 14 -t

    '''

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                             description="TODO",
                             epilog=epilog_msg)

    group_options = parser.add_argument_group('options')

    group_options.add_argument('-n', '--days',
                           dest='DAYS_FUTURE',
                           type=int,
                           action='store',
                           default=14,
                           required=False,
                           help='Number of day to parse calendar')

    group_options.add_argument('-t', '--test',
                               dest='TEST',
                               action='store_true',
                               default=False,
                               required=False,
                               help='TEST')

    args = parser.parse_args()
    if Constants.EXIT_FAILURE == check_parameters(args):
        sys.exit(Constants.EXIT_FAILURE)
    else:
        bot = BotAriss(args.DAYS_FUTURE)

        message = bot.get_synthese()
        send_discord_notification(message,
                                  testing = args.TEST)

