import time
import tellopy

def main():
    drone = None

    try:
        drone = tellopy.Tello()
        print("Battery:", drone.battery())
    except Exception as err:
        print(err)

    # Commands go here:

    # Make sure to avoid the obstacles #
    drone.takeoff()
    time.sleep(3)


    #drone.forward(20)
    #time.sleep(3)

    #drone.flip('f')
    #time.sleep(3)

    drone.cw(90)
    time.sleep(3)

    drone.land()
    time.sleep(3)

    print("Battery is at:", drone.battery())
    print("You have flied for ", drone.flight_time())
