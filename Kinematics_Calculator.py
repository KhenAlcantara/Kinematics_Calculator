# Kinematics Calculator
# Created by: Khen Jomarie L. Alcantara
# Degree: BS Electronics And Communication Engineering
# Level: 1st Year
# This program used sympy library for integration and differentiation of equation
# NOTE: To run this program you need to install sympy library first
# For installation run this command: pip install sympy
# Or manually install it in pycharm packages

# Import library
import os
import ctypes
from ctypes import wintypes
import sys
import sympy
import fractions

# Initialize variable
columns = 0
topics = {
    1: "Displacement, Time Interval, and Average Velocity",
    2: "Instantaneous Velocity",
    3: "Average and Instantaneous Acceleration",
    4: "Constant Acceleration",
    5: "Free Fall",
    6: "Finding Velocity and Displacement from Acceleration"
}
p_i, p_f, v_i, v_f, a, t = sympy.symbols('p_i p_f v_i v_f a t')
in_solving = False
_topic = False
selected = None
ai_a_select = None
fvda_select = None


# Class Kinematic use for calculating constant acceleration and free fall
class Kinematic:

    Given = {}

    Not_Given = []

    Unknown = []

    Equation = {
        1: sympy.Eq(v_f, v_i + a * t),
        2: sympy.Eq(p_f - p_i, v_i * t + 0.5 * a * t**2),
        3: sympy.Eq(v_f**2, v_i**2 + 2 * a * (p_f - p_i)),
        4: sympy.Eq(p_f - p_i, 0.5 * (v_i + v_f) * t)
    }

    Answer = {}


# Function for requesting administration
def run_as_administrator():
    # Checking current console if not running as administrator
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.basename(__file__), None, 1)
        sys.exit()


# Function for single instance console application
def is_single_instance(_title):
    # Define necessary Windows types
    lpctstr = ctypes.c_wchar_p

    # Create a mutex
    mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, True, lpctstr(_title))

    # Check if the mutex already exists
    if ctypes.windll.kernel32.GetLastError() == 183 or mutex_handle is None:  # ERROR_ALREADY_EXISTS = 183

        # Find the window by title
        hwnd = ctypes.windll.user32.FindWindowW(None, lpctstr(_title))

        # Bring the window to the foreground
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # If console is in minimize it will show
            ctypes.windll.user32.SetForegroundWindow(hwnd)

        return False

    return True


# Function for assigning console title
def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


# Function for resizing console
def set_console_size(width: int, height: int):
    os.system(f"mode con cols={width} lines={height}")


# Function for aligning console to center windows
def center_console_window():
    # Define necessary constants
    gwl_style = -16
    ws_size_box = 0x00040000
    ws_maximize_box = 0x00010000

    # Get handle to the console window
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Get current style
    style = ctypes.windll.user32.GetWindowLongW(hwnd, gwl_style)

    # Restore console style
    original_style = style | ws_size_box | ws_maximize_box
    ctypes.windll.user32.SetWindowLongW(hwnd, gwl_style, original_style)

    # Get screen dimensions
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # Get dimensions of the console window
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    console_width = rect.right - rect.left
    console_height = rect.bottom - rect.top

    # Calculate new position
    x = (screen_width - console_width) // 2
    y = (screen_height - console_height) // 2

    # Set console window position
    ctypes.windll.user32.MoveWindow(hwnd, x, y, console_width, console_height, True)

    # Update console style to disable resizing of console
    new_style = style & ~ws_size_box & ~ws_maximize_box
    ctypes.windll.user32.SetWindowLongW(hwnd, gwl_style, new_style)


# Function for clearing/deleting a line
def clear(line):
    for _ in range(line):
        print("\x1b[1A\x1b[2K", end="\r")


# Function for only int input
def int_input(_prompt: str):
    while True:
        try:
            input_int = int(input(_prompt))
            return input_int
        except ValueError:
            clear(1)
            continue


