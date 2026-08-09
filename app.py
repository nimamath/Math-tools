from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# معادله درجه دوم
# =========================

@app.route("/quadratic", methods=["GET", "POST"])
def quadratic():
    result = None
    delta = None
    x1 = None
    x2 = None
    equation = None

    if request.method == "POST":

        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])

        equation = f"{a}x² + {b}x + {c} = 0"

        if a == 0:
            result = "ضریب a نمی‌تواند صفر باشد."

        else:
            delta = b**2 - 4 * a * c

            if delta > 0:

                x1 = (-b + math.sqrt(delta)) / (2 * a)
                x2 = (-b - math.sqrt(delta)) / (2 * a)

                result = "معادله دو ریشهٔ حقیقی دارد."

            elif delta == 0:

                x1 = -b / (2 * a)

                result = "معادله یک ریشهٔ حقیقی مضاعف دارد."

            else:

                result = "معادله ریشهٔ حقیقی ندارد."

    return render_template(
        "quadratic.html",
        result=result,
        delta=delta,
        x1=x1,
        x2=x2,
        equation=equation
    )


# =========================
# رسم نمودار
# =========================

@app.route("/graph", methods=["GET", "POST"])
def graph():

    graph_exists = False

    if request.method == "POST":

        function = request.form["function"]

        try:

            x = np.linspace(-10, 10, 400)

            # توابع مجاز
            allowed = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "sqrt": np.sqrt,
                "exp": np.exp,
                "log": np.log,
                "pi": np.pi
            }

            y = eval(function, {"__builtins__": {}}, allowed)

            plt.figure(figsize=(8, 5))

            plt.plot(x, y)

            plt.axhline(0)
            plt.axvline(0)

            plt.grid(True)

            plt.xlabel("x")
            plt.ylabel("y")

            plt.title(f"y = {function}")

            plt.tight_layout()

            graph_path = os.path.join(
                "static",
                "graph.png"
            )

            plt.savefig(graph_path)
            plt.close()

            graph_exists = True

        except Exception:

            graph_exists = False

    return render_template(
        "graph.html",
        graph=graph_exists
    )


# =========================
# توابع مثلثاتی
# =========================

@app.route("/trigonometry", methods=["GET", "POST"])
def trigonometry():

    result = None
    function = None
    angle = None
    unit = None

    if request.method == "POST":

        function = request.form["function"]
        angle = float(request.form["angle"])
        unit = request.form["unit"]

        # تبدیل درجه به رادیان
        if unit == "degree":
            radians = math.radians(angle)
        else:
            radians = angle

        try:

            if function == "sin":
                value = math.sin(radians)

            elif function == "cos":
                value = math.cos(radians)

            elif function == "tan":

                # بررسی نقاط تعریف‌نشده
                if abs(math.cos(radians)) < 1e-12:
                    result = "تابع tan در این زاویه تعریف نشده."
                    value = None
                else:
                    value = math.tan(radians)

            elif function == "cot":

                # cot(x) = cos(x) / sin(x)
                if abs(math.sin(radians)) < 1e-12:
                    result = "تابع cot در این زاویه تعریف نشده."
                    value = None
                else:
                    value = math.cos(radians) / math.sin(radians)

            else:
                result = "تابع واردشده معتبر نیست."
                value = None

            if value is not None:
                result = f"{function}({angle}) = {value:.6f}"

        except Exception:

            result = "خطایی در محاسبه رخ داد."

    return render_template(
        "trigonometry.html",
        result=result,
        function=function,
        angle=angle,
        unit=unit
    )


if __name__ == "__main__":
    app.run()
