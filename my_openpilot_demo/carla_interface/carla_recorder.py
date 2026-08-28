
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

#启动gpu进行编码
USE_GPU_ENCODING = True

#一秒内保存的图片数
PICTURE_HZ = 2

#视频帧率
FPS = 20

class CarlaRecorder:
	"""负责取得数据，把数据存在磁盘里"""

	def __init__(self):
		self.submit_index = 0
		self.picture_index = 0
		self.frame_video_index = 0
		self.timer = 0.0

		self.fps = FPS
		self.picture_hz = PICTURE_HZ

		if shutil.which("ffmpeg") is None:
			raise RuntimeError(
			"未检测到 ffmpeg,请先安装:apt install -y ffmpeg"
			)
		elif self.picture_hz == 0 :
			raise RuntimeError("图片存储频率为0,无法保存图片")

		elif self.picture_hz > self.fps  :
			self.picture_hz = self.fps 
		
		



	def set_recording_files(self,sensor_name = None):
		"""创建文件和线程,准备ffmpeg"""

		if sensor_name is None:
			raise RuntimeError(
			"传感器未命名"
			)
		
		#video_queue负责保存用于生成录像的images;picture_queue用于保存部分用于可视化分析的images。
		#当queue的达到maxsize=60，会让仿真等待queue中的images处理到60以下再运行下一帧
		self.video_queue = queue.Queue(maxsize=60)
		self.picture_queue = queue.Queue(maxsize=60)

		#定义保存文件的名字
		time_str = datetime.now().strftime("%m%d_%H%M%S")
		experiment_name = f"{time_str}experiment"

		#定义保存文件路径
		project_root = Path(__file__).resolve().parent.parent
		experiment_dir = project_root / "recordings" / experiment_name
		sensor_dir = experiment_dir / "sensors" / sensor_name
		self.frame_dir = sensor_dir / "frames"

		# 定义视频输出路径
		video_path = sensor_dir / "demo.mp4"


		#创建实验目录
		self.frame_dir.mkdir(
			parents = True,
			exist_ok = True 
		)


		#创建保存图片线程
		self.save_pictures_thread = threading.Thread(
			target = self.save_pictures_worker
		)

		#创建保存视频线程
		self.save_video_thread = threading.Thread(
			target = self.save_video_worker
		)


		#定义ffmpeg生成需要的各项参数
		#输入：960x540 ,BGRA ,rawvideo,20 FPS,来自stdin
		#编码：RTX NVENC ,H264
		#输出：yuv420p ,MP4
		if USE_GPU_ENCODING :
			self.command = [
				"ffmpeg",
				"-y",

				#输入
				"-f","rawvideo",
				"-pix_fmt","bgra",
				"-s","960x540",
				"-r",str(self.fps),
				"-i","-",

				#编码
				"-c:v","h264_nvenc",
				"-preset","p1",
				"-pix_fmt","yuv420p",

				#输出
				str(video_path)

			]
		else:
			self.command = [
				"ffmpeg",
				"-y",

				#输入
				"-f","rawvideo",
				"-pix_fmt","bgra",
				"-s","960x540",
				"-r",str(self.fps),
				"-i","-",

				#编码
				"-c:v","libx264",
				"-preset","veryfast",
				"-pix_fmt","yuv420p",

				#输出
				str(video_path)

			]

		

	def submit(self,image = None):
		"""接收image数据并分配数据到对应queue"""

		if image  is None:
			raise RuntimeError("recorder没有成功接收到图片")


		#时间累积法选取关键帧存储为图片
		self.timer += 1 / self.fps
		if self.timer >= 1 / self.picture_hz:
			self.picture_queue.put(image)
			self.timer -= 1 / self.picture_hz

		self.video_queue.put(image)

		self.submit_index += 1

		if self.submit_index % 100 == 0:
			print(
				f"已提交:{self.submit_index}, ",
				f"已保存图片:{self.picture_index}, ",
				f"已保存视频帧数:{self.frame_video_index}",

				f"图片保存队列积压:{self.picture_queue.qsize()}",
				f"保存视频帧队列积压:{self.video_queue.qsize()}"
			)

	
	def save_pictures_worker(self):
		"""获取picture_queue中的image并保存为png图片"""

		
		while(True):

			#获取图片
			image = self.picture_queue.get()

			#当读取到save_queue中的None后退出循环，否则保存到磁盘
			if image is None:
				break
			else:
				#定义保存文件名及路径，图片名对应的是视频的帧数，而不是图片序数

				file_name = (f"{image.frame:06d}.png")
				file_path = self.frame_dir / file_name

				#保存图片
				image.save_to_disk(str(file_path))

				self.picture_index += 1
	

	def save_video_worker(self):
		"""把video_queue的image的image.raw_date通过subprocess.stdin管道传进进程ffmpge处理"""
		while(True):
			image = self.video_queue.get()

			if image is None:
				break
			else:

				#carla.Image对象有image.frame、image.timestamp、image.raw_data等属性
				#RGB Camera 实际输出的是 BGRA 排列的image.raw_data，需要转换成可以直接写入 pipe 的二进制数据。
				self.ffmpeg_process.stdin.write(bytes(image.raw_data))

			
				self.frame_video_index += 1



	def start_recoding(self):
		"""启动保存图片和视频的后台进程"""

		#启动ffmpeg进程
		self.ffmpeg_process = subprocess.Popen(
			self.command,
			stdin = subprocess.PIPE
		)
		self.save_pictures_thread.start()
		self.save_video_thread.start()


	def stop_recording(self):
		"""结束进程，生成视频"""

		#对录像&图片保存线程发出停止信号
		self.picture_queue.put(None)
		self.video_queue.put(None)

		#停止保存录像的进程
		self.save_video_thread.join()

		#关闭ffmpeg_process与python的数据管道
		self.ffmpeg_process.stdin.close()

		#数据传输完毕，开始生成视频
		return_code =self.ffmpeg_process.wait()

		if return_code == 0 :
			print(f"视频编码完成")
		else:
			raise RuntimeError("ffmpeg出现异常")

		
		self.save_pictures_thread.join()
		print("图片保存完成")