# Function for only float input
def float_input(_prompt: str):
    while True:
        try:
            input_int = float(input(_prompt))
            return input_int
        except ValueError:
            clear(1)
            continue


# Function for converting decimal to fraction
def convert_to_fraction(expression):
    expression = sympy.sympify(expression)
    coefficients = expression.as_coefficients_dict()
    fraction_coefficients = {var: fractions.Fraction(str(coe)).limit_denominator() for var, coe in
                             coefficients.items()}
    return sum(frac * var for var, frac in fraction_coefficients.items())


# Function for getting displacement
def displacement(x1, x2):
    return x2 - x1


# Function for getting time_interval
def time_interval(t1, t2):
    return t2 - t1


# Function for getting average velocity
def ave_velocity(_displacement, _time_interval):
    try:
        average_velocity = _displacement / _time_interval
        return average_velocity
    except ZeroDivisionError:
        return 0


# Function for getting instantaneous velocity
def instantaneous_velocity(_equation, _time):
    derivative = sympy.diff(_equation, t)
    return round(float(derivative.subs(t, _time)), 2)


# Main Function
def main():
    global in_solving
    global _topic
    global selected

    if not in_solving:  # Check if the program is not in solving
        # Title
        print("╔" + "═" * 78 + "╗")
        print(f"║{"KINEMATICS CALCULATOR":^78}║")
        print("╚" + "═" * 78 + "╝")

        # Option
        print("      OPTIONS:")
        for key, topic in topics.items():
            print(f"         [{key}] {topic}")

        print("         [0] Exit\n")

        selection = None
        while not selection:
            selected = int_input("      Select an option: ")
            if selected in range(1, 7):   # Checking for selected option
                clear(13)
                for key, topic in topics.items():
                    if key == selected:
                        # Display the selected topic
                        print("╔" + "═" * 78 + "╗")
                        print(f"║{topic.upper():^78}║")
                        print("╚" + "═" * 78 + "╝")

                        # Formating the selected topic for later use in calling function
                        _topic = (topic.replace(" from ", "_from_").replace(", and ", "_").replace(", ", "_")
                                  .replace(" ", "").replace("and", "_"))

                        # Checking if selected option is constant acceleration or free fall
                        if _topic == "ConstantAcceleration" or _topic == "FreeFall":
                            ConstantAcceleration_FreeFall_Calculation(_topic)
                        else:
                            globals()[_topic]()
                        selection = True
                        break
                else:
                    clear(1)
            elif selected == 0:
                exit()
            else:
                clear(1)
    else:
        for key, topic in topics.items():
            if key == selected:
                # Display the selected topic
                print("╔" + "═" * 78 + "╗")
                print(f"║{topic.upper():^78}║")
                print("╚" + "═" * 78 + "╝")

                # Checking if selected option is constant acceleration or free fall
                if _topic == "ConstantAcceleration" or _topic == "FreeFall":
                    ConstantAcceleration_FreeFall_Calculation(_topic)
                else:
                    globals()[_topic]()

    # Allow user to choose whether to exit or not after the program successfully executed
    print("\n\n", end="")
    print(("-" * 74).center(columns))
    print("[Y] Exit        [N] Solve Again        [H] Home".center(columns))
    while True:
        choice = input("      Select: ").upper()

        # Checking for user choice
        if choice == "y".upper():
            exit()
        elif choice == "n".upper():
            clear(100)
            in_solving = True
            return main()
        elif choice == "h".upper():
            clear(100)
            in_solving = False
            return main()
        else:
            clear(1)
            continue


# Function for displacement, time interval and average velocity
def Displacement_TimeInterval_AverageVelocity():
    # Request the user to input the given
    print("      Displacement:")
    x1 = float_input("         Initial position(m): ")
    x2 = float_input("         Final position(m)  : ")
    print("")
    print("      Time Interval:")
    t1 = float_input("         Initial time(s)    : ")
    t2 = float_input("         Final time(s)      : ")

    # Display the result
    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    print(f"         Displacement     : {displacement(x1, x2)}m")
    print(f"         Time Interval    : {time_interval(t1, t2)}s")
    print(f"         Average Velocity : {ave_velocity(displacement(x1, x2), time_interval(t1, t2))}m/s")


