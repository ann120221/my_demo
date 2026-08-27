from vehicle_state import VehicleState
from carla_interface.carla_client import CarlaClient
from carla_interface.carla_recorder import CarlaRecorder

class CarInterface:
	"""通过CARLA获取状态、返回控制"""

	def __init__(self):
		"""初始化，创建指定车辆"""
		self.fake_vehiclestate = VehicleState()
		self.carla_client1 = CarlaClient()

		#打扫场景
		self.carla_client1.clean()

		#初始化演员
		self.carla_client1.create_vehicle()
		self.carla_client1.set_spectator()

		#开始记录
		self.recorder = CarlaRecorder(
			self.carla_client1.world1,
			self.carla_client1.vehicle
		)
		self.recorder.start_recording()



	def update(self):
		"""获取当前VehicleState和局部参考路径"""

		vehicle_state = VehicleState()

		vt, vs, va = self.carla_client1.update()

		vehicle_state.x = vt.location.x
		vehicle_state.y = vt.location.y
		vehicle_state.yaw = vt.rotation.yaw
		vehicle_state.speed = vs

		reference_path = self.carla_client1.get_reference_path()

		self.vehicle_state1 = vehicle_state
		self.reference_path = reference_path

		return vehicle_state, reference_path
	
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

	def stop_recording(self):
		self.recorder.stop_recording()

	def frame_recoder(self):
		self.recorder.record_frame()




		

