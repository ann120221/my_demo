from control.control_command import ControlCommand 
from control.lateral_pureursuit import LateralPurePursuit
from control.longitudinal_pid import LongitudinalPID

class Controller:
    """控制算法"""
    
    def __init__(self):
        pass

    def update(self,vehicle_state,reference_path):
        """根据传入实时状态更新控制指令"""

        self.vehicle_state = vehicle_state
        self.cc = ControlCommand()
        longigtudinal = LongitudinalPID()
        lateral = LateralPurePursuit()

        #计算控制,返回控制结果
        self.cc.throttle, self.cc.brake = longigtudinal.update(vehicle_state.speed,20)
        self.cc.steer = lateral.update(vehicle_state,reference_path)
        
        return self.cc
        


