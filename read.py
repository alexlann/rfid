# SPDX-FileCopyrightText: <text> 2015 Tony DiCola, Roberto Laricchia,
# and Francesco Crisafulli, for Adafruit Industries </text>

# SPDX-License-Identifier: MIT

"""
This example shows connecting to the PN532 and writing & reading a mifare classic
type RFID tag
"""

import board
import busio

import spotifyApi

# Additional import needed for I2C/SPI
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B

from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to read!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
    # Try again if no card is available.
    if uid is None:
       continue

    print("Found card with UID:", [hex(i) for i in uid])

    authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
    if not authenticated:
        print("Authentication failed!")
    
    data = pn532.mifare_classic_read_block(4)
    if data is None:
       continue
        
    print("album Id: ", data[0])
    spotifyApi.play_album(data[0])

