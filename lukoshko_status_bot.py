from glob import glob
import os

from telegram import Bot
from telegram.ext import Updater

from file_watcher import FileWatcher


def main():
    token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_BOT_CHAT_ID')
    lukoshko_dir = os.environ.get('LUKOSHKO_DIR')

    bot = Bot(token)

    updater = Updater(token, use_context=True)
    # dp = updater.dispatcher

    file_watcher = FileWatcher(bot, chat_id, 60)
    file_watcher.watch_dirs(glob(f'{lukoshko_dir}/*'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
