class LongitudinalPID:
    """纵向速度PID控制器"""

    def __init__(
        self,
        kp=0.30,
        ki=0.05,
        kd=0.02,
        dt=0.05
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, current_speed, target_speed):

        # 1. 当前速度误差
        error = target_speed - current_speed

        # 2. 积分项
        self.integral += error * self.dt

        # 防止积分无限增长
        self.integral = max(
            -10.0,
            min(10.0, self.integral)
        )

        # 3. 微分项
        derivative = (
            error - self.previous_error
        ) / self.dt

        # 4. PID
        output = (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )

        self.previous_error = error

        # PID统一限制为 [-1, 1]
        output = max(-1.0, min(1.0, output))

        # 5. 分配给油门/刹车
        if output >= 0:
            throttle = output
            brake = 0.0
        else:
            throttle = 0.0
            brake = -output

        return throttle, brake