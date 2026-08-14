from control.controller import Controller
from carla_interface.carla_interface import CarInterface
from control.control_command import ControlCommand


DestoryVehicle_or_not = False


def main():

	controller1 = Controller()
	carInterface1 = CarInterface()

	carInterface1.switch_synchronous_mode(True)

	for _ in range(2000):
		vehicle_state1 = carInterface1.update()
		command = controller1.update(vehicle_state1)
		carInterface1.send_control(command)
		carInterface1.step()

	print(f"控制结束，控制车辆停止")
	stopcommand = ControlCommand()
	stopcommand.brake = 1.0 
	stopcommand.throttle = 0.0 
	stopcommand.steer = 0.0

	while True:
		vehicle_speed1 = carInterface1.update().speed

		if vehicle_speed1 < 0.05:
			carInterface1.switch_synchronous_mode(False)
			break
		else:
			carInterface1.send_control(stopcommand)
			carInterface1.step()


if __name__ == "__main__":
	main()