from control.control_command import ControlCommand 

class Controller:
    def __init__(self):
        pass

    def update(self,vehicle_state):
        self.vehicle_state = vehicle_state
        self.cc = ControlCommand()
        #计算控制,返回控制结果
        if self.vehicle_state.speed < 10 :
            self.cc.throttle = 1
        else:
            self.cc.throttle = 0
            self.cc.brake = 1
        return self.cc
        


