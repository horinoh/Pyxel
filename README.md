# Pyxel

## 実行

- VSCode で Main.py を開き、右上の▶で実行


## glm, numpy

|glm|numpy(np)|
|-|-|
|glm.angleAxis(glm.radians(45.0), glm.vec3(0.0, 1.0, 0.0))|quaternion.from_rotation_vector(np.array([0, 1, 0]) * np.radians(45))|
|q * glm.vec3(1,0,0)|quaternion.rotate_vectors(q, np.array([1, 0, 0])|
|glm.mat3(q)|quaternion.as_rotation_matrix(q)|