import math
import random
import matplotlib.pyplot as plt
from matplotlib import animation, rc, gridspec

N = 20  # エージェントの個数
SIZE = 50  # 仮想空間のサイズ
SPEED = N/5
SEED = 65355
R = 9
TREATMENT_PERIOD = 40  # 感染してから治るまでの期間
MORTALITY_RATE = 0.05  # 死亡率
MORTALITY_PERIOD = 20  # 感染から死亡までの期間

class Agent2:

    def __init__(self, state):
        self.state = state
        self.term = 0
        self.mortality = random.random()

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

    def _calc_next(self, agents):
        if self.state == "S":
            self._state_S(agents)
        elif self.state == "I":
            self._state_I()
        elif self.state == "R":
            self._state_R()
        elif self.state == "D":
          pass
        else:
          print("ERROR")

    def _state_S(self, agents):
        sx = self.x
        sy = self.y
        for i in range(len(agents)):
            ax = agents[i].x
            ay = agents[i].y

            if agents[i].state == "I":
                if (sx-ax)*(sx-ax) + (sy-ay)*(sy-ay) < R:
                    self.state = "I"
                    break
        self._update()

    def _state_I(self):
        self.term += 1
        if self.term > TREATMENT_PERIOD:
            self.state = "R"
        if self.term > MORTALITY_PERIOD and self.mortality < MORTALITY_RATE:
            self.state = "D"
        self._update()

    def _state_R(self):
      self._update()



def calcn(agents):
    """次時刻の状態を計算"""
    # 状態Sのデータ
    xlistS, ylistS = [], []
    # 状態Iのデータ
    xlistI, ylistI = [], []
    # 状態Rのデータ
    xlistR, ylistR = [], []
    # 状態Dのデータ
    xlistD, ylistD = [], []

    for i in range(len(agents)):
        agents[i]._calc_next(agents)
        # a[i].putstate()
        # グラフデータに現在位置を追加
        if agents[i].state == "S":
            xlistS.append(agents[i].x)
            ylistS.append(agents[i].y)
        elif agents[i].state == "I":
            xlistI.append(agents[i].x)
            ylistI.append(agents[i].y)
        elif agents[i].state == "R":
            xlistR.append(agents[i].x)
            ylistR.append(agents[i].y)
        elif agents[i].state == "D":
            xlistD.append(agents[i].x)
            ylistD.append(agents[i].y)

    return xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD

def scatter_plot(image, n, xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD):
    """散布図描画用関数"""
    image += ax[n].plot(xlistS, ylistS, ".", markersize=9, label="Susceptible", color="b", alpha=0.9) #状態Sのプロット
    image += ax[n].plot(xlistI, ylistI, ".", markersize=10, label="Infected", color="r") #状態Iのプロット
    image += ax[n].plot(xlistR, ylistR, ".", markersize=9, label="Recovered", color="g", alpha=0.5) #状態Rのプロット
    image += ax[n].plot(xlistD, ylistD, ".", markersize=8, label="Dead", color="k") #状態Dのプロット
    return image


#描画するグラフの設定
fig = plt.figure(figsize=(4.7,5.4))
#何行何列　
gs = gridspec.GridSpec(6, 1, height_ratios=[1, 1, 1, 1, 1, 1])
ax = [plt.subplot(gs[0:5, 0]), plt.subplot(gs[5, 0])]

plt.close()
agents = [Agent2("S") for i in range(N)]

agents[0].state = "I"
agents[0].x = SIZE/2
agents[0].y = SIZE/2

#アニメーション用のグラフ保管場所
ims = []

legend_flag = True  # 凡例描画のフラグ

# グラフデータの初期化
T = []
# Statas数推移
statasS_sum_left= []
statasI_sum_left= []
statasR_sum_left= []
statasD_sum_left= []

OVER_CAPACITY = N/2

# エージェントシミュレーション
for t in range(100):
    T.append(t)
    xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD = calcn(agents)  # 次時刻の状態を計算
    im = []

    # 左側グラフ（対策なしの表示
    # subplot0：散布図
    im += scatter_plot(im, 0, xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD)

    # subplot2：推移図
    statasS_sum_left.append(len(xlistS))
    statasI_sum_left.append(len(xlistI))
    statasR_sum_left.append(len(xlistR))
    statasD_sum_left.append(len(xlistD))
    im += ax[1].stackplot(T, statasI_sum_left, statasR_sum_left, statasS_sum_left, statasD_sum_left, colors=["r","g", "b", "k"], alpha=0.7)

    #描画設定
    if legend_flag:  # 一回のみ凡例を描画
        ax[0].legend(bbox_to_anchor=(1.12, 1.03), loc='lower right', fontsize=9, ncol = 4)
        ax[0].set_xlim(0, SIZE)
        ax[0].set_ylim(0, SIZE)
        ax[0].tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False, length=0)
        ax[0].tick_params(length=0)
        ax[1].tick_params(labelbottom=True,labelleft=True,labelright=False,labeltop=False)
        ax[1].axhline(OVER_CAPACITY, ls = "--", color = "black")
        legend_flag = False

    ims.append(im)

ani = animation.ArtistAnimation(fig, ims, interval=70)
ani.save('agent_animation_2.gif', writer='imagemagick')
rc('animation', html='jshtml')
ani