# Function for instantaneous velocity
def InstantaneousVelocity():
    # Request the user to input the equation
    print("         Sample equation: (20 + 5*t^2)")
    while True:  # Checking if equation is valid
        try:
            equation = input("         Enter the equation : ")
            equation = equation.replace("^", "**")
            equation = sympy.sympify(equation)
            if equation.free_symbols == {t}:
                break
            else:
                clear(1)
        except TypeError:
            clear(1)
        except sympy.SympifyError:
            clear(1)

    # Input the given time
    time = float_input("         At what time(s)?   : ")

    # Display the result
    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    print(f"         Instantaneous Velocity: {instantaneous_velocity(equation, time)}m/s")


# Function for average instantaneous acceleration
def Average_InstantaneousAcceleration():
    global ai_a_select

    # Option for average acceleration and instantaneous acceleration
    if not in_solving:
        print("      Select an option you want to solve:")
        print("         [1] Average Acceleration")
        print("         [2] Instantaneous Acceleration")
        print("")

    while True:
        if not in_solving:
            ai_a_select = input("      Select: ")
            clear(5)

        # Checking for the selected option
        if ai_a_select == "1":
            print("Solve for Average Acceleration".center(columns))
            print("")

            # Request the user to input the given
            initial_velocity = float_input("         Initial velocity(m) : ")
            final_velocity = float_input("         Final velocity(m)   : ")
            initial_time = float_input("         Initial time(s)     : ")
            final_time = float_input("         Final time(s)       : ")

            # Process for getting the average velocity
            _displacement = final_velocity - initial_velocity
            _time = final_time - initial_time
            average_velocity = ave_velocity(_displacement, _time)

            # Display the result
            print("")
            print(("-" * 68).center(columns))
            print("ANSWER\n".center(columns))
            print(f"         Average Acceleration: {average_velocity}m/s")
            break
        elif ai_a_select == "2":
            print("Solve for Instantaneous Acceleration".center(columns))
            print("")

            # Request the user to input the equation
            while True:  # Checking if equation is valid
                try:
                    print("         Sample equation: (3 * t^2 + 2 * t)")
                    equation = input("         Enter the acceleration equation: ")
                    equation = equation.replace("^", "**")
                    equation = sympy.sympify(equation)

                    if equation.free_symbols == {t}:
                        break
                    else:
                        clear(2)
                except TypeError:
                    clear(2)
                except sympy.SympifyError:
                    clear(2)

            # Input the given time
            _time = float_input("         At what time(s)?               : ")

            # Process for getting instantaneous velocity
            differentiate = sympy.diff(equation, t)
            instantaneous_acceleration = round(float(sympy.simplify(differentiate.subs({t: _time}))), 2)

            # Display the result
            print("")
            print(("-" * 68).center(columns))
            print("ANSWER\n".center(columns))
            print(f"         Average Acceleration: {instantaneous_acceleration}m/s")
            break
        else:
            clear(2)


