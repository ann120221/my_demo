from vehicle_state import VehicleState
from carla_interface.carla_client import CarlaClient

class CarInterface:
	"""通过CARLA获取状态、返回控制"""

	def __init__(self):
		"""初始化，创建指定车辆"""
		self.fake_vehiclestate = VehicleState()
		self.carla_client1 = CarlaClient()
		self.carla_client1.clean_spawn_point_vehicle(10)
		self.carla_client1.clean_role("ego_vehicle")
		self.carla_client1.create_vehicle()
		self.carla_client1.set_spectator()

	def update(self):
		"""获取实时状态并记录快照"""

		self.vehicle_state1 = VehicleState()

		vt, vs ,va = self.carla_client1.update()
		self.vehicle_state1.speed = vs
		
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

	def step(self):
		"""同步模式下推进一个仿真步"""

		if self.carla_client1.synchronous_mode:
			self.carla_client1.step()

	def switch_synchronous_mode(self,synchronous_mode = False):
		"""开关同步模式"""

		self.carla_client1.switch_synchronous_mode(synchronous_mode)
		

