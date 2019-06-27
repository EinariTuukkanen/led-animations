
# IP address of the server (UDP)
UDP_IP = '192.168.1.220'

# Port number used for UDP socket communication
UDP_PORT = 5005

# GPIO pin connected to the LED strip pixels (must support PWM)
LED_PIN = 18

# LED signal frequency in Hz (usually 800kHz)
LED_FREQ_HZ = 800000

# DMA channel used for generating PWM signal (try 5)
LED_DMA = 10

# Brightness of LED strip between 0 and 255
BRIGHTNESS = 255

# Set True if using an inverting logic level converter
LED_INVERT = False

# Set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_CHANNEL = 0


class Area:
    def __init__(self, name, start_index, end_index):
        self.name = name
        self.start_index = start_index
        self.end_index = end_index
        self.led_count = end_index - start_index


# Configure areas for the led system
AREAS = {
    'olohuone': Area('olohuone', 31, 100)
}