# Function for constant acceleration and free fall
def ConstantAcceleration_FreeFall_Calculation(_usage):
    # Initialize variable
    _p_i, _p_f, _v_i, _v_f, _a, _t = None, None, None, None, None, None

    # Checking for selected option to solve
    if _usage == "ConstantAcceleration":
        print("      Enter all the given (leave it blank if not given, or "'"?"'" if unknown): ")
        print("      NOTE: For unknown Displacement just put "'"0"'" in initial position and \n"
              "            "'"?"'" in final position.")
        print("")
    elif _usage == "FreeFall":
        _a = -9.8
        print("      Enter all the given (leave it blank if not given, or "'"?"'" if unknown): ")
        print("      NOTE: Ideal conditions without air resistance.\n"
              "            For unknown Displacement just put "'"0"'" in initial position and \n"
              "            "'"?"'" in final position.")
        print("")

    # Allow user to input the direction
    while True:
        if _usage == "ConstantAcceleration":
            direction = input("         Enter the direction(left/right): ").lower()
            if direction == "left" or direction == "right":
                break
            else:
                clear(1)

        elif _usage == "FreeFall":

            direction = input("         Enter the direction(upward/downward): ").lower()
            if direction == "upward" or direction == "downward":
                break
            else:
                clear(1)

    print("")
    var_symbol = None
    if _usage == "ConstantAcceleration":
        var_symbol = zip(["Initial position(m)", "Final position(m)", "Initial velocity(m/s)", "Final velocity(m/s)",
                          "Acceleration(m/s²)", "Time(s)"], [p_i, p_f, v_i, v_f, a, t])
    elif _usage == "FreeFall":
        var_symbol = zip(["Initial position(m)", "Final position(m)", "Initial velocity(m/s)", "Final velocity(m/s)",
                          "Time(s)"], [p_i, p_f, v_i, v_f, t])

    # Request the user to input the given
    for var, symbol in var_symbol:
        while True:
            user_input = input(f"         {var:<22}: ")
            try:
                if user_input:
                    if user_input == "?":
                        if len(Kinematic.Unknown) != 2:
                            Kinematic.Unknown.append(symbol)
                            Kinematic.Answer[symbol] = ""
                            print("\033[3E", end="")
                            clear(3)
                        else:
                            clear(1)
                            continue
                    else:
                        if direction == "left" or direction == "downward":
                            if symbol == p_f:
                                if p_i in Kinematic.Given:
                                    if float(user_input) < Kinematic.Given[p_i]:
                                        Kinematic.Given[symbol] = float(user_input)
                                        print("\033[3E", end="")
                                        clear(3)
                                    else:
                                        clear(1)
                                        print("\033[1E", end="")
                                        print("")
                                        print(("-" * 68).center(columns))
                                        print("      MSG: The final position must be less than the initial position.")
                                        print("\033[4F", end="")
                                        continue

                            if symbol == v_f:
                                if v_i in Kinematic.Given:
                                    if float(user_input) < Kinematic.Given[v_i]:
                                        Kinematic.Given[symbol] = float(user_input)
                                        print("\033[3E", end="")
                                        clear(3)
                                    else:
                                        clear(1)
                                        print("\033[1E", end="")
                                        print("")
                                        print(("-" * 68).center(columns))
                                        print("      MSG: The final velocity must be less than the initial velocity.")
                                        print("\033[4F", end="")
                                        continue
                        else:
                            if symbol == p_f:
                                if p_i in Kinematic.Given:
                                    if float(user_input) > Kinematic.Given[p_i]:
                                        Kinematic.Given[symbol] = float(user_input)
                                        print("\033[3E", end="")
                                        clear(3)
                                    else:
                                        clear(1)
                                        print("\033[1E", end="")
                                        print("")
                                        print(("-" * 68).center(columns))
                                        print("      MSG: The final position must be greater than the initial "
                                              "position.")
                                        print("\033[4F", end="")
                                        continue

                            if symbol == v_f:
                                if v_i in Kinematic.Given:
                                    if float(user_input) < Kinematic.Given[v_i]:
                                        Kinematic.Given[symbol] = float(user_input)
                                        print("\033[3E", end="")
                                        clear(3)
                                    else:
                                        clear(1)
                                        print("\033[1E", end="")
                                        print("")
                                        print(("-" * 68).center(columns))
                                        print("      MSG: The final velocity must be less than the initial "
                                              "velocity.")
                                        print("\033[4F", end="")
                                        continue
                        Kinematic.Given[symbol] = float(user_input)
                else:
                    Kinematic.Not_Given.append(symbol)
                    print("\033[3E", end="")
                    clear(3)
                break
            except ValueError:
                clear(1)

    for var, val in Kinematic.Given.items():
        if var == p_i:
            _p_i = val
        elif var == p_f:
            _p_f = val
        elif var == v_i:
            _v_i = val
        elif var == v_f:
            _v_f = val
        elif var == a:
            _a = val
        elif var == t:
            _t = val

    check_count = 8
    checking_variable = [x for x in Kinematic.Unknown]

    # Trying to solve the unknown variable the maximum try of the program is 8
    while len(Kinematic.Unknown) > 0:
        if check_count == 1:
            break
        var = checking_variable.pop(0)

        if var == t:
            answer = None
            try:
                if _usage == "ConstantAcceleration":
                    if all(x in Kinematic.Given for x in [v_i, v_f, a]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, a: _a}), t)
                    elif all(x in Kinematic.Given for x in [v_i, a, p_i, p_f]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, p_i: _p_i, p_f: _p_f}), t)
                    elif all(x in Kinematic.Given for x in [v_i, v_f, p_i, p_f]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, p_i: _p_i, p_f: _p_f}), t)

                elif _usage == "FreeFall":
                    if all(x in Kinematic.Given for x in [v_i, v_f]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, a: _a}), t)
                    elif all(x in Kinematic.Given for x in [v_i, p_i, p_f]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, p_i: _p_i, p_f: _p_f}), t)
                    elif all(x in Kinematic.Given for x in [v_i, v_f, p_i, p_f]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, p_i: _p_i, p_f: _p_f}), t)

                if len(answer) > 1:
                    for ans in answer:
                        if ans.is_real:
                            if ans > 0:
                                answer = round(float(ans), 2)
                        else:
                            real = sympy.im(ans)
                            if real > 0:
                                answer = round(float(real), 2)
                else:
                    answer = round(float(answer[0]), 2)

                Kinematic.Given[t] = answer
                Kinematic.Answer[t] = answer
                _t = answer
                Kinematic.Unknown.remove(t)
            except TypeError:
                checking_variable.append(var)
                pass

        elif var == a:
            answer = None
            try:
                if all(x in Kinematic.Given for x in [v_i, v_f, t]):
                    equation = Kinematic.Equation[1]
                    answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, t: _t}), a)[0]
                elif all(x in Kinematic.Given for x in [p_i, p_f, v_i, t]):
                    equation = Kinematic.Equation[2]
                    answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, v_i: _v_i, t: _t}), a)[0]
                elif all(x in Kinematic.Given for x in [v_i, v_f, p_i, p_f]):
                    equation = Kinematic.Equation[3]
                    answer = sympy.solve(equation.subs({v_i: _v_i, v_f: _v_f, p_i: _p_i, p_f: _p_f}), a)[0]

                answer = round(float(answer), 2)
                Kinematic.Given[a] = answer
                Kinematic.Answer[a] = answer
                _a = answer
                Kinematic.Unknown.remove(a)
            except TypeError:
                checking_variable.append(var)
                pass

        elif var == v_f:
            answer = None
            try:
                if _usage == "ConstantAcceleration":
                    if all(x in Kinematic.Given for x in [v_i, a, t]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, t: _t}), v_f)[0]
                    elif all(x in Kinematic.Given for x in [v_i, a, p_i, p_f]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, p_i: _p_i, p_f: _p_f}), v_f)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, v_i, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, v_i: _v_i, t: _t}), v_f)[0]

                elif _usage == "FreeFall":
                    if all(x in Kinematic.Given for x in [v_i, t]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, t: _t}), v_f)[0]
                    elif all(x in Kinematic.Given for x in [v_i, p_i, p_f]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_i: _v_i, a: _a, p_i: _p_i, p_f: _p_f}), v_f)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, v_i, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, v_i: _v_i, t: _t}), v_f)[0]

                answer = round(float(answer), 2)
                Kinematic.Given[v_f] = answer
                Kinematic.Answer[v_f] = answer
                _v_f = answer
                Kinematic.Unknown.remove(v_f)
            except TypeError:
                checking_variable.append(var)
                pass

        elif var == v_i:
            answer = None
            try:
                if _usage == "ConstantAcceleration":
                    if all(x in Kinematic.Given for x in [v_f, a, t]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_f: _v_f, a: _a, t: _t}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, a, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, a: _a, t: _t}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, v_f, a]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, v_f: _v_f, a: _a}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [v_f, p_i, p_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({v_f: _v_f, p_i: _p_i, p_f: _p_f, t: _t}), v_i)[0]

                elif _usage == "FreeFall":
                    if all(x in Kinematic.Given for x in [v_f, t]):
                        equation = Kinematic.Equation[1]
                        answer = sympy.solve(equation.subs({v_f: _v_f, a: _a, t: _t}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, a: _a, t: _t}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [p_i, p_f, v_f]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({p_i: _p_i, p_f: _p_f, v_f: _v_f, a: _a}), v_i)[0]
                    elif all(x in Kinematic.Given for x in [v_f, p_i, p_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({v_f: _v_f, p_i: _p_i, p_f: _p_f, t: _t}), v_i)[0]

                answer = round(float(answer), 2)
                Kinematic.Given[v_i] = answer
                Kinematic.Answer[v_i] = answer
                _v_i = answer
                Kinematic.Unknown.remove(v_i)
            except TypeError:
                checking_variable.append(var)
                pass

        elif var == p_f:
            answer = None
            try:
                if _usage == "ConstantAcceleration":
                    if all(x in Kinematic.Given for x in [p_i, v_i, a, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_i: _p_i, v_i: _v_i, a: _a, t: _t}), p_f)[0]
                    elif all(x in Kinematic.Given for x in [v_f, v_i, a, p_i]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_f: _v_f, v_i: _v_i, a: _a, p_i: _p_i}), p_f)[0]
                    elif all(x in Kinematic.Given for x in [p_i, v_i, v_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_i: _p_i, v_i: _v_i, v_f: _v_f, t: _t}), p_f)[0]

                elif _usage == "FreeFall":
                    if all(x in Kinematic.Given for x in [p_i, v_i, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_i: _p_i, v_i: _v_i, a: _a, t: _t}), p_f)[0]
                    elif all(x in Kinematic.Given for x in [v_f, v_i, p_i]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_f: _v_f, v_i: _v_i, a: _a, p_i: _p_i}), p_f)[0]
                    elif all(x in Kinematic.Given for x in [p_i, v_i, v_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_i: _p_i, v_i: _v_i, v_f: _v_f, t: _t}), p_f)[0]

                answer = round(float(answer), 2)
                Kinematic.Given[p_f] = answer
                Kinematic.Answer[p_f] = answer
                _p_f = answer
                Kinematic.Unknown.remove(p_f)
            except TypeError:
                checking_variable.append(var)
                pass

        elif var == p_i:
            answer = None
            try:
                if _usage == "ConstantAcceleration":
                    if all(x in Kinematic.Given for x in [p_f, v_i, v_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_f: _p_f, v_i: _v_i, v_f: _v_f, t: _t}), p_i)[0]
                    elif all(x in Kinematic.Given for x in [v_f, v_i, a, p_f]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_f: _v_f, v_i: _v_i, a: _a, p_f: _p_f}), p_i)[0]
                    elif all(x in Kinematic.Given for x in [p_f, v_i, a, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_f: _p_f, v_i: _v_i, a: _a, t: _t}), p_i)[0]

                elif _usage == "FreeFall":
                    if all(x in Kinematic.Given for x in [p_f, v_i, v_f, t]):
                        equation = Kinematic.Equation[4]
                        answer = sympy.solve(equation.subs({p_f: _p_f, v_i: _v_i, v_f: _v_f, t: _t}), p_i)[0]
                    elif all(x in Kinematic.Given for x in [v_f, v_i, p_f]):
                        equation = Kinematic.Equation[3]
                        answer = sympy.solve(equation.subs({v_f: _v_f, v_i: _v_i, a: _a, p_f: _p_f}), p_i)[0]
                    elif all(x in Kinematic.Given for x in [p_f, v_i, t]):
                        equation = Kinematic.Equation[2]
                        answer = sympy.solve(equation.subs({p_f: _p_f, v_i: _v_i, a: _a, t: _t}), p_i)[0]

                answer = round(float(answer), 2)
                Kinematic.Given[p_i] = answer
                Kinematic.Answer[p_i] = answer
                _p_i = answer
                Kinematic.Unknown.remove(p_i)
            except TypeError:
                checking_variable.append(var)
                pass

        check_count -= 1

    # Display the result
    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))

    if not Kinematic.Unknown and Kinematic.Given and Kinematic.Answer:
        if Kinematic.Answer:
            for var in Kinematic.Answer.keys():
                if var == p_i:
                    print(f"         Initial position : {Kinematic.Answer[var]}m")
                elif var == p_f:
                    print(f"         Final position   : {Kinematic.Answer[var]}m")
                elif var == v_i:
                    print(f"         Initial velocity : {Kinematic.Answer[var]}m/s")
                elif var == v_f:
                    print(f"         Final velocity   : {Kinematic.Answer[var]}m/s")
                elif var == a:
                    print(f"         Acceleration     : {Kinematic.Answer[var]}m/s²")
                elif var == t:
                    print(f"         Time             : {Kinematic.Answer[var]}s")

    elif Kinematic.Unknown and Kinematic.Given:
        for var in Kinematic.Answer.keys():
            if var == p_i:
                print(f"         Initial position : Not enough information to solve")
            elif var == p_f:
                print(f"         Final position   : Not enough information to solve")
            elif var == v_i:
                print(f"         Initial velocity : Not enough information to solve")
            elif var == v_f:
                print(f"         Final velocity   : Not enough information to solves")
            elif var == a:
                print(f"         Acceleration     : Not enough information to solve")
            elif var == t:
                print(f"         Time             : Not enough information to solve")

    elif not Kinematic.Unknown and Kinematic.Given:
        print("       No unknown variable to solve")

    elif not Kinematic.Unknown and not Kinematic.Given:
        print("       No unknown variable to solve")

    if t in Kinematic.Answer.keys():
        if Kinematic.Answer[t] < 0:
            print("")
            print("      NOTE: The time is negative; there is something wrong with the given.")

    # Clear all current used variable in kinematic class
    Kinematic.Given.clear()
    Kinematic.Not_Given.clear()
    Kinematic.Unknown.clear()
    Kinematic.Answer.clear()


