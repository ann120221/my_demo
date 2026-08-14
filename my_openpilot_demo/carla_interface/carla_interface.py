from vehicle_state import VehicleState
from carla_interface.carla_client import CarlaClient

class CarInterface:
	"""获取状态、发送控制"""
	def __init__(self):
		"""初始化，创建指定车辆"""
		self.fake_vehiclestate = VehicleState()
		self.carla_client1 = CarlaClient()
		self.carla_client1.clean_vehicle()
		self.carla_client1.create_vehicle()
		self.carla_client1.set_spectator()

	def update(self):
		"""获取实时状态并记录快照"""
		self.vehicle_state1 = VehicleState()

		carla_vehicle_state = self.carla_client1.update()
		self.vehicle_state1.speed = carla_vehicle_state[1]
		
		return self.vehicle_state1
	
	def send_control(self,command):
		"""发送控制命令"""
		self.command = command
		print(f"发送的控制指令如下：")
		print(f"speed:{self.vehicle_state1.speed}")
		print(f"brake:{self.command.brake}")
		print(f"throttle:{self.command.throttle}")
		print(f"steer:{self.command.steer}")

		self.carla_client1.receive_control(command)
		

