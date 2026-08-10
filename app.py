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
    def parse_angle(value):

    value = value.strip()

    # تبدیل اعداد فارسی
    persian = "۰۱۲۳۴۵۶۷۸۹"

    for i in range(10):
        value = value.replace(
            persian[i],
            str(i)
        )

    # تبدیل پی فارسی
    value = value.replace("π", "pi")

    # حذف فاصله‌ها
    value = value.replace(" ", "")

    # اگر فقط pi بود
    if value == "pi":
        return math.pi

    allowed = {
        "pi": math.pi
    }

    return eval(
        value,
        {"__builtins__": {}},
        allowed
    )
    def nice_trig_result(value):

    known = {
        0: "0",
        0.5: "1/2",
        -0.5: "-1/2",
        0.70710678118: "√2/2",
        -0.70710678118: "-√2/2",
        0.86602540378: "√3/2",
        -0.86602540378: "-√3/2",
        1: "1",
        -1: "-1"
    }


    for number, text in known.items():

        if abs(value - number) < 0.000001:
            return text


    return str(round(value, 10))

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


    if request.method == "POST":

        function = request.form["function"]

        angle_text = request.form["angle"]

        unit = request.form["unit"]


        try:

            angle = parse_angle(angle_text)


            if unit == "degree":
                angle = math.radians(angle)


            if function == "sin":

                answer = math.sin(angle)


            elif function == "cos":

                answer = math.cos(angle)


            elif function == "tan":

                answer = math.tan(angle)


            elif function == "cot":

                answer = 1 / math.tan(angle)



            result = f"{function}({angle_text}) = {nice_trig_result(answer)}"


        except:

            result = (
                "❌ ورودی زاویه معتبر نیست."
            )


    return render_template(
        "trigonometry.html",
        result=result
    )


# =========================
# اجرای برنامه
# =========================

if __name__ == "__main__":
    app.run()
