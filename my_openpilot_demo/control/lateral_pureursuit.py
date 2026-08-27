import math


class LateralPurePursuit:
    """Pure Pursuit横向轨迹跟踪"""

    def __init__(
        self,
        wheelbase=2.9,
        lookahead_base=4.0,
        lookahead_gain=0.3,
        max_steer_angle_deg=35.0
    ):
        self.wheelbase = wheelbase

        self.lookahead_base = lookahead_base
        self.lookahead_gain = lookahead_gain

        self.max_steer_angle = math.radians(
            max_steer_angle_deg
        )

    def update(self, vehicle_state, reference_path):

        if len(reference_path) == 0:
            return 0.0

        # --------------------------------
        # 1. 根据速度确定前视距离
        # --------------------------------

        lookahead_distance = (
            self.lookahead_base
            + self.lookahead_gain * vehicle_state.speed
        )

        # --------------------------------
        # 2. 在参考轨迹中寻找目标点
        # --------------------------------

        target_point = reference_path[-1]

        for point in reference_path:

            dx = point[0] - vehicle_state.x
            dy = point[1] - vehicle_state.y

            distance = math.sqrt(
                dx ** 2 + dy ** 2
            )

            if distance >= lookahead_distance:
                target_point = point
                break

        # --------------------------------
        # 3. 车辆 -> 目标点向量
        # --------------------------------

        target_x = target_point[0]
        target_y = target_point[1]

        dx = target_x - vehicle_state.x
        dy = target_y - vehicle_state.y

        # 实际车辆到目标点距离
        ld = math.sqrt(dx ** 2 + dy ** 2)

        if ld < 0.001:
            return 0.0

        # --------------------------------
        # 4. 求目标方向
        # --------------------------------

        target_angle = math.atan2(dy, dx)

        vehicle_yaw = math.radians(
            vehicle_state.yaw
        )

        alpha = target_angle - vehicle_yaw

        # 把角度限制到 [-pi, pi]
        alpha = (
            alpha + math.pi
        ) % (2 * math.pi) - math.pi

        # --------------------------------
        # 5. Pure Pursuit公式
        # --------------------------------

        steering_angle = math.atan2(
            2.0
            * self.wheelbase
            * math.sin(alpha),
            ld
        )

        # --------------------------------
        # 6. 转成CARLA [-1, 1]
        # --------------------------------

        steer = (
            steering_angle
            / self.max_steer_angle
        )

        steer = max(
            -1.0,
            min(1.0, steer)
        )

        return steer