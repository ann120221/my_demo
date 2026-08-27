import carla
import queue

class Sensor:
	"""负责产出图片等数据"""

	def __init__(self, world = None,vehicle = None):
		"""获取世界及车辆"""

		self.record_camera1_queue = queue.Queue(maxsize=800)

		if vehicle is None:
			raise RuntimeError("车辆没有生成，无法记录")
		else:self.vehicle = vehicle

		if world is None:
			raise RuntimeError("没有获取到对应,carla世界")
		else:
			self.world1 = world
			



	def set_record_camera(self):
		"""
		创建记录用相机
			返回相机名
			"""

		camera_blueprint_id ="sensor.camera.rgb"
		camera_name = "record_camera"

		#设置记录用相机的生成类型
		blueprint_library=self.world1.get_blueprint_library()
		record_camera_blueprint = blueprint_library.find(camera_blueprint_id)
		record_camera_blueprint.set_attribute("role_name","record_camera1")
		record_camera_blueprint.set_attribute("fov","90")
		record_camera_blueprint.set_attribute("image_size_x","960")
		record_camera_blueprint.set_attribute("image_size_y","540")
		record_camera_blueprint.set_attribute("sensor_tick","0.05")

		#设置生成相机相对于车的变换。因为生成的时候会进行绑定，所以要写相对位置
		record_camera_transform = carla.Transform(
			carla.Location(
				x = -20,
				y = 0,
				z = + 3
			),
			carla.Rotation(
				pitch = +10,
				yaw = 0,
				roll = 0
			)
		)

		#生成相机
		self.record_camera = self.world1.spawn_actor(
			record_camera_blueprint,
			record_camera_transform,
			attach_to = self.vehicle,
			attachment_type = carla.AttachmentType.SpringArmGhost
		)

		return camera_name

	def start_camera(self):
		"""启动相机"""

		#启动把相机监听到的图片放进队列
		self.record_camera.listen(self.record_camera1_queue.put)

	def get_image(self):
		"""获取队列中的数据"""

		return self.record_camera1_queue.get()

	def stop_camera(self):
		"""停止相机"""
		self.record_camera.stop()

	def destroy_camera(self):
		"""销毁相机"""
		self.record_camera.destroy()
