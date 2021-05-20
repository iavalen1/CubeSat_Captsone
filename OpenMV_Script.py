import pyb, sensor, image, time, ustruct, math, os

# Global variables
PIN3 = None
spi = None

# Initialize sensor and variables
def init():
    # Init global variables
    global PIN3,spi

    # Initialize sensor
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)

    # Initialize variables
    PIN3 = pyb.Pin("P3", pyb.Pin.IN)    # Sets up variable for CS PIN
    spi = pyb.SPI(2, pyb.SPI.SLAVE, polarity=0, phase=0)    # Sets up spi

# Takes the picture and sends in 1024 byte chunks (1019 for image + 5 for header)
def send_image():
    # Initialize variables
    num_of_chunks = 0
    chunk_data = None

    # Take and save picture
    sensor.snapshot().save("picture.jpg")

    # Read number of chunks
    num_of_chunks = math.ceil(os.stat("picture.jpg")[6] / 1019)

    # Send communication header
    spi.send(ustruct.pack("<bi%ds" % len(str(num_of_chunks)), 85, len(str(num_of_chunks)), str(num_of_chunks)))     # Contains number of chunks to be sent

    # Read file and send in 1024 byte chunks (1019 for image + 5 for header)
    with open("picture.jpg", "rb") as file:
        while(True):
            chunk_data = bytearray(file.read(1019))

            # Checks if EOF reached
            if not chunk_data:
                break;

            # Waits for PocketBeagle to be ready
            while(PIN3.value() == 1): pass

            # Send chunk
            spi.send(ustruct.pack("<bi%ds" % len(chunk_data), 85, len(chunk_data), chunk_data))

    os.remove("picture.jpg")

# Waiting for CS pin to go low to take and send picture
def main():
    while(True):
        # waits for PocketBeagle to initiate communication
        if(PIN3.value() == 0):
            send_image()    # Takes a picture and sends it to the PocketBeagle
            pyb.delay(1000) # Short delay for pins to reset

if __name__ == "__main__":
    init()
    main()
