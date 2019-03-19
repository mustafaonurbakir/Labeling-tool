import os
import _thread
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import pandas as pd
import numpy as np
import sys
import tkinter as tkinter
from tkinter import filedialog

from ttkthemes import themed_tk as tk
import ttk

from PIL import ImageTk, Image
from tkinter import Label, Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation 


import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

gi.require_version('GstVideo', '1.0')
from gi.repository import GstVideo


theme = "plastik"
global datas
global window
global is_play #play or pause
global is_play_video
global current_data_line
global is_file_available

#create the graphs
class FigureAnimator:
	def __init__(self, data_list, ylim=100,is_master=False):
		self.data_list = data_list
		self.local_point_counter = 0
		
		self.fig = plt.figure(dpi=50, figsize=(3, 3))
		ax = plt.axes(xlim=(0, 100), ylim=(0, ylim))
		#ax.set_xlabel('time')
		self.line, = ax.plot([], [], lw=2)
		self.is_master = is_master
	
	def init_data(self):
		self.line.set_data([], [])
		return self.line,
	
	def animate_data(self, i):
		
		if self.is_master:
			window.show_featudatas(self.local_point_counter)

		#grafikleri durdurma
		global is_play
		if is_play == 1:
			self.local_point_counter += 1
		elif is_play == 0:
			pass
		"""
		if self.local_point_counter < 100:
			temp_local_point = self.local_point_counter
		else:
			temp_local_point = 100
		"""
		x = np.linspace(0,150,100)
		y = self.data_list[self.local_point_counter:self.local_point_counter+100]

		self.line.set_data(x, y)
		return self.line,
	  
