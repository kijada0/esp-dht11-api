import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.axes as ax
import math
import datetime

label = [["c [%]", "n"], ["T [\u00B0C]", "n"]]
color_tab = ["tab:blue", "tab:green", "tab:red", "tab:orange", "tab:purple", "tab:cyan", "tab:olive", "tab:pink"]
a_tab = ""

q = int(1)

def main():
    global label
    global error

    raw_data = read_data("data.csv")
    data, label = data_processing(raw_data)

    multi_plot(data, label, True, True)

def read_data(dir):
    f = open(dir, "r")
    raw = f.readlines()
    f.close()

    data = []

    line = raw[0][:len(raw[0]) - 1].split(";")
    for i in range(len(line)): data.append([])

    for i in range(len(raw)):
        line = raw[i][:len(raw[i]) - 1].split(";")
        for j in range(len(line)):
            data[j].append(line[j])

    return data


def reglin(x0, y0):
    x = np.array(x0, dtype="float")
    y = np.array(y0)

    # print([sum(x), sum(y), sum(x**2), sum(y**2), sum(x*y)])
    # print((len(x)*sum(x*y) - sum(x)*sum(y)), (len(x)*sum(x**2) - sum(x)**2))

    a = (len(x) * sum(x * y) - sum(x) * sum(y)) / (len(x) * sum(x ** 2) - sum(x) ** 2)
    b = (sum(y) - a * sum(x)) / len(x)

    s = math.sqrt((sum(y ** 2) - a * sum(x * y) - b * sum(y)) / (len(x) - 2))
    da = math.sqrt(s ** 2 * (len(x)) / (len(x) * sum(x ** 2) - sum(x) ** 2))
    db = math.sqrt(s ** 2 * (sum(x ** 2)) / (len(x) * sum(x ** 2) - sum(x) ** 2))

    R = (len(x) * sum(x * y) - sum(x) * sum(y)) / (
        math.sqrt((len(x) * sum(x ** 2) - sum(x) ** 2) * (len(y) * sum(y ** 2) - sum(y) ** 2)))

    # print(a, b, "\n", s, da, db, "\n", R)
    return ([a, b, da, db, R])

def save_results(x, y, n):
    x = np.array(x)
    y = np.array(y)

    plt.savefig("plot_" + str(n) + ".png", format="jpg", dpi=500, bbox_inches="tight")


def multi_plot(data, labels, save_fig, reg):
    global color_tab
    global q

    x = np.array(data[0])
    y = np.array(data[2])

    x_lim = [x.min(), x.max()]
    y_lim = [y.min()-(y.min()*0.2), y.max()+(y.min()*0.2)]

    plt.close()

    plt.figure(figsize=(18, 6))
    fig = plt.subplot()

    #fig.plot(rx, ry, linestyle="--", alpha=0.5, linewidth=1, color=color_tab[q])
    if reg:
        r = reglin(x, y) # out: [a, b, da, db, R]
        rx = np.linspace(x_lim[0], x_lim[1], len(x))
        ry = r[0] * rx + r[1]
        fig.plot(rx, ry, markersize=1, linestyle="--", alpha=0.3, color="red")
        fig.plot(x, y, marker="o", markersize=2, linestyle="", color="cornflowerblue")
        fig.plot(x, y, marker=" ", linestyle="-", alpha=0.5, color="cornflowerblue")

        print("Reglin:\ta = ", round(r[0], 10), "\tda = ", round(r[2], 10), "\tb = ", round(r[1], 10), "\tdb = ", round(r[3], 10))

        rate_h = r[0]*(60*60)
        rate_d = r[0]*(60*60*24)
        text = "\nRate of change: {} [m%RH/second] \t {} [%RH/hour] \t {} [%RH/day] \n".format(round(r[0]*1000, 6), round(rate_h, 3), round(rate_d, 3))
        print(text)


    else:
        fig.plot(x, y, markersize=1, linestyle="--", alpha=0.3, color="black")
        fig.plot(x, y, marker="o", markersize=4, linestyle=" ", color="black")


    plt.xlabel(labels[0])
    plt.ylabel(labels[1])

    plt.xlim(x_lim)
    plt.ylim(y_lim)

    #plt.legend()

    fig.grid(which="major", alpha=0.6)
    fig.grid(which="minor", alpha=0.3)


    if save_fig:
        name = "plot_" + str(q) + ".png"
        print("Saving: ", name)
        plt.savefig(name, format="jpg", dpi=500, bbox_inches="tight")

    q = q+1

def data_processing(input_data):
    output_data = [[], [], []]
    output_label = []


    output_label = ["timestamp", input_data[2][0], input_data[3][0]]

    for raw_date, raw_time, series1, series2 in zip(input_data[0], input_data[1], input_data[2], input_data[3]):
        if "-" in raw_date:
            output_data[0].append(get_timestamp(raw_date, raw_time))
            output_data[1].append(float(series1))
            output_data[2].append(float(series2))


    return output_data, output_label


def get_timestamp(raw_date, raw_time):
    (y_dt, m_dt, d_dt) = raw_date.split("-")
    (h_td, m_td, s_td) = raw_time.split(":")

    dt = datetime.date(int(y_dt), int(m_dt), int(d_dt))
    tm = datetime.time(int(h_td), int(m_td), int(s_td))

    return datetime.datetime.timestamp(datetime.datetime.combine(dt, tm))


main()