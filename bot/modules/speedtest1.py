from speedtest import Speedtest
from telegram.ext import CommandHandler

from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage

def speedtest(self, servers):
    test = Speedtest()
    test = speedtest.Speedtest()
    test.get_servers(servers)
    test.get_best_server()
    test.download(threads=None)
    test.upload(threads=None)
    return test.results.dict()
    
class SpeedtestMod(loader.Module):
    strings = {"name": "Speedtest",
               "running": "<b>Running speedtest...</b>",
               "results": "<b>Speedtest Results:</b>",
               "results_download": "<b>Download:</b> <code>{}</code> <b>MiB/s</b>",
               "results_upload": "<b>Upload:</b> <code>{}</code> <b>MiB/s</b>",
               "results_ping": "<b>Ping:</b> <code>{}</code> <b>ms</b>"}

async def speedtestcmd(self, message):
    await utils.answer(message, self.strings("running", message))
    args = utils.get_args(message)
    servers = []\
    for server in args:
        try:
            servers += [int(server)]
            except ValueError:
                logger.warning("server failed")
                results = await utils.run_sync(self.speedtest, servers)
                ret = self.strings("results", message) + "\n\n"
                ret += self.strings("results_download", message).format(round(results["download"] / 2**20, 2)) + "\n"
                ret += self.strings("results_upload", message).format(round(results["upload"] / 2**20, 2)) + "\n"
                ret += self.strings("results_ping", message).format(round(results["ping"], 2)) + "\n"
                await utils.answer(message, ret)

SPEED_HANDLER1 = CommandHandler(BotCommands.SpeedCommand1, speedtest1, filters=CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(SPEED_HANDLER1)