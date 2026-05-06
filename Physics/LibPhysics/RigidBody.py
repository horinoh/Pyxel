import math

from pyglm import glm

import LibPhysics.Collision

Gravity = glm.vec3(0.0, -9.8, 0.0) * 0.1

class RigidBody:
    Gravity = Gravity

    def __init__(self, shape, invMass):
        self.Shape = shape
        self.Position = glm.vec3(0.0)
        self.Rotation = glm.quat()
        self.Velocity_Linear = glm.vec3(0.0)
        self.Velocity_Angular = glm.vec3(0.0)
        self.Mass_Inverse = invMass
        self.InertiaTensor = shape.InertiaTensor
        self.InertiaTensor_Inverse = shape.InertiaTensor_Inverse
        self.Elasticity = 0.5
        self.Friction = 0.5
    def __del__(self):
        pass
    
    def GetCenterOfMass(self):
        return self.Shape.CenterOfMass
    def GetCenterOfMass_World(self):
        return self.Position + RigidBody.Rotate(self.Rotation, self.GetCenterOfMass())
    
    def Rotate(quat, rhs):
        return quat * rhs

    def ToLocal(self, rhs, center):
        return self.Rotate(rhs - center)
    def ToWorld(self, rhs, center):
        return self.Rotate(rhs) + center
    def ToLocalPos(self, rhs):
        return self.ToLocal(rhs, self.GetCenterOfMass_World())
    def ToWorldPos(self, rhs):
        return self.ToWorld(rhs, self.GetCenterOfMass_World())
    def ToLocalDir(self, rhs):
        return self.ToLocal(rhs, glm.vec3(0.0))
    def ToWorldDir(self, rhs):
        return self.ToWorld(rhs, glm.vec3(0.0))
    
    def ToWorld(self, rhs):
        m3 = glm.mat3(self.Rotation)
        return m3 * rhs * glm.transpose(m3)
    def GetInertiaTensor_World(self):
        return self.ToWorld(self.InertiaTensor)
    def GetInertiaTensor_Inverse_World(self):
        return self.ToWorld(self.InertiaTensor_Inverse)
    
    def ApplyGravity(self, deltaSec):
        if 0.0 != self.Mass_Inverse:
            self.Velocity_Linear += Gravity * deltaSec

    def ApplyImpulse_Linear(self, impulse):
        if 0.0 != self.Mass_Inverse:
            self.Velocity_Linear += impulse * self.Mass_Inverse
    def ApplyImpulse_Angular(self, impulse):
        if 0.0 != self.Mass_Inverse:
            self.Velocity_Angular += self.GetInertiaTensor_Inverse_World() * impulse
            
            # 角速度の限界値 (パフォーマンス的理由)
            maxAngVel = 30.0
            if glm.length2(self.Velocity_Angular) > maxAngVel * maxAngVel:
                self.Velocity_Angular = glm.normalize(self.Velocity_Angular) * maxAngVel

    def ApplyImpulse(self, impactPoint, impulse):
        if 0.0 != self.Mass_Inverse:
            self.ApplyImpulse_Linear(impulse)
            self.ApplyImpulse_Angular(glm.cross(impactPoint - self.GetCenterOfMass_World(), impulse))
    def ApplyImpulse(self, ct):
        ptA = ct.PointA_World
        ptB = ct.PointB_World

        totalInvMass = ct.RigidBodyA.Mass_Inverse + ct.RigidBodyB.Mass_Inverse
        
        radA = ptA - ct.RigidBodyA.GetCenterOfMass_World();
        radB = ptB - ct.RigidBodyB.GetCenterOfMass_World();

        invIA = ct.RigidBodyA.GetInertiaTensor_Inverse_World()
        invIB = ct.RigidBodyB.GetInertiaTensor_Inverse_World()

        velA = ct.RigidBodyA.Velocity_Linear + glm.cross(ct.RigidBodyA.Velocity_Angular, radA)
        velB = ct.RigidBodyB.Velocity_Linear + glm.cross(ct.RigidBodyB.Velocity_Angular, radB)
        velBA = velA - velB
        
        def apply(n, vel, coef):
            jA = glm.cross(glm.cross(radA, n) * invIA, radA)
            jB = glm.cross(glm.cross(radB, n) * invIB, radB)
            j = vel * coef / (totalInvMass + glm.dot(jA + jB, n))
            ct.RigidBodyA.ApplyImpulse(ptA, -j)
            ct.RigidBodyA.ApplyImpulse(ptB, j)

        n = ct.Normal_World
        velN = n * glm.dot(velBA, n)
        totalElas = 1.0 + ct.RigidBodyA.Elasticity + ct.RigidBodyB.Elasticity
        apply(n, velN, totalElas)

        velT = velBA - velN
        t = glm.normalize(velT)
        totalFric = ct.RigidBodyA.Friction + ct.RigidBodyB.Friction
        apply(t, velT, totalFric)

    def Update(self, deltaSec):
        self.Position += self.Velocity_Linear * deltaSec
        
        I_Inv = self.GetInertiaTensor_Inverse_World()
        I = self.GetInertiaTensor_World()
        angAcc = glm.cross(self.Velocity_Angular, self.Velocity_Angular * I) * I_Inv 
        self.Velocity_Angular += angAcc * deltaSec

        deltaVel = self.Velocity_Angular * deltaSec
        Len = glm.length2(deltaVel)
        if math.isclose(Len, 0.0):
            return
        Len = glm.sqrt(Len)
        deltaQuat = glm.angleAxis(Len, deltaVel / Len)

        self.Rotation = glm.normalize(deltaQuat * self.Rotation)

        centerOfMass = self.GetCenterOfMass_World()
        self.Position = centerOfMass + RigidBody.Rotate(deltaQuat, self.Position - centerOfMass)

        #print(f"pos={self.Position}")
        #print(f"lvel={self.Velocity_Linear}")
        #print(f"avel={self.Velocity_Angular}")
