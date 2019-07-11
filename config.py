
import board

GPIO_PIN = board.D18

# IP address of the server (UDP)
UDP_IP = '192.168.1.220'

# Port number used for UDP socket communication
UDP_PORT = 5005

TOTAL_LED_COUNT = 100


class Area:
    def __init__(self, name, start_index, end_index):
        self.name = name
        self.start_index = start_index
        self.end_index = end_index
        self.led_count = end_index - start_index
    
    def update_colors(self, pixels, colors):
        for i, color in enumerate(colors):
            pixels[self.start_index + i] = color
        pixels.show()


# Configure areas for the led system
AREAS = {
    'room': Area('room', 31, 100)
}
