from pyglm import glm

import LibPhysics.RigidBody

class ContactBase:
    def __init__(self):
        self.TimeOfImpact = 0.0
        self.RigidBodyA = None
        self.RigidBodyB = None
        self.PointA_World = glm.vec3(0.0)
        self.PointB_World = glm.vec3(0.0)
        self.Normal_World = glm.vec3(0.0)
    def __del__(self):
        None

    def Swap(self):
        self.RigidBodyA, self.RigidBodyB = self.RigidBodyB, self.RigidBodyA
        self.PointA_World, self.PointB_World = self.PointB_World, self.PointA_World
        self.Normal_World = -self.Normal_World

class Contact(ContactBase):
    def __init__(self):
        super().__init__()
        self.PointA = glm.vec3(0.0)
        self.PointB = glm.vec3(0.0)
    def __del__(self):
        super().__del__()

    def Swap(self):
        super().Swap()
        self.PointA, self.PointB = self.PointB, self.PointA
        
    def CalcLocal(self):
        self.PointA = self.RigidBodyA.ToLocalPos(self.PointA_World)
        self.PointB = self.RigidBodyB.ToLocalPos(self.PointB_World)