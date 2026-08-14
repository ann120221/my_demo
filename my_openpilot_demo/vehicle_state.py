

class VehicleState:
    """"
    保存控制器可用的状态
    当前 CARLA 阶段暂时直接使用仿真真值代替测量和状态估计结果
    """
    def __init__(self):
        """车辆自身"""
        self.x = 0
        self.y = 0
        self.yaw = 0

        self.steering_angle = 0
        self.acceleration = 0
        self.speed = 0




