import carla


class CarlaClient:
	"""获取动态,静态数据"""
	def __init__(self):
		"""设置当前world需要生成的车型blueprint,位置transform的静态数据"""

		client1 = carla.Client("localhost",2100)
		client1.set_timeout(5.0)

		self.world1 = client1.get_world()
		self.blueprint_library=self.world1.get_blueprint_library()
		dodge_list = self.blueprint_library.filter("vehicle.dodge.*")
		if len(dodge_list) == 0:
			raise RuntimeError("未找到道格的车型")

		map1 = self.world1.get_map()
		spawn_points = map1.get_spawn_points()
		

		self.vehicle_blueprint = dodge_list[0]
		self.spawn_point = spawn_points[0]
		print(f"生成车型为:{self.vehicle_blueprint.id},生成位置:{self.spawn_point.location}")

	def create_vehicle(self):
		"""生成指定车辆"""

		self.vehicle = self.world1.try_spawn_actor(
			self.vehicle_blueprint,
			self.spawn_point
		)
		if self.vehicle is None:
			raise RuntimeError("车辆生成失败")
		

	def set_spectator(self):
		"""自由视角位置切换到车附近"""

		spectator = self.world1.get_spectator()
		vehicle_transform = self.vehicle.get_transform()

		spectator_transform = carla.Transform(
			carla.Location(
				x = vehicle_transform.location.x - 10,
				y = vehicle_transform.location.y,
				z = vehicle_transform.location.z + 5
			),
			carla.Rotation(
				pitch = vehicle_transform.rotation.pitch - 10,
				yaw = vehicle_transform.rotation.yaw,
				roll = vehicle_transform.rotation.roll 
			)
		)

		spectator.set_transform(spectator_transform)

	def clean_vehicle(self,radius = 10):
		"""
		获取地图中车和行人的位置，逐一判断距离目标生成点的距离，删除距离近的
		"""
		"""
		需要注意的是:
		1.actor没有actor.location属性,需要用get_location方法获取位置
		2.actor中有很多内容,包括交通灯、传感器、spectator 等,所以最好指定范围删除，而不是指定不删的
		"""
		spawn_location = self.spawn_point.location
		actors = self.world1.get_actors()
		clean_list = []

		clean_list .extend(actors.filter("vehicle.*"))
		clean_list .extend(actors.filter("walker.pedestrian.*"))

		for actor in clean_list:
			actor_location = actor.get_location()
			distance = spawn_location.distance(actor_location)
			if distance < radius  :
				actor.destroy()
				print (f"删除了距离目标{distance}米的{actor.type_id}")

	def update(self):
		"""获取carla 服务器端的车辆状态"""

		"""
		vt指的是vehicle_state_transform
		vv指的是vehicle_state_velocity
		vs指的是vehicle_state_speed
		va指的是vehicle_state_acceleration
		"""
		self.vt = self.vehicle.get_transform()
		self.vv = self.vehicle.get_velocity()
		self.vs = self.vv.length()
		self.va = self.vehicle.get_acceleration()
		return self.vt,self.vs,self.va

	def receive_control(self,command = None):
		"""根据controlcommand的控制指令控制车辆"""

		vehicle_control = carla.VehicleControl(
			throttle = command.throttle, 
			steer = command.steer ,
			brake = command.brake 
			)
		self.vehicle.apply_control(vehicle_control)






if __name__ == "__main__":
	carla_client = CarlaClient()
	carla_client.clean_vehicle()
	carla_client.create_vehicle()
	carla_client.set_spectator()
	carla_client.update()
