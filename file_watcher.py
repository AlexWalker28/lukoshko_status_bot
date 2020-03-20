import os
import time
import requests
import datetime
from glob import glob
from multiprocessing import Pool


class FileWatcher:

    def __init__(self, bot, chat_id, check_interval):
        self.bot = bot
        self.chat_id = chat_id
        self.check_interval = check_interval

    def _get_latest_filename(self, folder):
        return sorted(glob(f'{folder}/*'), key=os.path.getmtime)[-1]

    def _is_new_file(self, old_filename, directory):
        new_filename = self._get_latest_filename(directory)
        if old_filename != new_filename:
            print(f'new file created: {new_filename}')
            return True
        else:
            return False

    def watch_dirs(self, dirs):
        # select only folders
        dirs = list(filter(os.path.isdir, dirs))
        # to remove weird folders on NAS
        dirs = [d for  d in dirs if '@' not in d]
        print(f'watching directories: {dirs}')
        dirs_count = self._count_dirs()
        print(f'dirs count: {dirs_count}')
        recordings = [Recording(self.bot, self.chat_id, dir) for dir in dirs]
        with Pool(dirs_count) as pool:
            pool.map(self._watch_files, recordings)

    def _count_dirs(self):
        return len(list(filter(os.path.isdir, glob(f'{os.environ.get("LUKOSHKO_DIR")}/*'))))

    def _watch_files(self, recording):
        filename = self._get_latest_filename(recording.dir)
        print(f'watching file: {filename}')
        while True:
            file_size = os.path.getsize(filename)
            time.sleep(self.check_interval)
            requests.post(os.getenv("LUKOVICA_URL"), data={'time': datetime.datetime.utcnow(), 'lukoshko': True}, headers={'token': os.getenv('LUKOVICA_TOKEN')})
            print(f'{os.path.getsize(filename) - file_size}')
            if file_size == os.path.getsize(filename):
                if self._is_new_file(filename, recording.dir):
                    filename = self._get_latest_filename(recording.dir)
                    recording.is_active = True
                else:
                    recording.is_active = False
            elif file_size < os.path.getsize(filename):
                recording.is_active = True


class Recording:
    def __init__(self, bot, chat_id, dir):
        self.bot = bot
        self.chat_id = chat_id
        self._is_active = None
        self.dir = dir

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        if self._is_active != value:
            print(f'value changed\n previous value: {self._is_active}\n current_value: {value}')
            self._is_active = value
            self._send_message_to_bot(self.dir, value)

    def _send_message_to_bot(self, dir, is_recording):
        message = f'{dir.split("/")[-1]}\n'
        if is_recording:
            message += 'Recording is fine'
        else:
            message += '!!!RECORDING HAS STOPPED!!!'
        print(message)
        self.bot.send_message(chat_id=self.chat_id, text=f'{time.ctime()}\n{message}')
