import pygame
import sys
import time
from datetime import timedelta

"""
button_map = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "MINUS",
    5: "HOME",
    6: "PLUS",
    9: "L",
    10: "R",
    11: "DPAD_UP",
    12: "DPAD_DOWN",
    13: "DPAD_LEFT",
    14: "DPAD_RIGHT",
}"""
# Switch Pro Controller Button Map
button_map = {
    0: "B",
    1: "A",
    2: "X",
    3: "Y",
    4: "CAPTURE",
    5: "L",
    6: "R",
    7: "ZL",
    8: "ZR",
    9: "MINUS",
    10: "PLUS",
    11: "HOME",
    12: "L_STICK_PRESS",
    13: "R_STICK_PRESS"
}

# Represents one joystick input taking place over an interval of time
class ButtonInput:
    def __init__(self, button):
        self.button = button

    def __str__(self):
        return self.button

class StickInput:
    def __init__(self, xAxis, yAxis, xValue, yValue):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.xValue = xValue
        self.yValue = yValue

    def __str__(self):
        return "stick_todo"

# Represents the simultaneous joystick inputs taking place over an interval of time
# If the inputs array is empty, then the object represents a pause in inputs
class TimelineRecord:
    def __init__(self, inputs, start):
        self.inputs = inputs    # Array of ButtonInput/StickInput objects
        self.start = start      # Start time
        self.end = None         # End time

    def __str__(self):
        input_string = ""
        for i in self.inputs:
            input_string += f"{str(i)} "
        duration = timedelta(seconds=self.end-self.start).total_seconds()
        return f"{input_string}{duration}s"

# Handles the recording of a single input
def start_input(joystick):
    active_inputs = []
    current_time = time.perf_counter()
    for i in range(0, joystick.get_numbuttons()):
        if joystick.get_button(i):
            button = ButtonInput(button_map[i])
            active_inputs.append(button)

    record = TimelineRecord(active_inputs, current_time)
    return record

def end_input(active_record, file):
    active_record.end = time.perf_counter()
    file.write(str(active_record) + "\n")
    print(str(active_record))


# Records a macro and saves it to filename
def record_macro(filename, joystick):
    active_record = None    # Contains a TimelineRecord with no end time set
    recording = True

    with open(filename, "w") as file:
        print("\nController info:")
        print(f"ID: {joystick.get_id()}")
        print(f"Name: {joystick.get_name()}\n")
        print("Recording...")
        while recording:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:

                    # Use screenshot button to end recording
                    if button_map[event.button] == "CAPTURE":
                        print("Recording stopped")
                        recording = False
                        break

                    if active_record is None:
                        active_record = start_input(joystick)

                    else:
                        end_input(active_record, file)
                        active_record = start_input(joystick)

                    #print(f"Button down: {button_map[event.button]}")

                elif event.type == pygame.JOYBUTTONUP:
                    if active_record is None:
                        print("Error: active_record is none during event pygame.JOYBUTTONUP")

                    else:
                        end_input(active_record, file)
                        active_record = start_input(joystick)

                    #print(f"Button up: {button_map[event.button]}")


if __name__ == "__main__":
    # Initialize pygame's joystick module
    pygame.init()
    pygame.joystick.init()

    # Use the first connected joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    record_macro(sys.argv[1], joystick)
