# Author of PWM file: Tony DiCola
# License: Public Domain
from __future__ import division
import timeo
# Import the PCA9685 module.
import Adafruit_PCA9685
import math
import os
import sys
import tty, termios
import re
from xml.dom import minidom
from svg.path import parse_path

svg = minidom.parse("C:\Users\Emily\Downloads\Apple\homer-simpson.svg") #change to proper name
paths = [path.getAttribute('d') for path in svg.getElementsByTagName('path')]
print(paths)
locationx = 0
locationy = 0
locationz = 1
global listOfImageCoordinates
listOfImageCoordinates = []

regex = """[MZLHVCSQTARmzlhvcsqtar][\d\,\.-]+"""
regex_numbers = """-?[\d\.]+"""
for path in paths:
    commands = re.findall(regex, str(path))
    locations = []
    cubic_prev_control = None
    locationz = 1
    for command in commands:
        locationz = 1
        locations.append((locationx, locationy, locationz))
        if command[0] is 'M':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 2)
            locationx = float(parts[0])
            locationy = float(parts[1])
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'Z':
            continue
        elif command[0] is 'L':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 2)
            locationx = float(parts[0])
            locationy = float(parts[1])
            locationz = 0
            locations.append((locationx, locationy, loccationz))
        elif command[0] is 'H':
            part = float(command[1:])
            locationx = part
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'V':
            part = float(command[1:])
            locationy = part
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'C':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 6)
            parts = map(float, parts)
            cubic_prev_control = (parts[2], parts[3])
            midx = (0.5 ** 3) * locationx + 3.0 * (0.5 ** 3) * parts[0] + 3.0 * (0.5 ** 3) * parts[2] + (0.5 ** 3) * parts[4]
            midy = (0.5 ** 3) * locationy + 3.0 * (0.5 ** 3) * parts[1] + 3.0 * (0.5 ** 3) * parts[3] + (0.5 ** 3) * parts[5]
            locationz = 0
            locations.append((midx, midy, locationz))
            locationx = parts[4]
            locationy = parts[5]
            locationz = 0
            locations.append((parts[4], parts[5], locationz))
        elif command[0] is 'S':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 4)
            parts = map(float, parts)
            if cubic_prev_control is None:
                cubic_prev_control = (locationx, locationy)
            cp2 = (parts[0], parts[1])
            cp1 = (2 * locationx - cubic_prev_control[0], 2 * locationy - cubic_prev_control[1])
            cubic_prev_control = cp2
            ep = (parts[2], parts[3])
            parts = map(float, parts)
            midx = (0.5 ** 3) * locationx + 3.0 * (0.5 ** 3) * cp1[0] + 3.0 * (0.5 ** 3) * cp2[0] + (0.5 ** 3) * ep[0]
            midy = (0.5 ** 3) * locationy + 3.0 * (0.5 ** 3) * cp1[1] + 3.0 * (0.5 ** 3) * cp2[1] + (0.5 ** 3) * ep[1]
            locationz = 0
            locations.append((midx, midy, 0))
            locationx = ep[0]
            locationy = ep[1]
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'Q' or command[0] is 'T' or command[0] is 'A' or command[0] is 'R':
            raise Exception("Don't know how to interpret")
        elif command[0] is 'm':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 2)
            locationx += float(parts[0])
            locationy += float(parts[1])
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'z':
            continue
        elif command[0] is 'l':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 2)
            locationx += float(parts[0])
            locationy += float(parts[1])
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'h':
            part = float(command[1:])
            locationx += part
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'v':
            part = float(command[1:])
            locationy += part
            locationz = 0
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'c':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 6)
            parts = map(float, parts)
            cubic_prev_control = (parts[2] + locationx, parts[3] + locationy)
            midx = (0.5 ** 3) * locationx + 3.0 * (0.5 ** 3) * (locationx + parts[0]) + 3.0 * (0.5 ** 3) * (locationx + parts[2]) + (0.5 ** 3) * (locationx + parts[4])
            midy = (0.5 ** 3) * locationy + 3.0 * (0.5 ** 3) * (locationy + parts[1]) + 3.0 * (0.5 ** 3) * (locationy + parts[3]) + (0.5 ** 3) * (locationy + parts[5])
            locationx += parts[4]
            locationy += parts[5]
            locationz = 0
            locations.append((midx, midy, locationz))
            locations.append((locationx, locationy, locationz))
        elif command[0] is 's':
            parts = re.findall(regex_numbers, command[1:])
            assert (len(parts) == 4)
            parts = map(float, parts)
            cp2 = (locationx + parts[0], locationy + parts[1])
            if cubic_prev_control is None:
                cubic_prev_control = (locationx, locationy)
            cp1 = (2 * locationx - cubic_prev_control[0], 2 * locationy - cubic_prev_control[1])
            cubic_prev_control = cp2
            ep = (locationx + parts[2], locationy + parts[3])
            parts = map(float, parts)
            midx = (0.5 ** 3) * locationx + 3.0 * (0.5 ** 3) * cp1[0] + 3.0 * (0.5 ** 3) * cp2[0] + (0.5 ** 3) * ep[0]
            midy = (0.5 ** 3) * locationy + 3.0 * (0.5 ** 3) * cp1[1] + 3.0 * (0.5 ** 3) * cp2[1] + (0.5 ** 3) * ep[1]
            locationz = 0
            locations.append((midx, midy, locationz))
            locationx = ep[0]
            locationy = ep[1]
            locations.append((locationx, locationy, locationz))
        elif command[0] is 'q' or command[0] is 't' or command[0] is 'a' or command[0] is 'r':
            print command[0]
            raise Exception("Don't know how to interpret")
        else:
            raise Exception("Don't like this input")
        if command[0] not in ['C', 'c', 's', 'S']:
            cubic_prev_control = None

    for location in locations:
        coordinate = [-((float(location[0])/16) + 10), (float(location[1])/16) - 5, float(location[2])] #line to change
        listOfImageCoordinates.append(coordinate)

