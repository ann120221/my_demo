from control.controller import Controller
from carla_interface.carla_interface import CarInterface
from control.control_command import ControlCommand


DestoryVehicle_or_not = False


def main():

	controller1 = Controller()
	carInterface1 = CarInterface()

	#开启同步模式
	carInterface1.switch_synchronous_mode(True)

	#启动进程和相机
	carInterface1.start_recoding()

	for _ in range(800):
		vehicle_state1,reference_path = carInterface1.update()
		command = controller1.update(vehicle_state1,reference_path)
		carInterface1.send_control(command)
		carInterface1.step()
		carInterface1.frame_recoder()



	print(f"循环结束，开始控制车辆停止")
	stopcommand = ControlCommand()
	stopcommand.brake = 1.0 
	stopcommand.throttle = 0.0 
	stopcommand.steer = 0.0

	while True:
		vehicle_state1, _ = carInterface1.update()
		vehicle_speed1 = vehicle_state1.speed

		if vehicle_speed1 < 0.05:
			carInterface1.stop_recording()
			break
		
		carInterface1.send_control(stopcommand)
		carInterface1.step()
		carInterface1.frame_recoder()




if __name__ == "__main__":
	main()