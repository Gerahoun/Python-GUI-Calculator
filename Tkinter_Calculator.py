import tkinter as tk
import math, re, os, sys

expression = ""
result = "0"



SAFE_FUNCS = {
    'sin': lambda x: math.sin(math.radians(x)),
    'cos': lambda x: math.cos(math.radians(x)),
    'tan': lambda x: math.tan(math.radians(x)),
    'log': lambda x: math.log10(x),
    'sqrt': math.sqrt,
    'pi': math.pi,
    'e': math.e,
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def update_display():
    expr_label.config(text=expression)
    res_label.config(text=result)

def press(key):
    global expression, result
    if key == "CE":
        expression = ""
        result = "0"
    elif key == "C":
        expression = expression[:-1]
    elif key == "=":
        calc()
    elif key in ("+", "-", "×", "÷", "%", ".", "000"):
        if expression and expression[-1] in "+-×÷%":
            expression = expression[:-1] + key
        else:
            expression += key
    elif key in ("SIN", "COS", "TAN", "LOG"):
        expression += key.lower() + "("
    else:
        expression += key
    update_display()

def prepare(expr: str):
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expr)
    return expr

def calc():
    global expression, result
    try:
        expr = prepare(expression)
        val = eval(expr, {"__builtins__": None}, SAFE_FUNCS)
        if isinstance(val, float):
            val = round(val, 12)
            result = str(val).rstrip("0").rstrip(".")
        else:
            result = str(val)
    except Exception:
        result = "Error"
    update_display()

window = tk.Tk()
window.geometry("1400x600")
window.configure(bg="#B4B4B4")
window.title("Calculator")
window.iconbitmap(resource_path("Images/Tkinter_Calculator.ico"))


BTN_COLORS = {
    "numbers": {"bg": "#DDDDDD", "fg": "black"},
    "color_1": {"bg": "#AAAAAA", "fg": "black"},
    "color_2": {"bg": "#868686", "fg": "black"},
    "dark_Color_1": {"bg": "#272727", "fg": "white"},
    "dark_Color_2": {"bg": "#404040", "fg": "white"},
    "dark_Color_3": {"bg": "#303030", "fg": "white"},
    "special_Blue": {"bg": "#3A87CF", "fg": "white"},
    "special_Green": {"bg": "#3CAF3A", "fg": "white"},
    "special_Red": {"bg": "#CF3A3A", "fg": "white"},
    "special_Purple": {"bg": "#3A44CF", "fg": "white"},
    "special_Gray": {"bg": "#5C5C5C", "fg": "white"},
    "special_Orange": {"bg": "#CF733A", "fg": "white"},
}
RES_LABEL_COLORS = {
    "special_Blue": "#3A87CF",
    "special_Green": "#3CAF3A",
    "special_Red": "#CF3A3A",
    "special_Purple": "#3A44CF",
    "special_Gray": "#5C5C5C",
    "special_Orange": "#CF733A",
}

expr_label = tk.Label(window, text="0", anchor="e", bg="#AAAAAA", fg="#000000", font=("Digital Numbers", 14), justify="right")
expr_label.place(x=40, y=30, width=500, height=150)

res_label = tk.Label(window, text="0", anchor="se", bg="#AAAAAA", fg="#3A87CF", font=("Digital Numbers", 36, "bold"), justify="right")
res_label.place(x=40, y=170, width=500, height=400)

btn_groups = {
    "numbers": [], "color_1": [], "color_2": [],
    "special_Blue": [], "special_Green": [], "special_Red": [],
    "special_Purple": [], "special_Gray": [], "special_Orange": []
}

def make_btn(x, y, w, h, text="", style="numbers", image=None):
    colors = BTN_COLORS[style]
    btn = tk.Button(window, text=text, image=image, font=("Digital Numbers", 18),
                    command=lambda: press(text) if text else None,
                    bg=colors["bg"], fg=colors["fg"],
                    activebackground=colors["bg"], activeforeground=colors["fg"],
                    borderwidth=0)
    btn.place(x=x, y=y, width=w, height=h)
    btn_groups[style].append(btn)
    return btn

moon_icon = tk.PhotoImage(file=resource_path("Images/Moon.png"))
sun_icon = tk.PhotoImage(file=resource_path("Images/Sun.png"))
roller_icon = tk.PhotoImage(file=resource_path("Images/Roller.png"))

color_cycle = ["special_Blue", "special_Green", "special_Red", "special_Purple", "special_Gray", "special_Orange"]
current_color_index = 0

def Theme_mode():
    global current_color_index
    current_color_index = (current_color_index + 1) % len(color_cycle)
    new_color = color_cycle[current_color_index]
    for group, btn_list in btn_groups.items():
        if group.startswith("special"):
            for btn in btn_list:
                btn.config(bg=BTN_COLORS[new_color]["bg"], fg=BTN_COLORS[new_color]["fg"],
                           activebackground=BTN_COLORS[new_color]["bg"], activeforeground=BTN_COLORS[new_color]["fg"])
    res_label.config(fg=RES_LABEL_COLORS[new_color])

