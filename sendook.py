#!/usr/bin/env python3
import argparse
import time
import logging
import sys
# import RPi.GPIO as GPIO #using dynamic import instead for test running on standard PC
import importlib

global GPIO

global parser
parser = argparse.ArgumentParser()


def gpio_init(gpio):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)


def gpio_cleanup():
    GPIO.cleanup()


def sleep_finegrain(delay):
    logger = logging.getLogger()
    _delay = delay / 100
    logger.debug("Sleeping for " + str(delay))
    end = time.time() + delay - _delay
    while time.time() < end:
        time.sleep(_delay)


def send_one(gpio, delay):
    GPIO.output(gpio, GPIO.HIGH)
    sleep_finegrain(delay)
    GPIO.output(gpio, GPIO.LOW)


def send_ook(gpio, code_parsed, pulselenght):
    logger = logging.getLogger()
    for cd in code_parsed:
        delay = cd[1]*pulselenght
        if cd[0] == 1:
            logger.debug("Sending 1")
            send_one(gpio, delay)
        if cd[0] == 0:
            logger.debug("Sending 0")
            sleep_finegrain(delay)


def parse_and_send(rawcode, gpio, pulselength, sleepbetween, repeat):
    logger = logging.getLogger()
    slp_us = sleepbetween/1000000.0
    pl_us = pulselength/1000000.0
    try:
        gpio_init(gpio)
        code_parsed = parse_code(rawcode)
        count = 0
        logger.debug("Message parsed:"+str(code_parsed))
        while count < repeat:
            logger.debug("Sending message count:" + str(count+1))
            send_ook(gpio, code_parsed, pl_us)
            logger.debug("Inbetween wait for count:" + str(count+1))
            sleep_finegrain(slp_us)
            count = count+1
        gpio_cleanup()
    except KeyboardInterrupt:
        gpio_cleanup()


class MockGPIO:
    def __init__(self):
        self._logger = logging.getLogger()
        self.IN = 0
        self.OUT = 0
        self.LOW = 0
        self.HIGH = 0
        self.BCM = 0

    def setmode(self, mode):
        return True

    def setup(self, gpio, mode):
        self._logger.debug("GPIO Mock setup")
        return True

    def cleanup(self):
        self._logger.debug("GPIO Mock cleanup")
        return True

    def output(self, gpio, signalmode):
        return True


def parse_code(rawcode):
    parsed = []
    rawptr = 0
    lastcode = None
    lastchar = None
    if rawcode == None or rawcode == "":
        return []
    while rawptr < len(rawcode):
        currentcode = None
        currentchar = rawcode[rawptr]
        if currentchar == "1":
            currentcode = [1, 1]
        if currentchar == "0":
            currentcode = [0, 1]
        if currentcode == None and lastcode == None:
            rawptr += 1
            continue
        if currentcode != None and currentchar != lastchar:
            if lastcode != None:
                parsed.append(lastcode)
            lastcode = currentcode
            lastchar = currentchar
        else:
            if currentcode != None:
                lastcode = [lastcode[0], lastcode[1]+1] # pylint is creepy
        rawptr += 1
    if lastcode != None:
        parsed.append(lastcode)
    return parsed


def main(*start_args):
    global GPIO

    parser.add_argument('code',  type=str,
                        help="Binary code to send. Use 0 or 1. Other chars are filtered out. Watch for starting 0s.")
    parser.add_argument('-g', dest='gpio', type=int, default=17,
                        help="GPIO pin (Default: 17)")
    parser.add_argument('-p', dest='pulselength', type=int, default=None,
                        help="Individual pulselength for 1/0 in microsec(Default: 35)")
    parser.add_argument('-s', dest='sleep', type=int, default=None,
                        help="Sleep time between repeats in microsec")
    parser.add_argument('-r', dest='repeat', type=int, default=10,
                        help="Repeat cycles (Default: 10)")
    parser.add_argument('-v', dest='verbose', type=bool, default=False,
                        help="Verbose (debug) output")
    parser.add_argument('-d', dest='dryrun', type=bool, default=False,
                        help="Dry run (do not really use gpio")

    args = parser.parse_args(start_args)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)-15s.%(msecs)03d - [%(levelname)s] %(module)s: %(message)s',)
    else:
        logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)-15s.%(msecs)03d - [%(levelname)s] %(module)s: %(message)s',)

    if args.dryrun:
        GPIO = MockGPIO()
    else:
        GPIO = importlib.import_module("RPi.GPIO")
    print(args)
    parse_and_send(args.code, args.gpio, args.pulselength,
                   args.sleep, args.repeat)


if __name__ == '__main__':
    main(*sys.argv[1:])
