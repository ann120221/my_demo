from control.controller import Controller
from carla_interface.carla_interface import CarInterface

def main():

    controller1 = Controller()
    carInterface1 = CarInterface()
    for _ in range(20):
        vehicle_state1 = carInterface1.update()
        command = controller1.update(vehicle_state1)
        carInterface1.send_control(command)


if __name__ == "__main__":
    main()