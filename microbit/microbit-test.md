
# 🧪 Micro:bit Serial Test Integration

This README documents how to test basic serial communication between a micro:bit board and the Python dice-game project. The goal is to verify that button A and B presses on the micro:bit send `"PING"` and `"PONG"` signals that are received correctly in Python.

---

## 🔌 Hardware Required

- 1x [BBC micro:bit](https://microbit.org/)
- 1x USB cable (data-compatible)
- Host machine (macOS, Linux or Windows)

---

## 🔧 Setup Steps

### 📦 1. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# deactivate when done
deactivate
```

### 📥 2. Install dependencies

We need pyserial to read from the micro:bit and Pillow for GUI (used elsewhere in the project):

```bash
pip3 install pyserial Pillow
# verify install
python -c "import serial, PIL; print('pyserial and pillow are installed')"
```

### 💾 3. Flash the micro:bit

Drag the microbit-test.hex file into the device volume, or use ([MakeCode editor](https://makecode.microbit.org/)) with the following code

```python
def on_forever():
    basic.show_icon(IconNames.HAPPY)
    if input.button_is_pressed(Button.A):
        serial.write_line("PING")
    if input.button_is_pressed(Button.B):
        serial.write_line("PONG")
basic.forever(on_forever)
```

Upload it to your micro:bit by dragging the .hex file into the device volume, or use MakeCode editor at https://makecode.microbit.org/

### 🖥️ 4. Python test script: microbit-test.py

```python
with serial.Serial('/dev/tty.usbmodem111402', 115200, timeout=1) as ser:
    print("Listening for micro:bit PING…")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "PING":
            print("🅰 PING received from micro:bit!")
        if line == "PONG":
            print("🅱 PONG received from micro:bit!")
```

⚠️ Replace /dev/tty.usbmodem111402 with your actual serial port if needed.

### 🧪 5. Run the test

- Plug in your micro:bit

- Activate the virtual environment:

  ```bash
  source .venv/bin/activate
  ```

- Run the Python script:

  ```bash
  python3 microbit/microbit-test.py
  ```

- Press Button A → You should see:

  ```bash
  🅰 PING received from micro:bit!
  ```

- Press Button B → You should see:
  ```bash
  🅱 PONG received from micro:bit!
  ```

## 🛠️ Troubleshooting

- Use ls /dev/tty.* to find your micro:bit port on macOS
- On Windows, try COM3, COM4, etc.
- Ensure the .hex file is correctly flashed and includes serial.write_line