#end of svg to coord file

# Uncomment to enable debug output.
# import logging
# logging.basicConfig(level=logging.DEBUG)

pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150  # Min pulse length out of 4096
servo_max = 4000  # Max pulse length out of 4096


# Helper function to make setting a servo pulse width simpler.

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60  # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096  # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
pwm.set_pwm(0, 0, 360)
pwm.set_pwm(4, 0, 360)
pwm.set_pwm(8, 0, 300)

old_servo0_output = 360
old_servo1_output = 360
old_servo2_output = 300
tmp_servo0_output = old_servo0_output

tmp_servo1_output = old_servo1_output
tmp_servo2_output = old_servo2_output

pi = 3.1415926
base_heigh = 5.0;  # The heigh of the base
pen_length = 5.80001;  # The length of the pen

upper_arm_length = 13.9
fore_arm_length = 15.2
point1_num = 13
point2_num = 14

# point_num = point1_num + point2_num

point_num = 100
Line_Pos = [[0 for i in range(3)] for j in range(point_num)]
n = 0
c2 = [0 for i in range(point_num)]
c1 = [0 for i in range(point_num)]
upper_angle1 = [0 for i in range(point_num)]
upper_angle2 = [0 for i in range(point_num)]
fore_angle1 = [0 for i in range(point_num)]
fore_angle2 = [0 for i in range(point_num)]
New_Pos = [0 for i in range(point_num)]
New_Line_Pos = [0 for i in range(point_num)]
Angle_Pos = [[0 for i in range(3)] for j in range(point_num)]
Angle_Degree = [[0 for i in range(3)] for j in range(point_num)]

# fd = sys.stdin.fileno()
# old_settings = termios.tcgetattr(fd)
print('Moving servos to draw a line, press Ctrl-Z to quit ... \n')
# print ('input letter l to draw a line \n')

#lines = [10, -5, 25, -5, 25, -5, 25, 10, 25, 10, 10, 10, 10, 10, 10, -5] do not need, new array i listOfImageCoordinates
i95 = 0

