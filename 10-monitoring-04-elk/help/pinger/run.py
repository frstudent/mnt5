#!/usr/bin/env python3

import logging
import random
import time


logging.basicConfig(filename='../logs/pinger.log',
                            filemode='a',
                            format='%(asctime)s pinger %(levelname)s: %(message)s',
#                            format='%(asctime)s,%(msecs)d pinger %(levelname)s: %(message)s',
#                            format='%(asctime)s pinger %(levelname)s %(message)s',
#                            datefmt='%H:%M:%S',
                            datefmt='%b %d %H:%M:%S',
                            level=logging.INFO)

while True:

    number = random.randrange(0, 10)

    if number == 0:
        logging.info('Hello there!!')
    elif number == 1:
        logging.warning('Hmmm....something strange')
    elif number == 2:
        logging.error('OH NO!!!!!!')
    elif number == 3:
        logging.exception(Exception('this is exception'))
    elif number == 4:
        logging.error(Exception('Host not found'))
    elif number == 5:
        logging.warning(Exception('Opertaion timeout'))
    elif number == 6:
        logging.exception('User not found')
    elif number == 7:
        logging.info('Random number works')

    time.sleep(3)
