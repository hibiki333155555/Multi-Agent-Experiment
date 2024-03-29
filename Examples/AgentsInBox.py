import math
import random
import matplotlib.pyplot as plt
from matplotlib import animation, rc

N = 2  # エージェントの個数
SIZE = 50  # 仮想空間のサイズ
SPEED = N/5
SEED = 65355

class Agent:

    def __init__(self):
        self.x = random.randint(1,SIZE)  # x座標の初期値
        self.y = random.randint(1,SIZE)  # y座標の初期値
        radian = math.radians(random.randint(1,360))
        self.x_v = math.cos(radian)*SPEED  # x方向の速さ
        self.y_v = math.sin(radian)*SPEED  # y方向の速さ


    def _update(self):
        """
        エージェントのxy座標を更新する
        """
        if self.x + self.x_v < 0 or SIZE < self.x + self.x_v:
            self.x_v *= -1
        if self.y + self.y_v < 0 or SIZE < self.y + self.y_v:
            self.y_v *= -1
        self.x = self.x + self.x_v
        self.y = self.y + self.y_v


random.seed(SEED) # 乱数の初期化
agents = [Agent() for i in range(30)]

fig, ax = plt.subplots()
ax.set_xlim(0, SIZE)
ax.set_ylim(0, SIZE)
ax.set_aspect("equal", adjustable="box")
plt.close()

ims = []

for t in range(200):
    im = []
    xlist = []
    ylist = []
    for i in range(len(agents)):
        agents[i]._update()
        xlist.append(agents[i].x)
        ylist.append(agents[i].y)

    im = ax.plot(xlist, ylist, 'o', c='b')
    ims.append(im)



ani = animation.ArtistAnimation(fig, ims, interval=30)

ani.save('agent_animation.gif', writer='imagemagick')
rc('animation', html='jshtml')
ani