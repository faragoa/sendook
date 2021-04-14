# sendook
Send ASK/OOK messages from python 

Usage:
Record your binary code, any bitlength (with URH)

Then play it from raspberry pi.

Usage: python3 sendook.py [-h] [-g GPIO] [-p PULSELENGTH] [-s SLEEP] [-r REPEAT] [-v VERBOSE] [-d DRYRUN] code

-g : GPIO pin for output

-p : individula pulse length (same for 1, 0s)

-s : wait between repeats

-r : number of repeats

-v : detailed debug log

-d : dryrun mode. Not opening GPIO and not sending code. Useful for debug logs without filling the ether with garbage
code: binary code format like "0110110". As in OOK, the send will stop at 0s and will go at 1s. All other characters are simply omitted.

Tested with raspberry pi 3b, 3a. You need a radio transmitter wired to the pi to make it work. For exact hardware google "radio transmission 433 mhz raspberry pi". It definitely works for other frequency OOK transmitters.

Worked for dimmers (24 bit code), garage door openers (60 bit length code). 

For recording I used Universal Radio Hacker & TV dongle.