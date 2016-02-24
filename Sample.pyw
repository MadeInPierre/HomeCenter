################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    last_gesture_dic = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    last_time_gesture_triggered = 1.0

    def IsBetween(self, value, minimum, maximum):
        if value <= maximum and value >= minimum:
            return True
        else:
            return False

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        '''
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        # Get hands

        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print "  %s, id %d, position: %s" % (
            #    handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            #print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #    direction.pitch * Leap.RAD_TO_DEG,
            #    normal.roll * Leap.RAD_TO_DEG,
            #    direction.yaw * Leap.RAD_TO_DEG)

        # Get gestures
        for gesture in frame.gestures():

            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)


            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
##                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
##                        gesture.id, self.state_names[gesture.state],
##                        swipe.position, swipe.direction, swipe.speed)
                if self.state_names[gesture.state] == "STATE_END":
                    if swipe.direction[0] < -0.9 and self.IsBetween(swipe.direction[1], -0.3, 0.3): # LEFT
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onLeft()
                            self.last_time_gesture_triggered = time.time()
                    elif swipe.direction[0] > 0.9 and self.IsBetween(swipe.direction[1], -0.3, 0.3): # RIGHT
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onRight()
                            self.last_time_gesture_triggered = time.time()

                    elif swipe.direction[1] > 0.9 and self.IsBetween(swipe.direction[0], -0.3, 0.3): # UP
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onUp()
                            self.last_time_gesture_triggered = time.time()
                    elif swipe.direction[1] < -0.9 and self.IsBetween(swipe.direction[0], -0.3, 0.3): # DOWN
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onDown()
                            self.last_time_gesture_triggered = time.time()

                    elif self.IsBetween(swipe.direction[1], 0.55, 0.85) and self.IsBetween(swipe.direction[2], -0.85, -0.55) and self.IsBetween(swipe.direction[0], -0.3, 0.3): # UP
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onUp()
                            self.last_time_gesture_triggered = time.time()
                    elif self.IsBetween(swipe.direction[1], -0.85, -0.55) and self.IsBetween(swipe.direction[2], 0.55, 0.85) and self.IsBetween(swipe.direction[0], -0.3, 0.3): # DOWN
                        if time.time() >= self.last_time_gesture_triggered + 0.2:
                            self.onDown()
                            self.last_time_gesture_triggered = time.time()
    def onLeft(self):
        print "<<< LEFT <<<"
    def onRight(self):
        print "                 >>> RIGHT >>>"
    def onUp(self):
        print "         AAA UP AAA"
    def onDown(self):
        print "         vvv DOWN vvv"



def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    while True:
        pass

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
