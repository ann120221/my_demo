import carla

class Client:
    """获取world,vehicle,state,"""
    def __init__(self):
         """获取world,vehicle静态数据"""
        client1 = carla.Client("localhost",2100)
        
    