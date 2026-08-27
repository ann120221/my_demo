from vehicle_state import VehicleState
from carla_interface.carla_client import CarlaClient

from carla_interface.carla_sensor import Sensor
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

		#初始化传感器
		self.sensor1 = Sensor(
			self.carla_client1.world1,
			self.carla_client1.vehicle
		)

		#创建好文件夹、进程和相机
		self.recorder = CarlaRecorder()
		self.recorder.set_recording_files(
			self.sensor1.set_record_camera()
			)


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
		#print(f"发送的控制指令如下：")
		print(f"speed:{self.vehicle_state1.speed}")
		#print(f"brake:{self.command.brake}")
		#print(f"throttle:{self.command.throttle}")
		#print(f"steer:{self.command.steer}")

		self.carla_client1.receive_control(command)

	def step(self):
		"""同步模式下推进一个仿真步"""

		if self.carla_client1.synchronous_mode:
			self.carla_client1.step()


	def switch_synchronous_mode(self,synchronous_mode = False):
		"""开关同步模式"""

		self.carla_client1.switch_synchronous_mode(synchronous_mode)

	def start_recoding(self):
		"""启动进程和相机"""

		self.recorder.start_recodering()
		self.sensor1.start_camera()

	def stop_recording(self):
		"""停止相机、进程后，销毁相机"""
		#相机停止
		self.sensor1.stop_camera()

		#停止进程并生成视频
		self.recorder.stop_recording()

		#销毁相机
		self.sensor1.destroy_camera()

	def frame_recoder(self):
		"""获取当前帧的图片并传入recorder进行保存"""
		self.recorder.submit(self.sensor1.get_image())




		

