import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import math

points = [(0, 0), (0, 0), (0, 0), (0, 0)]

# Default points (x, y)
root = tk.Tk()
root.geometry("300x100")
root.title("Curve SetUp")

def run():
    global points
    global Editbox1
    try:
        input_points = Editbox1.get().split(';')
        points = [tuple(map(float, point.strip('()').split(','))) for point in input_points]
        Graphing1()
    except Exception as e:
        print(f"Error parsing input: {e}")

def Graphing1():
    global points
    (x1, y1) = points[0]  # start point
    (x4, y4) = points[3]  # end point
    (x2, y2) = points[1]
    (x3, y3) = points[2]

    t = np.linspace(0, 1, 100)
    def f(t):
        return x1*(1-t)**3 + 3*x2*t*(1-t)**2 + 3*x3*t**2*(1-t) + x4*t**3
    def g(t):
        return y1*(1-t)**3 + 3*y2*t*(1-t)**2 + 3*y3*t**2*(1-t) + y4*t**3

    plt.plot(f(t), g(t))
    plt.scatter(x=x1, y=y1)
    plt.scatter(x=x2, y=y2)
    plt.scatter(x=x3, y=y3)
    plt.scatter(x=x4, y=y4)
    plt.title("Bézier Curve")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(False)
    plt.show()

def Kappa():
    global points
    global Editbox1
    try:
        input_points = Editbox1.get().split(';')
        points = [tuple(map(float, point.strip('()').split(','))) for point in input_points]
        Graphing2()
        Graphing3()
    except Exception as e:
        print(f"Error parsing input: {e}")

def Graphing2():
    global points
    (x1, y1) = points[0]  # start point
    (x4, y4) = points[3]  # end point
    (x2, y2) = points[1]
    (x3, y3) = points[2]
    t = np.linspace(0, 1, 100)

    def Bx_Prime(t):
        return 3*(x2-x1)*(1-t)**2 + 6*(x3-x2)*(1-t)*t + 3*(x4-x3)*t**2
    def By_Prime(t):
        return 3*(y2-y1)*(1-t)**2 + 6*(y3 - y2)*(1-t)*t + 3*(y4-y3)*t**2

    def Bx_primeprime(t):
        return 6*(x3-2*x2+x1)*(1-t) + (x4-2*x3+x2)*t
    def By_primeprime(t):
        return 6*(y3-2*y2+y1)*(1-t) + (y4-2*y3+y2)*t

    def KappaResult(t):
        return abs(Bx_Prime(t)*By_primeprime(t) - By_Prime(t)*Bx_primeprime(t)) / math.sqrt(Bx_Prime(t)**2 + By_Prime(t)**2)**3

    KappaValues = np.array([KappaResult(t) for t in t])

    plt.plot(KappaValues)
    plt.title("Curvature of Bézier (Kappa rad/m)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(False)
    plt.show()

def Graphing3():
    global points
    (x1, y1) = points[0]  # start point
    (x4, y4) = points[3]  # end point
    (x2, y2) = points[1]
    (x3, y3) = points[2]
    t = np.linspace(0, 1, 100)
    def f(t):
        return x1*(1-t)**3 + 3*x2*t*(1-t)**2 + 3*x3*t**2*(1-t) + x4*t**3
    def g(t):
        return y1*(1-t)**3 + 3*y2*t*(1-t)**2 + 3*y3*t**2*(1-t) + y4*t**3
    def Bx_Prime(t):
        return 3 * (x2 - x1) * (1 - t) ** 2 + 6 * (x3 - x2) * (1 - t) * t + 3 * (x4 - x3) * t ** 2
    def By_Prime(t):
        return 3 * (y2 - y1) * (1 - t) ** 2 + 6 * (y3 - y2) * (1 - t) * t + 3 * (y4 - y3) * t ** 2
    def Bx_primeprime(t):
        return 6 * (x3 - 2 * x2 + x1) * (1 - t) + (x4 - 2 * x3 + x2) * t + 1e-9
    def By_primeprime(t):
        return 6 * (y3 - 2 * y2 + y1) * (1 - t) + (y4 - 2 * y3 + y2) * t + 1e-9
    def KappaResult(t):
        return abs(Bx_Prime(t) * By_primeprime(t) - By_Prime(t) * Bx_primeprime(t)) / math.sqrt(
            Bx_Prime(t) ** 2 + By_Prime(t) ** 2) ** 3
    KappaValues = np.array([KappaResult(t) for t in t])
    RadiusValues = np.array([1 / k if k != 0 else 1e9 for k in KappaValues])  # Handle zero curvature
    def Tx(t):
        return Bx_Prime(t) / math.sqrt(Bx_Prime(t)**2 + By_Prime(t)**2)
    def Ty(t):
        return By_Prime(t) / math.sqrt(Bx_Prime(t)**2 + By_Prime(t)**2)
    # (Normal Unit)Vector = [-1*float(Ty(t)), Tx(t)]
    def Cx(ti, radius, tx, ty):
        return f(ti) - radius * ty

    def Cy(ti, radius, tx, ty):
        return g(ti) + radius * tx

    theta = np.linspace(0, 2 * math.pi, 100)
    x_theta_all = []
    y_theta_all = []

    for i, ti in enumerate(t):
        tx = Tx(ti)
        ty = Ty(ti)
        cx = Cx(ti, RadiusValues[i], tx, ty)
        cy = Cy(ti, RadiusValues[i], tx, ty)
        r = RadiusValues[i]

        x_circle = cx + r * np.cos(theta)
        y_circle = cy + r * np.sin(theta)

        x_theta_all.append(x_circle)
        y_theta_all.append(y_circle)
    # Plot Bézier curve
    plt.plot(f(t), g(t), label="Bézier Curve")

    # Plot osculating circles
    for x_c, y_c in zip(x_theta_all, y_theta_all):
        plt.plot(x_c, y_c, color="green", alpha=0.3)

    plt.title("Bézier Curve")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(False)
    plt.show()

RunButton = tk.Button(root, text="Run", font=("Courier", 10), command=run)
RunButton.place(x=225, y=60)
GetCalculus = tk.Button(root, text="𝝹", font=("Courier", 10), command=Kappa)
GetCalculus.place(x=225, y=40)
Editbox1 = tk.Entry(root, width=40, font=("Courier", 10))
Editbox1.place(x=15, y=15)
Editbox1.insert(0, "(0,-3);(2,5);(6,-7);(3,4)")
frame1 = tk.Frame()
label1 = tk.Label(root, font=("Courier", 10), text="(0,0)-start point at first \nmodifier points in the middle 2,\n(0,0)-end point at the last plae")
label1.place(x=15, y=55)

root.mainloop()