# this is main window
class Window():
	def __init__(self, master, data):
		self.master = master
		pad=3
		#self._geom='200x200+1+1'
		master.geometry("{0}x{1}+0+0".format( master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		
		self.master.bind('<z>', self.z_key)
		self.master.bind('<x>', self.x_key)
		self.master.bind('<c>', self.c_key)
		self.master.bind('<space>', self.space_key)
		
		#status bar
		"""
		self.status_frame = tkinter.Frame(self.master)
		self.status = tkinter.Label(self.status_frame, text="this is the status bar")
		self.status.pack(fill="both", expand=True)
		self.status_frame.grid(row=15, column=0, columnspan=2, sticky="ew")
		
		self.some_status = tkinter.Label(self.master, text="status bar", bg="#dfdfdf")
		self.some_status.grid(row=10, column=0, columnspan=2, sticky="we")
		"""
		
		#it store the information of buttons
		self.last_situation = 0

		# self.master.geometry('1200x600')
		self.master.title("Labeling Tool")

		self.video_path = vid_path

		self.acc_data = data["SPEED"].diff()

		self.time = data["TIME"]

		self.speed_data = data["SPEED"]
		self.speed_data = np.concatenate([np.zeros(70),self.speed_data])
		#print ("speed_data")
		self.rpm_data = data["RPM"]
		self.rpm_data = np.concatenate([np.zeros(70),self.rpm_data])

		self.engine_load = data["ENGINE_LOAD"]
		self.engine_load = np.concatenate([np.zeros(70),self.engine_load])

		self.throttle_pos = data["THROTTLE_POS"]
		self.throttle_pos = np.concatenate([np.zeros(70),self.throttle_pos])

		self.label_data = data["LABEL"]
		#print("label_data")
		
		####################################################################################################################
		
		#video
		self.video_frame = tkinter.Frame(master, bg='',width=500, height=300)
		self.video_frame_id = self.video_frame.winfo_id()

		self.player = Gst.ElementFactory.make('playbin', None)
		self.player.set_property('uri', 'file://%s' % vid_path)
		
		self.player.set_state(Gst.State.PAUSED)

		self.bus = self.player.get_bus()
		self.bus.enable_sync_message_emission()
		self.bus.connect('sync-message::element', self.set_frame_handle, self.video_frame_id)

		#video frame"
		self.video_frame.grid(row=1,column=1,rowspan=2,columnspan=10)
		"""
		w = tkinter.Canvas(master, width=500, height=300)
		w.create_rectangle(500, 0, 100, 300, fill='red')
		w.grid(row=1, column=1, rowspan = 2, columnspan=10)
		"""
		####################################################################################################################
		#butonun yazisi
		global btn_text
		btn_text = tkinter.StringVar()
		btn_text.set(">")
		
		#videonun altındaki 3 buton
		ttk.Button(text="Videoyu ilk hareket anına kadar oynatabilirsiniz.", command=self.play_pause_video).grid(row=6,column=1, columnspan=3, padx=5, pady=5)
		ttk.Button(text="<<", command=self.move_plot_prev).grid(row=7,column=1)
		ttk.Button(text=">>", command=self.move_plot_next).grid(row=7,column=3)
		ttk.Button(textvariable=btn_text, command=self.play_pause).grid(row=7,column=2)
		ttk.Button(text="So Bad (z)", command=self.set_bad).grid(row=8,column=1)
		#tkinter.Button(text="Bad", command=self.move_plot_next).grid(row=8,column=2)
		ttk.Button(text="Normal (x)", command=self.set_normal).grid(row=8,column=2)
		ttk.Button(text="Fine (c)", command=self.set_good).grid(row=8,column=3)
		ttk.Button(text="Save", command=self.save_to_csv).grid(row=8,column=5)

		####################################################################################################################
		#images
		####################################################################################################################
		#plots
		#speed plot 
		self.speed_animator = FigureAnimator(self.speed_data, is_master=True)
		self.speed_canvas = FigureCanvasTkAgg(self.speed_animator.fig, master=self.master)
		self.speed_canvas.get_tk_widget().config(width=150, height=150)
		#rpm plot
		self.rpm_animator = FigureAnimator(self.rpm_data,ylim=5000)
		self.rpm_canvas = FigureCanvasTkAgg(self.rpm_animator.fig, master=self.master)
		self.rpm_canvas.get_tk_widget().config(width=150, height=150)
		#engine load plot
		self.engine_load_animator = FigureAnimator(self.engine_load,ylim=110)
		self.load_canvas = FigureCanvasTkAgg(self.engine_load_animator.fig, master=self.master)
		self.load_canvas.get_tk_widget().config(width=150, height=150)
		#throttle position  plot
		self.throttle_pos_animator = FigureAnimator(self.throttle_pos,ylim=110)
		self.throttle_canvas = FigureCanvasTkAgg(self.throttle_pos_animator.fig, master=self.master)
		self.throttle_canvas.get_tk_widget().config(width=150, height=150)

		#grafikler ve baslikleri
		#tkinter.Label(text="SPEED").grid(column=12,row=0)
		self.speed_canvas.get_tk_widget().grid(column=13,row=7, padx=10, pady=10, columnspan=2, rowspan=4)	   

		#tkinter.Label(text="RPM").grid(column=13,row=0)
		self.rpm_canvas.get_tk_widget().grid(column=16,row=7, padx=10, pady=10, columnspan=2, rowspan=4)

		#tkinter.Label(text="% Engine Load").grid(column=13,row=2)
		self.load_canvas.get_tk_widget().grid(column=19,row=7, rowspan=4, padx=10, pady=10, columnspan=2)

		#tkinter.Label(text="% Throttle Position").grid(column=12, row=2)
		self.throttle_canvas.get_tk_widget().grid(column=22,row=7, rowspan=4, padx=10, pady=10, columnspan=2)

		####################################################################################################################
		#basina bosluk
		self.acc_label = tkinter.Label(text="	  ")
		self.acc_label.grid(column=0, row=0)


	def show_featudatas(self, i):

		speed_change  = self.speed_data[i+100] - self.speed_data[i+90]
		speed_change = speed_change*10 / 36
		
		if self.last_situation == 1:
			datas.at[i+100, "LABEL"] = "bad"

		elif self.last_situation == 2:
			datas.at[i+100, "LABEL"] = "good"
		
		global current_data_line
		current_data_line = i 


		""" if speed_change > 1.8:
			self.acc_label.config(text="HIGH ACCELERATION",bg="red")

		elif speed_change < -2.6:
			self.acc_label.config(text="HARSH BRAKING",bg="red")
		else:
			self.acc_label.config(text="NO SPECIFIC EVENT",bg="yellow")
		#REFACTOR UP THERE
		 """
		if i % 10 == 0:
			speed  = self.speed_data[i+70] / 280
			rpm = self.rpm_data[i+70] / 6000
			print( "speed", self.speed_data[i+70])
			print( "rpm", self.rpm_data[i+70])
			print( "f1",speed/rpm)

	def move_plot_next(self):
		self.speed_animator.local_point_counter += 10
		self.rpm_animator.local_point_counter += 10
		self.engine_load_animator.local_point_counter += 10
		self.throttle_pos_animator.local_point_counter += 10

	def move_plot_prev(self):
		self.speed_animator.local_point_counter -= 10
		self.rpm_animator.local_point_counter -= 10
		self.engine_load_animator.local_point_counter -= 10
		self.throttle_pos_animator.local_point_counter -= 10
	
	def play_pause(self):
		global is_play
		global btn_text

		if is_play == 1:
			btn_text.set(">")
			is_play = 0
			self.player.set_state(Gst.State.PAUSED)
		elif is_play == 0:
			btn_text.set("||")
			is_play = 1
			self.player.set_state(Gst.State.PLAYING)

	def play_pause_video(self):
		global is_play_video
		if is_play_video == 1:
			self.player.set_state(Gst.State.PAUSED)
			is_play_video == 0
		elif is_play_video == 0:
			self.player.set_state(Gst.State.PLAYING)
			is_play_video = 1

	def set_frame_handle(self, bus, message, frame_id):
		if not message.get_structure() is None:
			if message.get_structure().get_name() == 'prepare-window-handle':
				display_frame = message.src
				display_frame.set_property('force-aspect-ratio', True)
				display_frame.set_window_handle(frame_id)

	def set_good(self):
		self.last_situation = 1
		print(self.last_situation)

	def set_normal(self):
		self.last_situation = 0
		print(self.last_situation)
	
	def set_bad(self):
		self.last_situation = 2
		print(self.last_situation)
	
	def save_to_csv(self):
		try:
			datas.to_csv("file.csv", sep='\t')
			tkinter.messagebox.showinfo("Saved", "File is saved.")
		except:
			tkinter.messagebox.showerror("Error!", "An error occurred while saving!")

	@staticmethod
	def z_key(event):
		print("key press: z")
		window.set_good()
	
	@staticmethod
	def x_key(event):
		print("key press: x")
		window.set_normal()
	
	@staticmethod
	def c_key(event):
		print("key press: c")
		window.set_bad()
	
	@staticmethod
	def space_key(event):
		print("key press: space")
		window.play_pause()

#this window manage the file dialogs	
class Window2():
	def __init__(self, master2):
		self.master2 = master2
		self.master2.geometry("600x400")
		self.master2.title("file dialogs")
		
		#file dialogs
		global text_var
		text_var = tkinter.StringVar()
		text_var.set("no file")
		global text_var2
		text_var2 = tkinter.StringVar()
		text_var2.set("no file")
		
		
		ttk.Label(self.master2, text="Data file: ").grid(row=1, padx=5, pady=5)
		ttk.Entry(self.master2, textvariable = text_var , width=20).grid(row=1, column=2)
		ttk.Button(self.master2, text="Browse", command=self.load_file, width=10).grid(row=1, column=4, padx=5, pady=5)
		
		ttk.Label(text="Video file: ").grid(row=3, padx=5, pady=5)
		ttk.Entry(self.master2,textvariable=text_var2, width=20).grid(row=3, column=2)
		ttk.Button(text="Browse", command=self.load_file2, width=10).grid(row=3, column=4, padx=5, pady=5)

		ttk.Button(text="Next", command=self.check_files).grid(row=8,column=4, padx=5, pady=5)
		ttk.Button(text="Cancel", command=self.do_exitt).grid(row=8,column=5, padx=5, pady=5)
		
		
	def load_file(self):
		global file_path_data
		path = os.getcwd()
		file_path = filedialog.askopenfilename(initialdir = path, filetypes=(("Txt files", "*.txt"),("All files", "*.*") ))
		
		if file_path:
			try:
				global text_var
				file_path_data=file_path
				text_var.set(file_path)
			except:
				tkinter.showerror("Browse File", "Failed to read file\n'%s'" % file_path_data)
	
	def load_file2(self):
		global file_path_video
		path = os.getcwd()
		file_path = filedialog.askopenfilename(initialdir = path, filetypes=(("Mp4 files", "*.mp4"),("Avi files", "*.avi"),("All files", "*.*") ))
		
		if file_path:
			try:
				global text_var2
				file_path_video=file_path
				text_var2.set(file_path)
			except:
				tkinter.showerror("Browse File", "Failed to read file\n'%s'" % file_path_video)
	
	def check_files(self):
		global file_path_data
		global file_path_video
		global is_file_available
		print(file_path_data)
		print(file_path_video)
		if file_path_data == None or file_path_video == None:
			tkinter.messagebox.showerror("File Browser", "Please select file")
		else:
			is_file_available = True
			self.master2.quit()
			
	def do_exitt(self):
		global is_file_available
		is_file_available = False
		self.master2.quit()
			
#this function parse the datas
def parse_data(fl_name):
	engine_load = np.empty(shape=[0,1])
	rpm = np.empty(shape=[0,1])
	speed = np.empty(shape=[0,1])
	throttle_pos = np.empty(shape=[0,1])
	accelerator_pos = np.empty(shape=[0,1])
	time = np.empty(shape=[0,1])
	
	
	
	fp = open(fl_name)
	lines = fp.readlines()

	for counter in range(0,len(lines), 6):

		engine_load = np.append(engine_load, [float(lines[counter].split()[-2])])
		rpm = np.append(rpm, float(lines[counter+1].split()[-2]))
		speed = np.append(speed, float(lines[counter+2].split()[-2]))
		throttle_pos = np.append(throttle_pos, float(lines[counter+3].split()[-2]))
		accelerator_pos = np.append(accelerator_pos, float(lines[counter+4].split()[-2]))
		time = np.append(time, float("".join(lines[counter+4].split()[1].split(":"))[:-3]))

	datas = pd.DataFrame()
	datas["ENGINE_LOAD"] = engine_load
	datas["RPM"] = rpm
	datas["SPEED"] = speed
	datas["THROTTLE_POS"] = throttle_pos
	datas["ACC_D"] = accelerator_pos
	datas["LABEL"] = "normal"
	datas["TIME"] = time
	return datas
	
#this class provide information to qml files
class Cluster(QObject):
	def __init__(self):
		QObject.__init__(self)
		
	kphResult = pyqtSignal(int, arguments=['kph'])
	powerResult = pyqtSignal(int, arguments=['power'])
 
	# Slot for summing two numbers
	@pyqtSlot()
	def kph(self):
		self.kphResult.emit(datas.at[current_data_line, "SPEED"])
	
	# Slot for subtraction of two numbers
	@pyqtSlot()
	def power(self):
		self.powerResult.emit(datas.at[current_data_line, "RPM"]/100)
 
# this function work as a thread
# this start qml files and window
def qml_thread(threadName, delay):
	import sys

	# Create an instance of the application
	app = QGuiApplication(sys.argv)
	# Create QML engine
	engine = QQmlApplicationEngine()
	
	cluster = Cluster()
	# And register it in the context of QML
	engine.rootContext().setContextProperty("cluster", cluster)
	
	try:
		engine.load("cluster/qml/Cluster.qml")
		engine.quit.connect(app.quit)
		sys.exit(app.exec_())
	except:
		print("qml dosyasi acilamadi")
	

if __name__ == "__main__":
	
	#global is_play
	#video oynarak baslamasin
	is_play = 0
	is_play_video = 0
	file_path_data = None
	file_path_video = None
	is_file_available = False
	interval = 190
	"""
	data_files = ["record_bad.txt"]
	datas = parse_data(data_files[0])
	vid_path = os.path.abspath(sys.argv[1])
	"""
	
	Gst.init(None)
	GObject.threads_init()
	

	####################################################################################################################
	#file browser screen
	
	master = tk.ThemedTk()
	master.get_themes()
	master.set_theme(theme)
	
	window2= Window2(master)
	master.mainloop()
	master.destroy()
	
	#if there is no file -> exit
	print("is file avaible:" ,is_file_available)
	if is_file_available != True:
		sys.exit(0)
	
	data_files = [file_path_data]
	datas = parse_data(data_files[0])
	print (datas)
	
	
	vid_path = file_path_video
	
	
	####################################################################################################################
	#Main window
	master = tk.ThemedTk()
	master.get_themes()
	master.set_theme(theme)
	window = Window(master, datas)
	
	####################################################################################################################
	#Menu functions
	def hello():
		print ("hello!")
		
	def about_windows():
		tkinter.messagebox.showinfo("About", "With this app you can give labels to videos and driving data. \n Mustafa Onur Bakır")
	
	#Menubar 
	menubar = tkinter.Menu(master)
	# create a pulldown menu, and add it to the menu bar
	filemenu = tkinter.Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=hello)
	filemenu.add_command(label="Save", command=window.save_to_csv)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=master.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	# create a pulldown menu, and add it to the menu bar
	helpmenu = tkinter.Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=about_windows)
	menubar.add_cascade(label="Help", menu=helpmenu)
	
	master.config(menu=menubar)
	
	####################################################################################################################
	
	
	anim_speed = animation.FuncAnimation(window.speed_animator.fig, window.speed_animator.animate_data, init_func=window.speed_animator.init_data,
							   frames=len(datas), interval=interval, blit=True, repeat_delay=interval)
		
	anim_rpm = animation.FuncAnimation(window.rpm_animator.fig, window.rpm_animator.animate_data, init_func=window.rpm_animator.init_data,
							   frames=len(datas), interval=interval, blit=True, repeat_delay=interval)

	anim_load = animation.FuncAnimation(window.engine_load_animator.fig, window.engine_load_animator.animate_data, init_func=window.engine_load_animator.init_data,
							   frames=len(datas), interval=interval, blit=True, repeat_delay=interval)

	anim_throttle = animation.FuncAnimation(window.throttle_pos_animator.fig, window.throttle_pos_animator.animate_data, init_func=window.throttle_pos_animator.init_data,
							   frames=len(datas), interval=interval, blit=True, repeat_delay=interval)
	
	
	#qml islemleri ayri bir threadda gerceklesiyor
	try:
		_thread.start_new_thread(qml_thread, ("Qml thread", 2, ))
	except:
		print("thread olusmadi")

	master.mainloop()
