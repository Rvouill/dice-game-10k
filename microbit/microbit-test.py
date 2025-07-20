import serial

with serial.Serial('/dev/tty.usbmodem111402', 115200, timeout=1) as ser:
    print("Listening for micro:bit PING…")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "PING":
            print("🅰 PING received from micro:bit!")
        if line == "PONG":
            print("🅱 PONG received from micro:bit!")