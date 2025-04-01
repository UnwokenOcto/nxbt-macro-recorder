# NXBT Macro Recorder

NXBT Macro Recorder is a tool that allows you to record macros for [NXBT](https://github.com/Brikwerk/nxbt/).
This fork adds in support for recording joystick motion and simultaneous button
inputs.

## Usage

To record a macro and store it in a file, run the following command:

```python
python macro.py <macro_name>
```

The inputs will be recorded until the Screenshot button is pressed.
Button mappings can be set by modifying the button_map dictionary near the top
of macro.py.

## TODO

* Implement recording of left/right triggers and dpad
