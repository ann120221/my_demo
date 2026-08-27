
#获取文件当前路径
from pathlib import Path
#系统时间
from datetime import datetime
#队列
import queue
import subprocess

import shutil

#线程
import threading

class CarlaRecorder:
	"""负责取得数据，把数据存在磁盘里"""
	def __init__(self):
		self.submit_index = 0

	def submit(self,image = None):
		"""接收image数据"""

		if image  is None:raise RuntimeError("recorder没有成功接受到图片")
	
		self.save_queue.put(image)
		self.submit_index += 1

		if self.submit_index % 50 == 0:
			print(
				f"已提交:{self.submit_index}, "
				f"已保存:{self.frame_index}, "
				f"队列积压:{self.save_queue.qsize()}"
			)

	def set_recording_files(self,sensor_name = None):
		"""创建文件和线程"""

		self.save_queue = queue.Queue(maxsize=1400)
		self.frame_index = 0
		self.sensor_name = sensor_name

		#定义保存文件的名字
		time_str = datetime.now().strftime("%m%d_%H%M%S")
		experiment_name = f"{time_str}experiment"

		#定义保存路径
		project_root = Path(__file__).resolve().parent.parent
		experiment_dir = project_root / "recordings" / experiment_name
		sensor_dir = experiment_dir / "sensors" / self.sensor_name
		frame_dir = sensor_dir / "frames"


		self.sensor_dir = sensor_dir
		self.frame_dir = frame_dir

		#创建实验目录
		frame_dir.mkdir(
			parents = True,
			exist_ok = True 
		)

		#创建保存线程
		self.save_thread = threading.Thread(
			target = self.save_worker
		)


	def save_worker(self):
		"""获取save_queue中的image并保存为png图片"""

		while(True):
			#定义保存文件名及路径
			file_name = (f"{self.frame_index:06d}.png")
			file_path = self.frame_dir / file_name

			#获取图片并保存
			image = self.save_queue.get()

			#当读取到save_queue中的None后退出循环
			if image is None:
				break
			else:
				image.save_to_disk(str(file_path))

			self.frame_index += 1

	def start_recodering(self):
		"""启动用于保存图片的后台进程"""

		self.save_thread.start()




	def stop_recording(self):
		"""把图片合成为视频并停止记录"""

		if shutil.which("ffmpeg") is None:
			raise RuntimeError(
			"未检测到 ffmpeg,请先安装:apt install -y ffmpeg"
			)

		#在停止相机的基础上停止后台线程，绝对不要直接销毁相机
		self.save_queue.put(None)
		self.save_thread.join()

		if self.frame_index == 0:
			print("没有录像帧，无法生成视频")
			return

		# 设置视频输出位置
		video_path = self.sensor_dir / "demo.mp4"

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