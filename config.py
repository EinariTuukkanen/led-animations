
# IP address of the server (UDP)
UDP_IP = '127.0.0.1'

# Port number used for UDP socket communication
UDP_PORT = 5005

# GPIO pin connected to the LED strip pixels (must support PWM)
LED_PIN = 18

# LED signal frequency in Hz (usually 800kHz)
LED_FREQ_HZ = 800000

# DMA channel used for generating PWM signal (try 5)
LED_DMA = 5

# Brightness of LED strip between 0 and 255
BRIGHTNESS = 255

# Set True if using an inverting logic level converter
LED_INVERT = False

# Set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_CHANNEL = 0

# Configure areas for the led system
AREAS = {
    'olohuone': {
        'start_index': 0,
        'end_index': 100,
    },
}
