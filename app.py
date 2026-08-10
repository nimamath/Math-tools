from flask import Flask, render_template, request
import math

app = Flask(__name__)


def to_number(value):
    """
    تبدیل ورودی‌های مختلف به عدد.
    پشتیبانی از:
    12
    -12
    3.14
    -2.5
    ۳.۱۴
    -۲٫۵
    3,14
    """

    value = value.strip()

    # اعداد فارسی
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"

    # اعداد عربی
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"

    for i in range(10):
        value = value.replace(persian_digits[i], str(i))
        value = value.replace(arabic_digits[i], str(i))

    # علامت اعشار
    value = value.replace("٫", ".")
    value = value.replace(",", ".")

    # حذف فاصله‌های احتمالی
    value = value.replace(" ", "")

    return float(value)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quadratic", methods=["GET", "POST"])
def quadratic():

    result = None

    values = {
        "a": "",
        "b": "",
        "c": ""
    }

    if request.method == "POST":

        values["a"] = request.form.get("a", "")
        values["b"] = request.form.get("b", "")
        values["c"] = request.form.get("c", "")

        try:

            a = to_number(values["a"])
            b = to_number(values["b"])
            c = to_number(values["c"])

            # بررسی درجه دوم بودن
            if a == 0:

                result = (
                    '<span class="error">'
                    'ضریب a نمی‌تواند صفر باشد؛ '
                    'در این صورت معادله درجه دوم نیست.'
                    '</span>'
                )

            else:

                delta = b ** 2 - 4 * a * c

                # دو ریشه حقیقی
                if delta > 0:

                    sqrt_delta = math.sqrt(delta)

                    x1 = (-b + sqrt_delta) / (2 * a)
                    x2 = (-b - sqrt_delta) / (2 * a)

                    result = (
                        f"Δ = {delta}<br><br>"
                        f"دو ریشه حقیقی داریم:<br><br>"
                        f"x₁ = {x1}<br>"
                        f"x₂ = {x2}"
                    )

                # یک ریشه حقیقی
                elif delta == 0:

                    x = -b / (2 * a)

                    result = (
                        "Δ = 0<br><br>"
                        "یک ریشه حقیقی داریم:<br><br>"
                        f"x = {x}"
                    )

                # بدون ریشه حقیقی
                else:

                    result = (
                        f"Δ = {delta}<br><br>"
                        "این معادله ریشه حقیقی ندارد."
                    )

        except ValueError:

            result = (
                '<span class="error">'
                'لطفاً برای a، b و c عدد معتبر وارد کنید.'
                '<br><br>'
                'مثال: -2.5 یا 3.14 یا ۲٫۵'
                '</span>'
            )

    return render_template(
        "quadratic.html",
        result=result,
        values=values
    )


# =========================
# رسم نمودار
# =========================

@app.route("/graph", methods=["GET", "POST"])
def graph():

    graph_exists = False
    error = None

    if request.method == "POST":

        function = request.form.get("function", "").strip()

        try:

            x = np.linspace(-10, 10, 400)

            # توابع قابل استفاده
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

            # تبدیل ^ به **
            function = function.replace("^", "**")

            # پشتیبانی از sin(x)، cos(x) و ...
            y = eval(
                function,
                {"__builtins__": {}},
                allowed
            )

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

            error = "تابع واردشده قابل رسم نیست."


    return render_template(
        "graph.html",
        graph=graph_exists,
        error=error
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

        try:

            function = request.form["function"]
            angle = float(request.form["angle"])
            unit = request.form["unit"]

            # تبدیل درجه به رادیان
            if unit == "degree":
                radians = math.radians(angle)
            else:
                radians = angle

            # -----------------
            # sin
            # -----------------

            if function == "sin":

                value = math.sin(radians)

            # -----------------
            # cos
            # -----------------

            elif function == "cos":

                value = math.cos(radians)

            # -----------------
            # tan
            # -----------------

            elif function == "tan":

                if abs(math.cos(radians)) < 1e-12:

                    result = "تابع tan در این زاویه تعریف نشده."
                    value = None

                else:

                    value = math.tan(radians)

            # -----------------
            # cot
            # -----------------

            elif function == "cot":

                if abs(math.sin(radians)) < 1e-12:

                    result = "تابع cot در این زاویه تعریف نشده."
                    value = None

                else:

                    value = math.cos(radians) / math.sin(radians)

            else:

                result = "تابع انتخاب‌شده معتبر نیست."
                value = None


            if value is not None:

                result = f"{function}({angle}) = {value:.6f}"


        except ValueError:

            result = "لطفاً یک زاویه معتبر وارد کنید."

        except Exception:

            result = "خطایی در محاسبه رخ داد."


    return render_template(
        "trigonometry.html",
        result=result,
        function=function,
        angle=angle,
        unit=unit
    )


# =========================
# اجرای برنامه
# =========================

if __name__ == "__main__":
    app.run()
