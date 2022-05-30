import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from decimal import Decimal
from matplotlib.animation import FuncAnimation


FRAMES = 100
ITERATIONS = 10_000

M = 1.9 * (10 ** 30)
G = 6.67 * (10 ** (-11))

R_0_DEFAULT = 10 ** 12
V_0_DEFAULT = 4000
ALPHA_DEFAULT = np.pi / 2

prev_point1 = None


def r(theta):
    return L_m ** 2 / (G * M * (1 + e * np.cos(theta)))


def polar_to_cartesian(rho, theta):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def init_plot1():
    axes.set_aspect('equal', 'box')
    axes.set_title("Comet orbit around the Sun", size=16)
    axes.axis("off")
    axes.plot(x, y, c="#000000")
    axes.scatter(0, 0, 5, c="#ffff00", linewidths=1, edgecolors="#ffcc00")
    scalebar = AnchoredSizeBar(axes.transData,
                            r_0 // 10, f"{Decimal(r_0 // 10):.0E} m", "lower left", 
                            pad=0.1,
                            color="#000000",
                            frameon=False,
                            size_vertical=1,
                            fontproperties=fontprops)

    axes.add_artist(scalebar)
    axes.annotate("Sun", (0, 0), xytext=(-26, 0), textcoords="offset pixels", fontproperties=fontprops)


def animate_plot1(i):
    global prev_point1
    x_coord, y_coord = x[i * (ITERATIONS // FRAMES)], y[i * (ITERATIONS // FRAMES)]
    if prev_point1 is not None:
        prev_point1.remove()
    prev_point1 = axes.scatter(mirrored_axis - x_coord, y_coord, 10, c="#000000")
    return axes


def init_plot2():
    axes.set_title("Comet orbit around the Sun", size=16)
    axes.axis("off")
    axes.plot(x, y, c="#000000")
    axes.scatter(0, 0, 100, c="#ffff00", linewidths=1, edgecolors="#ffcc00")
    scalebar = AnchoredSizeBar(axes.transData,
                            r_0 // 100, f"{Decimal(r_0 // 100):.0E} m", "lower left", 
                            pad=0.1,
                            color="#000000",
                            frameon=False,
                            size_vertical=1,
                            fontproperties=fontprops)

    axes.add_artist(scalebar)
    axes.annotate("Sun", (0, 0), xytext=(-32, 0), textcoords="offset pixels", fontproperties=fontprops)
    axes.set_xlim([-r_0 // 10, r_0 // 10])


# Входные данные
print("""
Движение кометы в поле тяготения Солнца

После ввода входных данных программа сохранит в той же директории, откуда она была запущена, 2 файла с траекторией кометы и 1 файл с симуляцией её движения.
Входные данные:""")
while True:
    r_0 = input("Введите расстояние от кометы до Солнца (в м) или \"def\" для значения по умолчанию (1e12): ")
    if r_0 == "def":
        r_0 = R_0_DEFAULT
        break
    try:
        if "inf" in r_0:
            raise ValueError
        r_0 = float(r_0)
        break
    except Exception:
        print("Некорректные данные")
        

while True:
    v_0 = input("Введите начальную скорость комета (в м/с) или \"def\" для значения по умолчанию (2000): ")
    if v_0 == "def":
        v_0 = V_0_DEFAULT
        break
    try:
        if "inf" in v_0:
            raise ValueError
        v_0 = float(v_0)
        break
    except Exception:
        print("Некорректные данные")

while True:
    alpha = input("Введите угол между этими векторами (в градусах) или \"def\" для значения по умолчанию (90): ")
    if alpha == "def":
        alpha = ALPHA_DEFAULT
        break
    try:
        if "inf" in alpha:
            raise ValueError
        alpha = float(alpha) / 180 * np.pi
        break
    except Exception:
        print("Некорректные данные")

print("Обработка данных...")
try:
    L_m = r_0 * v_0 * np.sin(alpha)
    e = np.sqrt(1 + (v_0 ** 2 - 2 * G * M / r_0) * L_m ** 2 / (G ** 2 * M ** 2))

    theta = np.linspace(0, 2 * np.pi, ITERATIONS)
    rho = r(theta)
    x, y = polar_to_cartesian(rho, theta)
    mirrored_axis = min(x) + max(x)

    fontprops = fm.FontProperties(size=12)

    # plot 1
    fig, axes = plt.subplots()
    init_plot1()
    animation = FuncAnimation(fig, animate_plot1, frames=FRAMES, interval=50)
    animation.save("plot1.gif", writer="ffmpeg", dpi=120)
    prev_point1.remove()
    fig.savefig("plot1.png")

    # plot 2
    fig, axes = plt.subplots()
    init_plot2()
    fig.savefig("plot2.png")
except Exception as ex:
    print("Произошла ошибка:", ex)
    print("Попробуйте запустить программу с другими входными данными.")
    exit(0)
else:
    print("Данные успешно обработаны. Результаты находятся в текущей директории.")
