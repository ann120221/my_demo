import carla
from pathlib import Path
from datetime import datetime
import queue
import subprocess

import shutil

class CarlaRecorder:

	def __init__(self, world = None,vehicle = None):
		#定义存放照片的变量
		self.image_queue = queue.Queue()

		if vehicle is None:
			raise RuntimeError("车辆没有生成，无法记录")
		else:self.vehicle = vehicle

		if world is None:
			raise RuntimeError("没有获取到对应,cara世界")
		else:
			self.world1 = world
			blueprint_library=self.world1.get_blueprint_library()

			#设置记录用相机的生成类型
			self.record_camera_blueprint = blueprint_library.find("sensor.camera.rgb")
			self.record_camera_blueprint.set_attribute("role_name","record_camera1")
			self.record_camera_blueprint.set_attribute("fov","90")
			self.record_camera_blueprint.set_attribute("image_size_x","960")
			self.record_camera_blueprint.set_attribute("image_size_y","540")
			self.record_camera_blueprint.set_attribute("sensor_tick","0.05")



	def start_recording(self):
		"""初始化并开始记录"""

		#确定文件路径
		project_root = Path(__file__).resolve().parent.parent

		#定义保存文件
		time_str = datetime.now().strftime("%m%d_%H%M%S")
		experiment_name = f"{time_str}experiment"
		experiment_dir = project_root / "recordings" / experiment_name
		frame_dir = experiment_dir / "frames"

		#创建文件
		frame_dir.mkdir(
			parents = True,
			exist_ok = True 
		)

		self.expriment = experiment_dir
		self.frame_dir = frame_dir
		self.frame_index = 0

		#设置生成相机相对于车的变换。因为生成的时候会进行绑定，所以要写相对位置
		record_camera_transform = carla.Transform(
			carla.Location(
				x = -20,
				y = 0,
				z = + 3
			),
			carla.Rotation(
				pitch =+10,
				yaw = 0,
				roll = 0
			)
		)

		#生成相机
		self.record_camera = self.world1.spawn_actor(
			self.record_camera_blueprint,
			record_camera_transform,
			attach_to = self.vehicle,
			attachment_type = carla.AttachmentType.SpringArmGhost
		)

		self.record_camera.listen(self.image_queue.put)


	def record_frame(self):
		"""获取queue中的image并保存为png图片"""

		#定义保存文件名及路径
		file_name = (f"{self.frame_index:06d}.png")
		file_path = self.frame_dir / file_name

		#获取图片并保存
		image = self.image_queue.get()
		image.save_to_disk(str(file_path))

		self.frame_index += 1

		return image

	def stop_recording(self):
		"""把图片合成为视频并停止记录"""

		if shutil.which("ffmpeg") is None:
			raise RuntimeError(
			"未检测到 ffmpeg,请先安装:apt install -y ffmpeg"
			)
		self.record_camera.stop()
		self.record_camera.destroy()

		if self.frame_index == 0:
			print("没有录像帧，无法生成视频")
			return

		# 设置视频输出位置
		video_path = self.expriment / "demo.mp4"

		# 图片序列格式
		input_path = self.frame_dir / "%06d.png"

		fps = 20

		#调用ffmpeg生成视频
		command = [
			"ffmpeg",
			"-y",
			"-framerate", str(fps),
			"-start_number", "0",
			"-i", str(input_path),
			"-c:v", "libx264",
			"-pix_fmt", "yuv420p",
			str(video_path)
		]

		print("正在生成视频...")

		subprocess.run(
			command,
			check=True
		)

		print(f"视频生成完成：{video_path}")