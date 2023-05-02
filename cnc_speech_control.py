import speech_recognition as sr
import re
import serial

# Define serial port settings
SERIAL_PORT = "COM4"
BAUD_RATE = 9600

# Create a recognizer object
r = sr.Recognizer()

# Initialize serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Record audio from microphone
with sr.Microphone() as source:
    print("Speak now...")
    audio = r.listen(source)

# Use speech recognition to transcribe audio to text
try:
    command = r.recognize_google(audio)
    print("You said: " + command)
except sr.UnknownValueError:
    print("Could not understand audio")
    exit()
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    exit()

# Define regular expressions to match CNC commands
patterns = {
    r"set (the)? (?P<axis>x|y|z) (position|coordinate) to (?P<position>-?\d+(\.\d+)?)(?: millimeters|mm)?": "G92 {axis}{position}\n",
    r"move (the)? (?P<axis>x|y|z) (axis|axes) (by|to) (?P<position>-?\d+(\.\d+)?)(?: millimeters|mm)?": "G0 {axis}{position}\n",
    r"set the feed rate to (?P<rate>\d+) (millimeters|mm) per minute": "G1 F{rate}\n",
    r"set the spindle speed to (?P<speed>\d+) RPM": "S{speed}\n",
    r"start (the)? (spindle|tool)": "M3\n",
    r"stop (the)? (spindle|tool)": "M5\n",
    r"home (the)? (?P<axis>x|y|z) (axis|axes)": "G28 {axis}\n",
    r"set (the)? (tool|cutter) diameter to (?:a|(?P<diameter>\d+(\.\d+)?))(?: millimeters|mm)": "T1\nG10 P1 L20 D{diameter}\n",
}

# Try to match the command to a pattern and generate corresponding G-code
gcode = None
for pattern, gcode_template in patterns.items():
    matches = re.search(pattern, command)
    if matches:
        gcode = gcode_template.format(*matches.groups())
        break

# If no pattern matches the command, exit with an error message
if gcode is None:
    print(f"Sorry, I couldn't understand the command: {command}")
    exit()

# Send G-code to CNC machine over serial port
ser.write(gcode.encode())
ser.flush()

# Wait for response from CNC machine
response = ser.readline().decode().strip()
if response != "ok":
    print(f"Error sending G-code command to CNC machine: {response}")
    exit()

print(f"G-code sent to CNC machine: {gcode}")
