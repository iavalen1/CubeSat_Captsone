import sys
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO

# Global variables
spi = None

# Initialize pins and global variables
def init():
    # Initialize global variable
    global spi
    
    # Create spi object
    spi = SPI(0,0)
    
    # Set SPI slave select to output high
    GPIO.setup("P1_6", GPIO.OUT)
    GPIO.output("P1_6", GPIO.HIGH)

# Toggles the CS pin
def toggle_cs():
    # Set SS pin low
    GPIO.output("P1_6", GPIO.LOW)
    # Set SS pin high
    GPIO.output("P1_6", GPIO.HIGH)

# Takes a picture and stores image as picture.jpg
def take_picture(directory):
    # Variables
    num_of_chunks = 0       # Number of chunks to be recieved
    header = None           # Header info for each chunk
    
    # Initiate communication
    toggle_cs()
    
    # Waits for the initial response
    while(spi.readbytes(1)[0] != 85): pass

    # Read chunks information
    header = spi.readbytes(4)
    num_of_chunks = int("".join(chr(x) for x in spi.readbytes(header[0])))
    
    # Store chunks as image
    with open(directory, "wb") as file:
        # Loop to recieve and store each chunk
        for loop_num in range(0,num_of_chunks):
            # Initiate transmission of nth chunk
            toggle_cs()
            
            # Wait for initial byte
            while(spi.readbytes(1)[0] != 85): pass
            
             # Save length of chunk from header
            header = spi.readbytes(4)   # Saves the header info for the chunk
            length = header[1] << 8 | header[0]     # Saves the length of the chunk
        
            # Store chunk data
            data = spi.readbytes(length)
            file.write(bytearray(data))
    
# main function
def main():
    take_picture("picture.png")      # Takes picture and saves as picture.jpg
    print("Done!")

if __name__ == "__main__":
    init()
    main()