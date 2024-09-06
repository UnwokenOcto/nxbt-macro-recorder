import pygame
import sys
import time

# Initialize pygame's joystick module
pygame.init()
pygame.joystick.init()

# Use the first connected joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

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
}


def record_macro(filename):
    recording = True
    start_time = time.time()
    last_action = time.time()
    active_button = None

    with open(filename, "w") as f:
        while recording:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:

                    # Skip if a button was already pressed
                    if active_button is not None:
                        continue

                    button = event.button
                    # Use screenshot button to end recording
                    if button == 15:
                        print("Recording stopped")
                        recording = False
                        break

                    start_time = time.time()
                    pause_duration = start_time - last_action
                    active_button = button

                    print(f"{pause_duration:.1f}s")
                    f.write(f"{pause_duration:.1f}s\n")

                elif event.type == pygame.JOYBUTTONUP:
                    button = event.button
                    if active_button != button:
                        continue

                    duration = time.time() - start_time
                    last_action = time.time()
                    active_button = None

                    print(f"{button_map[button]} {duration:.1f}s")
                    f.write(f"{button_map[button]} {duration:.1f}s\n")


if __name__ == "__main__":
    record_macro(sys.argv[1])
