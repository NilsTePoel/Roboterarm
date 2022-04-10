#!/usr/bin/python3

import time
import json

from robot_arm import RobotArm

class Movement:
    def __init__(self, num_servo, degrees, time):
        self.num_servo = num_servo
        self.degrees = degrees
        self.time = time

class Recording:
    def __init__(self, start_time, movement_history):
        self.start_time = start_time
        self.movement_history = movement_history

    def save_to_disk(self, path):
        serialized_movement_history = [movement.__dict__ for movement in self.movement_history]
        serialized_recording = (self.start_time, serialized_movement_history)

        with open(path, 'w') as f:
            json.dump(serialized_recording, f)
    
    @classmethod
    def read_from_disk(cls, path):
        with open(path, 'r') as f:
            serialized_recording = json.load(f)
            
            start_time = serialized_recording[0]
            serialized_movement_history = serialized_recording[1]
            movement_history = [Movement(m["num_servo"], m["degrees"], m["time"]) for m in serialized_movement_history]
            
            recording = cls(start_time, movement_history)
            return recording

class RobotArmRecorder: 
    def __init__(self, servo_count):
        self.__robot_arm = RobotArm(servo_count)

        self.__movement_history = []
        self.__start_time = time.time()

    def move_servo(self, num_servo, degrees):
        self.__movement_history.append(Movement(num_servo, degrees, time.time()))
        self.__robot_arm.set_servo_position(num_servo, degrees)

    def start_new_recording(self):
        # Verlauf zurücksetzen
        self.__movement_history.clear()
        self.__start_time = time.time()

        # Anfangspositionen der Servos im Verlauf abspeichern
        servo_count = self.__robot_arm.servo_count
        for num_servo in range(servo_count):
            m = Movement(num_servo, self.__robot_arm.get_servo_position(num_servo), self.__start_time)
            self.__movement_history.append(m)

    def get_recording(self):
        return Recording(self.__start_time, self.__movement_history)

    def play_recording(self, recording):
        current_time = recording.start_time

        for movement in recording.movement_history:
            # Bis zur Bewegung warten
            time_before_movement = movement.time - current_time
            time.sleep(time_before_movement)
            current_time = movement.time

            # Servo anhand des Verlaufs bewegen
            self.__robot_arm.set_servo_position(movement.num_servo, movement.degrees)
