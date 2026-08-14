

class VehicleState:
    """用于存储控制算法所需车辆动态数据的类"""

    """"
    当前 CARLA 阶段暂时直接使用仿真真值代替测量和状态估计结果
    """
    def __init__(self):

        self.x = 0
        self.y = 0
        self.yaw = 0

        self.steering_angle = 0
        self.acceleration = 0
        self.speed = 0




