#!/usr/bin/python3

from tkinter import *
import tkinter.filedialog;
from functools import partial

from robot_arm import RobotArm
from robot_arm_recorder import RobotArmRecorder, Recording

class RobotArmControl:
    def __init__(self, servo_count):
        self.__recorder = RobotArmRecorder(servo_count)
        self.__servo_count = servo_count
        self.__create_ui()

    def __create_ui(self):
        self.__window = Tk()

        self.__create_servo_sliders()
        self.__create_button_controls()

        self.__window.title("Roboterarm-Steuerung")

    def __create_servo_sliders(self):
        for num_servo in range(self.__servo_count):
            slider_label = "Servo %d" % (num_servo + 1)
            slider = Scale(self.__window, label=slider_label, length=200,
                from_=RobotArm.SERVO_MIN_DEGREES, to=RobotArm.SERVO_MAX_DEGREES,
                orient=HORIZONTAL, command=partial(self.__move_servo, num_servo))
            slider.set(RobotArm.SERVO_DEFAULT_DEGREES)
            slider.grid(row=num_servo, column=0, columnspan=2)

    def __move_servo(self, num_servo, pos):
        self.__recorder.move_servo(num_servo, int(pos))

    def __create_button_controls(self):
        btn_new_recording = Button(self.__window, text="Neue Aufnahme",
            command=self.__recorder.start_new_recording)
        btn_new_recording.grid(row=self.__servo_count, column=0, sticky="nesw")

        btn_save_recording = Button(self.__window, text="Aufnahme speichern",
            command=self.__save_recording)
        btn_save_recording.grid(row=self.__servo_count, column=1, sticky="nesw")
        
        btn_play_recording = Button(self.__window, text="Aufnahme abspielen",
            command=self.__play_recording)
        btn_play_recording.grid(row=self.__servo_count + 1, column=0, sticky="nesw")
        
        btn_loop_recording = Button(self.__window, text="Aufnahme-Endlosschleife",
            command=self.__loop_recording)
        btn_loop_recording.grid(row=self.__servo_count + 1, column=1, sticky="nesw")

    def __save_recording(self):
        path = tkinter.filedialog.asksaveasfilename(defaultextension=".json")
        if not path:
            return

        recording = self.__recorder.get_recording()
        recording.save_to_disk(path)
        
    def __play_recording(self):
        path = tkinter.filedialog.askopenfilename(defaultextension=".json")
        if not path:
            return
    
        recording = Recording.read_from_disk(path)
        self.__recorder.play_recording(recording)
        
    def __loop_recording(self):
        path = tkinter.filedialog.askopenfilename(defaultextension=".json")
        if not path:
            return
    
        recording = Recording.read_from_disk(path)
        while True:
            self.__recorder.play_recording(recording)

    def show_window(self):
        self.__window.mainloop()

if __name__=='__main__':
    control = RobotArmControl(4)
    control.show_window()