# Function for finding displacement from acceleration
def FindingVelocity_Displacement_from_Acceleration():
    global fvda_select

    # Option for finding velocity and displacement from acceleration
    if not in_solving:
        print("      Select an option you want to solve:")
        print("         [1] Velocity and Displacement")
        print("         [2] Time at Maximum Velocity and Maximum Displacement")
        print("")

    while True:  # Checking for selected option
        if not in_solving:
            fvda_select = input("      Select: ")
            clear(5)

        if fvda_select == "1":
            print("Solve for Velocity and Displacement".center(columns))
            break
        elif fvda_select == "2":
            print("Solve for Time at Maximum Velocity and Maximum Displacement".center(columns))
            break
        else:
            clear(2)

    print("")
    # Request the user to input the equation
    while True:  # Checking if the equation is valid
        try:
            print("         Sample equation: (1.50 * t) - (0.120 * t^2)")
            equation = input("         Enter the acceleration equation: ")
            equation = equation.replace("^", "**")
            equation = sympy.sympify(equation)

            if equation.free_symbols == {t}:
                break
            else:
                clear(2)
        except TypeError:
            clear(2)
        except sympy.SympifyError:
            clear(2)

    x = sympy.Symbol("x")
    v = sympy.Symbol("v")
    c = sympy.Symbol("c")

    # Request the user to input the given
    print("")
    given_velocity = float_input("         Enter the given velocity(m/s)          : ")
    given_v_time = float_input("         Enter the given time(s) of velocity    : ")

    at_v_time = None
    max_velocity = None
    if fvda_select == "1":
        at_v_time = float_input("         Get the velocity at what time(s)?      : ")
    elif fvda_select == "2":
        max_velocity = float_input("         Enter the maximum velocity(m/s)        : ")

    given_position = float_input("         Enter the given position(m)            : ")
    given_p_time = float_input("         Enter the given time(s) of position    : ")

    at_p_time = None
    max_position = None
    if fvda_select == "1":
        at_p_time = float_input("         Get the displacement at what time(s)?  : ")
    elif fvda_select == "2":
        max_position = float_input("         Enter the maximum position(m)          : ")

    # Process for getting the velocity/displacement function
    first_integration = sympy.integrate(equation, t)
    velocity_equation = sympy.Eq(v, first_integration + c)
    c_velocity = sympy.solve(velocity_equation.subs({v: given_velocity, t: given_v_time}), c)[0]
    velocity_function = sympy.Eq(v, first_integration + c_velocity)

    second_integration = sympy.integrate(velocity_function.rhs, t)
    displacement_function = sympy.Eq(x, second_integration + c)
    c_displacement = sympy.solve(displacement_function.subs({x: given_position, t: given_p_time}), c)[0]
    displacement_function = sympy.Eq(x, second_integration + c_displacement)

    formatted_velocity_function = f"v = {convert_to_fraction(velocity_function.rhs)}"
    formatted_displacement_function = f"x = {convert_to_fraction(displacement_function.rhs)}"

    # Display the function
    print(("-" * 68).center(columns))
    print("")
    print("ANSWER\n".center(columns))
    print(f"         Velocity function           : {str(formatted_velocity_function).replace("**", "^")}")
    print(f"         Displacement function       : {str(formatted_displacement_function).replace("**", "^")}")

    # Checking now for selected option in finding velocity and displacement from acceleration
    if fvda_select == "1":
        # Process for getting velocity and displacement
        _velocity = round(float(sympy.solve(velocity_function.subs({t: at_v_time}), v)[0]), 2)
        _displacement = round(float(sympy.solve(displacement_function.subs({t: at_p_time}), x)[0]), 2)

        # Displace the result
        print(f"         Velocity at {f"{at_v_time}"+"s":<16}: {_velocity}m/s")
        print(f"         displacement at {f"{at_p_time}"+"s":<12}: {_displacement}m")
    elif fvda_select == "2":
        # Process for getting the time of maximum velocity and displacement
        v_time = sympy.solve(velocity_function.subs({v: max_velocity}), t)
        d_time = sympy.solve(displacement_function.subs({x: max_position}), t)

        v_total_time = ", ".join(f"{x}s" for x in [round(float(time), 2)
                                                   for time in v_time if time.is_real and time > 0])
        p_total_time = ", ".join(f"{x}s" for x in [round(float(time), 2)
                                                   for time in d_time if time.is_real and time > 0])
        if not p_total_time:
            p_total_time = ", ".join(f"{x}s" for x in [round(float(time.as_real_imag()[0]), 2) for time in d_time])

        # Display the result
        print(f"         Time at max velocity is     : {v_total_time}")
        print(f"         Time at max displacement is : {p_total_time}")


if __name__ == "__main__":
    # Title of console
    console_title = "Kinematics Calculator"

    run_as_administrator()  # Request for administration privilege

    # Check for single instances
    if not is_single_instance(console_title):
        exit()

    set_console_title(console_title)  # Set the title of console
    set_console_size(80, 40)  # Resizing of console
    columns = os.get_terminal_size().columns  # Save the new column size
    center_console_window()  # Align the console to center
    main()  # Calling main function
