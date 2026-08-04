# 간단한 계산기 프로그램

import tkinter as tk

# 계산 함수
def click(button):
    current = entry.get()

    if button == "=":
        try:
            result = eval(current)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    elif button == "C":
        entry.delete(0, tk.END)

    else:
        entry.insert(tk.END, button)


# 윈도우 생성
window = tk.Tk()
window.title("Python Calculator")
window.geometry("300x400")

# 입력창
entry = tk.Entry(
    window,
    font=("Arial", 20),
    justify="right"
)
entry.pack(
    padx=10,
    pady=10,
    fill="both"
)


# 버튼 배치
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
    "C"
]


frame = tk.Frame(window)
frame.pack()


row = 0
col = 0

for button in buttons:
    btn = tk.Button(
        frame,
        text=button,
        width=5,
        height=2,
        font=("Arial", 15),
        command=lambda b=button: click(b)
    )

    btn.grid(row=row, column=col, padx=3, pady=3)

    col += 1

    if col == 4:
        col = 0
        row += 1


window.mainloop()