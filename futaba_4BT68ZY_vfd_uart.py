# -*- coding: utf-8 -*-
"""Futaba 4-BT-68ZY VFD
   Micropython UART Driver for the Raspberry Pi Pico.
"""

__author__ = "Salvatore La Bua"
__copyright__ = "Copyright 2025, Salvatore La Bua"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Salvatore La Bua"
__email__ = "slabua@gmail.com"
__status__ = "Development"

from machine import Pin, UART
from utime import localtime, sleep


class Futaba4BT68ZY:
    """Driver class for the Futaba 4-BT-68ZY VFD display"""

    def __init__(self, uart_id=0, baudrate=9600, tx_pin=0, rx_pin=1):
        self.uart = UART(
            uart_id,
            baudrate=baudrate,
            bits=8,
            parity=1,
            stop=1,
            tx=Pin(tx_pin),
            rx=Pin(rx_pin),
        )
        self.colon_state = False

    def send_frame(self, command, value):
        """Send a 4-byte frame to the display"""
        frame = bytes([0xFE, 0xFD, command, value])
        self.uart.write(frame)

    def display_full(self):
        """Turn the display on"""
        self.send_frame(0x01, 0x01)

    def display_off(self):
        """Turn the display off"""
        self.send_frame(0x01, 0x00)

    def set_hours(self, hours: int):
        """Set the hours (0-23)"""
        if 0 <= hours <= 23:
            hours %= 12  # Convert to 12-hour format
            self.send_frame(0x02, hours)
        else:
            print("Invalid hours value")

    def set_minutes(self, minutes: int):
        """Set the minutes (0-59)"""
        if 0 <= minutes <= 59:
            self.send_frame(0x03, minutes)
        else:
            print("Invalid minutes value")

    def set_colon(self, state: bool):
        """Turn the colon on or off"""
        self.send_frame(0x04, 0x01 if state else 0x00)

    def update_time(self):
        """Read the current time and update the display"""
        now = localtime()
        self.set_hours(now[3])  # Hours
        self.set_minutes(now[4])  # Minutes

        # Toggle colon state for blinking effect
        self.colon_state = not self.colon_state
        self.set_colon(self.colon_state)


if __name__ == "__main__":
    vfd = Futaba4BT68ZY()

    while True:
        vfd.update_time()
        sleep(0.5)  # Wait for 0.5 seconds before the next update
