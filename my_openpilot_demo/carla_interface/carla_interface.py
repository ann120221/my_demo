from vehicle_state import VehicleState
from control.control_command import ControlCommand

class CarInterface:
    """获取状态、发送控制"""
    def __init__(self):
        self.fake_vehiclestate = VehicleState()
        self.fakecommand = ControlCommand()

    def update(self):
        """获取实时状态并记录快照"""
        self.vehicle_state1 = VehicleState()
        
        self.vehicle_state1.speed = self.fake_vehiclestate.speed 

        
        return self.vehicle_state1
    
    def send_control(self,command):
        """发送控制命令"""
        self.command = command
        self.fakecommand =self.command
        print(f"speed:{self.vehicle_state1.speed}")
        print(f"brake:{self.command.brake}")
        print(f"throttle:{self.command.throttle}")
        print(f"steer:{self.command.steer}")
        if self.fakecommand.throttle == 1 :self.fake_vehiclestate.speed += 1
        if self.fakecommand.brake == 1 : self.fake_vehiclestate.speed -= 1