while True:
    #
    ch = raw_input('input letter l to draw a line \n')

    if ch == 'l':
        n = n + 1
        x0 = listOfImageCoordinates[i95][0]
        y0 = listOfImageCoordinates[i95][1]
        z0 = [i95][2]
        x = listOfImageCoordinates[i95 + 1][0]
        y = listOfImageCoordinates[i95 + 1][1]
        z = [i95 + 1][2]

        i95 = i95 + 1
        print x0
        print y0
        print x
        print y
        print i95

        if abs(x - x0) >= abs(y - y0):
            line_pos_num = int(abs(x - x0)) + 1

        else:
            line_pos_num = int(abs(y - y0)) + 1

        Line_Pos[0][0] = x0
        Line_Pos[0][1] = y0
        Line_Pos[0][2] = 2

        for num1 in range(1, line_pos_num + 1):
            Line_Pos[num1][0] = x0 + (x - x0) / line_pos_num * (num1 - 1)
            Line_Pos[num1][1] = y0 + (y - y0) / line_pos_num * (num1 - 1)
            Line_Pos[num1][2] = z0 + (z - z0) / line_pos_num * (num1 - 1)

        Line_Pos[line_pos_num + 1][0] = Line_Pos[line_pos_num][0]
        Line_Pos[line_pos_num + 1][1] = Line_Pos[line_pos_num][1]
        Line_Pos[line_pos_num + 1][2] = Line_Pos[line_pos_num][2] + 2
        Line_Pos[line_pos_num + 2][0] = (x - x0) / 2
        Line_Pos[line_pos_num + 2][1] = (y - y0) / 2
        Line_Pos[line_pos_num + 2][2] = 2
        point1_num = line_pos_num + 2

        for num in range(0, point1_num):

            if Line_Pos[num][0] >= 25:
                pen_offset = -0.2

            elif Line_Pos[num][0] <= 9:
                pen_offset = 0.1

            else:
                pen_offset = 0

            New_Line_Pos[num] = pen_length - base_heigh + Line_Pos[num][2] + pen_offset

            if (New_Line_Pos[num]) == 0:
                New_Line_Pos[num] = 0.00001

            c2[num] = math.sqrt((Line_Pos[num][0]) * (Line_Pos[num][0]) + (Line_Pos[num][1]) * (Line_Pos[num][1]))
            c1[num] = math.sqrt(
                Line_Pos[num][0] * Line_Pos[num][0] + Line_Pos[num][1] * Line_Pos[num][1] + New_Line_Pos[num] *
                New_Line_Pos[num]);

            # base angle
            Angle_Pos[num][0] = math.atan(Line_Pos[num][1] / Line_Pos[num][0]);
            Angle_Degree[num][0] = Angle_Pos[num][0] / pi * 180;

            # upper_angle
            upper_angle1[num] = math.atan(New_Line_Pos[num] / c2[num]);

            upper_angle2[num] = math.acos(
                (c1[num] * c1[num] + upper_arm_length * upper_arm_length - fore_arm_length * fore_arm_length) / (
                    2 * c1[num] * upper_arm_length));

            Angle_Pos[num][1] = upper_angle1[num] + upper_angle2[num];
            Angle_Degree[num][1] = Angle_Pos[num][1] / pi * 180;

            # fore_angle
            fore_angle1[num] = math.acos(
                (c1[num] * c1[num] + fore_arm_length * fore_arm_length - upper_arm_length * upper_arm_length) / (
                    2 * c1[num] * fore_arm_length));

            fore_angle2[num] = math.atan(c2[num] / New_Line_Pos[num]);
            Angle_Pos[num][2] = fore_angle1[num] + fore_angle2[num] - pi / 2;

            # if Angle_Pos[num][2] < 0:

            #    Angle_Pos[num][2] = pi + Angle_Pos[num][2]

            Angle_Degree[num][2] = Angle_Pos[num][2] / pi * 180;
            servo0_output = 360 + Angle_Degree[num][0] * 168 / 75

            # servo0_output = int(servo0_output)
            # servo1_output = 245 + Line_Pos[num][1] * 250/125
            servo1_output = 230 + Angle_Degree[num][1] * 253 / 120
            # servo1_output = int(servo1_output)
            servo2_output = 280 + Angle_Degree[num][2] * 220 / 70
            # servo2_output = int(servo2_output)
            # servo2_output = 280 + Line_Pos[num][2] * 195/68
            # print(servo0_output)
            # print(servo1_output)
            # print(servo2_output)

            if (abs(servo0_output - old_servo0_output)) >= (abs(servo1_output - old_servo1_output)):

                step_num = int((abs(servo0_output - old_servo0_output))) + 1

            elif (abs(servo1_output - old_servo1_output)) >= (abs(servo2_output - old_servo2_output)):

                step_num = int((abs(servo1_output - old_servo1_output))) + 1

            else:

                step_num = int((abs(servo2_output - old_servo2_output))) + 1

            tmp_servo0_output = old_servo0_output
            tmp_servo1_output = old_servo1_output
            tmp_servo2_output = old_servo2_output
            old_servo0_output = servo0_output
            old_servo1_output = servo1_output
            old_servo2_output = servo2_output

            for line_num in range(0, step_num + 1):
                servo0_output = tmp_servo0_output + (old_servo0_output - tmp_servo0_output) * line_num / step_num
                servo0_output = int(servo0_output)
                servo1_output = tmp_servo1_output + (old_servo1_output - tmp_servo1_output) * line_num / step_num
                servo1_output = int(servo1_output)
                servo2_output = tmp_servo2_output + (old_servo2_output - tmp_servo2_output) * line_num / step_num
                servo2_output = int(servo2_output)
                pwm.set_pwm(0, 0, servo0_output)
                pwm.set_pwm(4, 0, servo1_output)
                pwm.set_pwm(8, 0, servo2_output)

                # print('The position of Servo0 is %d',servo0_output)

                # print('The position of Servo1 is %d',servo1_output)

                # print('The position of Servo2 is %d',servo2_output)

                # time.sleep(0.3)

    else:

        # termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        break
