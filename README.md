# CNC Speech Control
### transcribes spoken commands into G-code commands for controlling a CNC machine. The G-code commands are sent over a serial connection to the CNC machine.

## Requirements
#### Python 3.x
#### speech_recognition library
#### serial library
## Usage
#### Connect your CNC machine to your computer using a serial connection.
#### Update the `SERIAL_PORT` and `BAUD_RATE` variables to match your CNC machine's serial connection settings.
#### Run the script using python `cnc_speech_control.py`
#### When prompted, speak a command into the microphone.
#### The script will attempt to match your spoken command to a pattern and generate the corresponding G-code command.
#### The G-code command will be sent to the CNC machine over the serial connection.
## Supported Commands
### The following commands are currently supported:

#### Set the X/Y/Z position to a specified value
#### Move the X/Y/Z axis by a specified value
#### Set the feed rate to a specified value
#### Set the spindle speed to a specified value
#### Start or stop the spindle or tool
#### Home the X/Y/Z axis
#### Set the tool diameter

## How it Works
#### The script uses regular expressions to match spoken commands to G-code commands. If a match is found, the corresponding G-code command is generated and sent to the CNC machine over the serial connection.

#### If no match is found, an error message is displayed and the script exits.

## Future Improvements
#### Add support for additional CNC commands
#### Improve the accuracy of speech recognition
#### Implement error handling for serial connection issues
