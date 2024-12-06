import serial
import time

# Set the serial port parameters
port = "COM1"          # Replace with the serial port you're monitoring (e.g., COM1, COM2, etc.)
baud_rate = 9600       # Set the baud rate for your device
timeout = 1            # Timeout in seconds for reading from the serial port
log_file = "serial_log.txt"  # File where data will be logged

# Open the serial port
ser = serial.Serial(port, baudrate=baud_rate, timeout=timeout)

# Check if the serial port is open
if ser.is_open:
    print(f"Successfully opened port {port}")

# Open the log file in write mode
with open(log_file, 'a') as log:
    print(f"Logging data to {log_file}...")
    
    # Continuously read from the serial port and log data
    try:
        while True:
            if ser.in_waiting > 0:  # Check if data is available to read
                data = ser.readline()  # Read a line of data
                if data:
                    # Decode data from bytes to string and strip the newline character
                    decoded_data = data.decode('utf-8').strip()
                    
                    # Print to the console (optional)
                    print(f"Received: {decoded_data}")
                    
                    # Log the data to the file with a timestamp
                    log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {decoded_data}\n")
                    
            time.sleep(0.1)  # Small delay to avoid overloading the CPU
    except KeyboardInterrupt:
        # Handle the user pressing Ctrl+C to stop logging
        print("Logging stopped.")
        ser.close()
