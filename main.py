import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

graphic = None
x1_input = None
x2_input = None
y1_input = None
y2_input = None
r_input = None
clicked = None
fig = None
canvas = None
root = None


def plot_point(x, y):
    graphic.scatter(x, y, c='black', marker='s')


def draw_step_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    plot_point(x, y)
    if dx > dy:
        step = dx
    else:
        step = dy
    dx = dx / step
    dy = dy / step
    for i in range(int(step)):
        x += dx
        y += dy
        plot_point(round(x), round(y))

def draw_cda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    plot_point(x, y)
    for i in range(int(steps)):
        x += x_inc
        y += y_inc
        plot_point(round(x), round(y))


def draw_brezenhem_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if x1 < x2:
        sx = 1
    else:
        sx = -1
    if y1 < y2:
        sy = 1
    else:
        sy = -1
    err = dx - dy
    x, y = x1, y1
    plot_point(x, y)
    while x != x2 or y != y2:
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        plot_point(x, y)


def draw_brezenhem_circle(x0, y0, r):
    x, y = 0, r
    delta = 1 - 2 * r
    while y >= 0:
        plot_point(x0 + x, y0 + y)
        plot_point(x0 + x, y0 - y)
        plot_point(x0 - x, y0 + y)
        plot_point(x0 - x, y0 - y)
        error = 2 * (delta + y) - 1
        if delta < 0 and error <= 0:
            x += 1
            delta += 2 * x + 1
            continue
        error = 2 * (delta - x) - 1
        if delta > 0 and error > 0:
            y -= 1
            delta += 1 - 2 * y
            continue
        x += 1
        delta += 2 * (x - y)
        y -= 1

def is_valid(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

def redraw():
    global graphic
    global x1_input
    global x2_input
    global y1_input
    global y2_input
    global r_input
    global clicked
    global fig
    global canvas
    global root
    drop_value = clicked.get()
    if drop_value != "Choose algorithm":
        fig.clear()
        graphic = fig.add_subplot(111)
        graphic.axis('equal')
    else:
        return
    x1, x2, y1, y2, r = 0,0,0,0,0
    if x1_input.get() == '' or y1_input.get() == '':
        x1 = 0
        y1 = 0
    else:
        x1 = int(x1_input.get()) 
        y1 = int(y1_input.get())
    if x2_input.get() == '' or y2_input.get() == '':
        x2 = 100
        y2 = 100
    else:
        x2 = int(x2_input.get())
        y2 = int(y2_input.get())
    
    if r_input.get() == '':
        r = 20
    else:
        r = int(r_input.get())
    
    if x1 == x2 and y1 == y2:
        return
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    if drop_value == "Step line rastorization":
        draw_step_line(x1, int(y1_input.get()), int(x2_input.get()), int(y2_input.get()))
    elif drop_value == "CDA line rastorization":
        draw_cda_line(int(x1_input.get()), int(y1_input.get()), int(x2_input.get()), int(y2_input.get()))
    elif drop_value == "Brezenhem line rastorization":
        draw_brezenhem_line(int(x1_input.get()), int(y1_input.get()), int(x2_input.get()), int(y2_input.get()))
    else:
        draw_brezenhem_circle(int(x1_input.get()), int(y1_input.get()), int(r_input.get()))

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=8)
    canvas.draw()



def main():
    global graphic
    global x1_input
    global x2_input
    global y1_input
    global y2_input
    global r_input
    global clicked
    global fig
    global canvas
    global root
    root = tk.Tk()
    root.title('Rasterization')
    for c in range(8): root.columnconfigure(index=c, weight=1)
    for r in range(3): root.rowconfigure(index=r, weight=1)
    fig = Figure(figsize=(5, 4), dpi=100)
    graphic = fig.add_subplot(111)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=8)

    canvas.draw()
    options = [
    "Step line rastorization",
    "CDA line rastorization",
    "Brezenhem line rastorization",
    "Brezenhem circle rastorization",
    ]
    clicked = tk.StringVar()

    clicked.set("Choose algorithm")
    
    drop = tk.OptionMenu( root , clicked , *options )
    drop.grid(row=0, column=0, rowspan=2)

    check = (root.register(is_valid), "%P")
    
    tk.Label(text='x1').grid(row=0, column=1)
    x1_input = tk.Entry(validate='all', validatecommand=check) 
    x1_input.grid(row=0, column=2)
    tk.Label(text='y1').grid(row=1, column=1)
    y1_input = tk.Entry(validate='all', validatecommand=check) 
    y1_input.grid(row=1, column=2)
    tk.Label(text='x2').grid(row=0, column=3)
    x2_input = tk.Entry(validate='all', validatecommand=check) 
    x2_input.grid(row=0, column=4)
    tk.Label(text='y2').grid(row=1, column=3)
    y2_input = tk.Entry(validate='all', validatecommand=check) 
    y2_input.grid(row=1, column=4)
    tk.Label(text='radius').grid(row=0, column=5, rowspan=2)
    r_input = tk.Entry(validate='all', validatecommand=check)
    r_input.grid(row=0, rowspan=2, column=6)

    draw = tk.Button(text='Draw', command=redraw)
    draw.grid(row=0, column=7, rowspan=2)

    root.mainloop()



if __name__ == "__main__":
    main()
