#!/usr/bin/python3

from libraries.pca9685 import PCA9685

class RobotArm:
    # Servo-Positionen
    SERVO_MIN_DEGREES = 0
    SERVO_MAX_DEGREES = 180
    SERVO_DEFAULT_DEGREES = (SERVO_MAX_DEGREES - SERVO_MIN_DEGREES) / 2
    
    # Die PWM-Frequenz muss für den Servo-Betrieb immer 50 Hz betragen
    __SERVO_PWM_FREQ = 50

    def __init__(self, servo_count):
        self.__pwm = PCA9685()
        self.__pwm.setPWMFreq(RobotArm.__SERVO_PWM_FREQ)

        self.__servo_count = servo_count

        # Servos in Startposition bringen
        self.__servo_positions = [RobotArm.SERVO_DEFAULT_DEGREES] * servo_count
        for num_servo in range(servo_count):
            self.set_servo_position(num_servo, self.__servo_positions[num_servo])

    def __convert_degrees_to_pulse(self, degrees):
        return degrees * (100 / 9) + 500

    def set_servo_position(self, num_servo, degrees):
        if (num_servo < 0 or num_servo >= self.__servo_count):
            raise ValueError("invalid servo number")
        if (degrees < RobotArm.SERVO_MIN_DEGREES or degrees > RobotArm.SERVO_MAX_DEGREES):
            raise ValueError("invalid position")

        pulse = self.__convert_degrees_to_pulse(degrees)
        self.__pwm.setServoPulse(num_servo, pulse)

        # Neue Position im Array übernehmen
        self.__servo_positions[num_servo] = degrees

    def get_servo_position(self, num_servo):
        if (num_servo < 0 or num_servo >= self.__servo_count):
            raise ValueError("invalid servo number")

        return self.__servo_positions[num_servo]
    
    @property
    def servo_count(self):
        return self.__servo_count
