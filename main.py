import psutil
import tkinter as tk
import matplotlib.animation as animation
import threading
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(f"{proc.info['pid']} - {proc.info['name']}")
    return processes

def end_process():
    selected_index = processes_listbox.curselection()
    if selected_index:
        selected_process = processes_listbox.get(selected_index)
        pid = int(selected_process.split()[0])
        try:
            process = psutil.Process(pid)
            process.terminate()
            messagebox.showinfo("Success", f"Process {pid} terminated successfully!")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "Process already terminated or does not exist.")
    else:
        messagebox.showerror("Error", "Please select a process to terminate.")

def sort():
    processes = get_processes()
    processes_listbox.delete(0, tk.END)
    for proc in processes:
        processes_listbox.insert(tk.END, proc)

def search_processes():
    keyword = search_entry.get().lower()
    processes = get_processes()
    processes_listbox.delete(0, tk.END)
    for proc in processes:
        if keyword in proc.lower():
            processes_listbox.insert(tk.END, proc)

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.05)

def animate_cpu_usage(i):
    y.append(get_cpu_usage())
    if len(y) > 50:
        y.pop(0)
    line.set_ydata(y)
    ax.set_ylim(0, 100)
    return line,

def start_animation():
    global ani
    ani = animation.FuncAnimation(fig, animate_cpu_usage, interval=500)
    ax.set_xlabel('Time')
    ax.set_ylabel('CPU Usage (%)')
    ani_thread = threading.Thread(target=ani._start)
    ani_thread.daemon = True
    ani_thread.start()

def get_memory_usage():
    return psutil.virtual_memory().percent

def animate_memory_usage(i):
    y_memory.append(get_memory_usage())
    if len(y_memory) > 50:
        y_memory.pop(0)
    line_memory.set_ydata(y_memory)
    ax_memory.set_ylim(0, 100)
    return line_memory,

def start_memory_animation():
    global ani_memory
    ani_memory = animation.FuncAnimation(fig_memory, animate_memory_usage, interval=500)
    ax_memory.set_xlabel('Time')
    ax_memory.set_ylabel('Memory Usage (%)')
    ani_memory_thread = threading.Thread(target=ani_memory._start)
    ani_memory_thread.daemon = True
    ani_memory_thread.start()

root = tk.Tk()

root.title("Process Manager")

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Processes')

search_frame = tk.Frame(tab1)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_processes)
search_button.pack(side=tk.LEFT)

processes_label = tk.Label(tab1, text="Processes:")
processes_label.pack()

processes_listbox = tk.Listbox(tab1, selectmode=tk.SINGLE, height=30, width=50)
processes_listbox.pack()

sort_button = tk.Button(tab1, text="Sort", command=sort)
sort_button.pack()

end_button = tk.Button(tab1, text="End Process", command=end_process)
end_button.pack()

sort()

tab2 = ttk.Frame(tab_control)

tab_control.add(tab2, text='CPU Usage')
tab_control.pack(expand=1, fill='both')

fig = Figure(figsize=(5, 4), dpi=100)
y = [0] * 50
ax = fig.add_subplot(111)
line, = ax.plot(y)

canvas = FigureCanvasTkAgg(fig, master=tab2)
canvas.draw()
canvas.get_tk_widget().pack()

start_button = tk.Button(tab2, text="Start", command=start_animation)
start_button.pack()

tab3 = ttk.Frame(tab_control)

tab_control.add(tab3, text='Memory Usage')

fig_memory = Figure(figsize=(5, 4), dpi=100)
y_memory = [0] * 50
ax_memory = fig_memory.add_subplot(111)
line_memory, = ax_memory.plot(y_memory)

canvas_memory = FigureCanvasTkAgg(fig_memory, master=tab3)
canvas_memory.draw()
canvas_memory.get_tk_widget().pack()

start_button_memory = tk.Button(tab3, text="Start", command=start_memory_animation)
start_button_memory.pack()

root.mainloop()