dark_mode_on = False

def Dark_mode():
    global dark_mode_on
    dark_mode_on = not dark_mode_on
    if dark_mode_on:
        dark_btn.config(image=sun_icon)
        window.configure(bg="#1E1E1E")
        expr_label.config(bg=BTN_COLORS["dark_Color_3"]["bg"], fg=BTN_COLORS["dark_Color_3"]["fg"])
        res_label.config(bg=BTN_COLORS["dark_Color_3"]["bg"], fg=RES_LABEL_COLORS[color_cycle[current_color_index]])
        for group, btn_list in btn_groups.items():
            for btn in btn_list:
                if group.startswith("special"):
                    btn.config(bg=BTN_COLORS[color_cycle[current_color_index]]["bg"], fg=BTN_COLORS[color_cycle[current_color_index]]["fg"],
                               activebackground=BTN_COLORS[color_cycle[current_color_index]]["bg"], activeforeground=BTN_COLORS[color_cycle[current_color_index]]["fg"])
                else:
                    if btn["text"] in ("CE", "Dark mode"):
                        btn.config(bg=BTN_COLORS["dark_Color_3"]["bg"], fg=BTN_COLORS["dark_Color_3"]["fg"])
                    elif btn["text"] in ("0", "000", "TAN", "LOG", "SIN", "COS"):
                        btn.config(bg=BTN_COLORS["dark_Color_2"]["bg"], fg=BTN_COLORS["dark_Color_2"]["fg"])
                    else:
                        btn.config(bg=BTN_COLORS["dark_Color_1"]["bg"], fg=BTN_COLORS["dark_Color_1"]["fg"])
    else:
        dark_btn.config(image=moon_icon)
        window.configure(bg="#B4B4B4")
        expr_label.config(bg="#AAAAAA", fg="#000000")
        res_label.config(bg="#AAAAAA", fg=RES_LABEL_COLORS[color_cycle[current_color_index]])
        for group, btn_list in btn_groups.items():
            for btn in btn_list:
                if group.startswith("special"):
                    btn.config(bg=BTN_COLORS[color_cycle[current_color_index]]["bg"], fg=BTN_COLORS[color_cycle[current_color_index]]["fg"],
                               activebackground=BTN_COLORS[color_cycle[current_color_index]]["bg"], activeforeground=BTN_COLORS[color_cycle[current_color_index]]["fg"])
                else:
                    colors = BTN_COLORS.get(group, BTN_COLORS["numbers"])
                    btn.config(bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"], activeforeground=colors["fg"])

make_btn(1152, 141, 218, 429, text="=", style="special_Blue")
make_btn(1035, 363, 101, 207, text="+", style="color_1")
make_btn(570, 30, 101, 96, text="CE", style="color_2")
make_btn(686, 30, 101, 96, text="LOG", style="color_1")
make_btn(802, 30, 101, 96, text="SIN", style="color_1")
make_btn(919, 30, 101, 96, text="COS", style="color_1")
make_btn(1035, 30, 101, 96, text="TAN", style="color_1")
make_btn(686, 141, 101, 96, text="8", style="numbers")
make_btn(802, 141, 101, 96, text="9", style="numbers")
make_btn(919, 141, 101, 96, text="÷", style="numbers")
make_btn(1035, 141, 101, 96, text="%", style="numbers")
make_btn(570, 141, 101, 96, text="7", style="numbers")
make_btn(919, 252, 101, 96, text="×", style="numbers")
make_btn(570, 252, 101, 96, text="4", style="numbers")
make_btn(685, 250, 103, 98, text="5", style="numbers")
make_btn(802, 252, 101, 96, text="6", style="numbers")
make_btn(1035, 252, 101, 96, text="-", style="numbers")
make_btn(570, 363, 101, 96, text="1", style="numbers")
make_btn(686, 363, 101, 96, text="2", style="numbers")
make_btn(802, 363, 101, 96, text="3", style="numbers")
make_btn(919, 363, 101, 96, text=".", style="numbers")
make_btn(570, 474, 101, 96, text="C", style="special_Blue")
make_btn(686, 474, 217, 96, text="0", style="color_1")
make_btn(919, 474, 101, 96, text="000", style="color_1")
Theme_btn = make_btn(1152, 30, 101, 96, style="special_Blue", image=roller_icon)
Theme_btn.config(command=Theme_mode)
dark_btn = make_btn(1268, 30, 101, 96, style="color_2", image=moon_icon)
dark_btn.config(command=Dark_mode)
update_display()
window.mainloop()