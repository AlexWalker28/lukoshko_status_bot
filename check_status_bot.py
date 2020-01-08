import time
from multiprocessing import Pool


def write_to_file(filename, sec):
    start = time.time()
    with open(filename, 'w') as f:
        elapsed = time.time() - start
        while elapsed < sec:
            f.write('a')
            elapsed = time.time() - start
        print(f'time elapsed: {elapsed} sec')


def write_to_folders(filenames, sec):
    start = time.time()
    for filename in filenames:
        print(filename)
        with open('test_dir/' + filename, 'w') as f:
            elapsed = time.time() - start
            while elapsed < sec:
                f.write('a')
                elapsed = time.time() - start
            print(f'time elapsed: {elapsed} sec')

with Pool(processes=3) as pool:
    pool.starmap(write_to_folders, [(['channel0/test0.txt', 'channel0/test1.txt', 'channel0/test2.txt'], 3),
                                    (['channel1/test0.txt', 'channel1/test1.txt', 'channel1/test2.txt'], 3),
                                    (['channel2/test0.txt', 'channel2/test1.txt', 'channel2/test2.txt'], 5)])
