from tkinter import *
import serial
import serial.tools.list_ports
import threading
import csv

serialPort = "/dev/ttyACM0"
baudRate = 9600
ser = serial.Serial(serialPort, baudRate) 
# sudo chmod 666 /dev/ttyACM0

# arduino_ports = [
#     p.device
#     for p in serial.tools.list_ports.comports()
#     if 'Arduino' in p.description  
# ]
# print(arduino_ports)
# ser = serial.Serial(arduino_ports[0])

class DataLogger:
    live_label_running = True
    text_content = []
    def __init__(self, root):
        self.root = root
        self.root.title("Modar Cube - Test Software")
        self.root.geometry("400x300")
        self.root.resizable(False,False)
        # self.root.iconbitmap('comet.ico')
        self.init_gui()



    def text_widget(self):
        self.live_text = Text(root)
        self.live_text.place(x=135, y=22, width = 250, height= 246)

    def get_data(self):

        filename = self.file_entry.get() + '.csv'

        if filename != ".csv":

            try:
                ser_bytes = ser.readline()
                decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                data = decoded_bytes.split()
                feilds = []

                with open(filename, "w") as csvfile:
                    csvwriter = csv.writer(csvfile, lineterminator = "\n")
                    csvwriter.writerow(feilds)

                while True:
                    try:
                        ser_bytes = ser.readline()
                        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                        data = decoded_bytes.split(" ", 0)
                        
                        with open(filename, "a") as csvfile:
                            csvwriter = csv.writer(csvfile, lineterminator = "\n")
                            csvwriter.writerow(data)
                        
                        self.live_text.insert(END, str(data) + "\n")
                        self.live_text.see("end")
                        print(data)

                        if DataLogger.live_label_running == False:
                            break
                    except:
                         print("UPSS SOMETHING HAS GONE WRONG - PLEASE RESTART")
                         break
            except:
                self.live_text.insert(END, "ERROR - COM PORT NOT FOUND" + "\n")
                DataLogger.live_label_running = False
                self.toggle_start()
        else:
            self.live_text.insert(END, "ERROR - PLEASE WRITE FILE NAME" + "\n")
            DataLogger.live_label_running = False
            self.toggle_start()

    def get_data_thread(self):
        self.thread2 = threading.Thread(target = self.get_data, name = "Getting Datta",)
        self.thread2.deamon = False
        self.thread2.start()
    
    def start_data(self):
        DataLogger.live_label_running = True
        self.get_data_thread()
        self.toggle_start()
    
    def pause_data(self):
        DataLogger.live_label_running = False
        self.toggle_start()

    def stop_data(self):
        DataLogger.live_label_running = False
        self.live_text.delete(1.0, END)
        self.toggle_start()

    def toggle_start(self):
        if DataLogger.live_label_running == True:
            self.start_button.configure(state = "disabled")
        else:
            self.start_button.configure(state = "normal")

    def MagnetOn(self):
        DataLogger.live_label_running = True
        ser.write('1'.encode())
        #print("Magnet is ON")

    def MagnetOff(self):
        DataLogger.live_label_running = True
        ser.write('2'.encode())
        #print("Magnet is OFF")
    
    def left_widgets(self):
        self.filelabel = Label(root, text = 'File Name :')
        self.filelabel.place(x=10, y=8)

        self.file_entry = Entry(root)
        self.file_entry.place(x=10, y=30, width=100, height=25)
   
        self.CometLabel = Label(root, text = "Comet Ingenieria" + "\n" + "Valencia 2021", fg ="Black", font = ("Arial", 9, "bold"))
        self.CometLabel.place(x=200, y=268)

        self.BeginLabel = Label(root, text = "Test Software", fg ="Black", font = ("Arial", 9, "bold"))
        self.BeginLabel.place(x=200, y=1)

    def bottom_buttons(self):
        self.start_button = Button(root, text = "Start", command = lambda: self.start_data())
        self.start_button.place(x=10, y=80, width=100, height=30)

        self.BtnOn = Button(root, text = "Magnet ON", cursor='hand2', command=lambda: self.MagnetOn())
        self.BtnOn.place(x=10, y=120, width=100, height=30)
        
        self.BtnOff = Button(root, text = "Magnet OFF", cursor='hand2', command=lambda: self.MagnetOff())
        self.BtnOff.place(x=10, y=160, width=100, height=30)  

        self.pause_button = Button(root, text = "Pause", command = lambda: self.pause_data())
        self.pause_button.place(x=10, y=240, width=100, height=30)

        self.stop_button = Button(root, text = "Stop", command = lambda: self.stop_data())
        self.stop_button.place(x=10, y=200, width=100, height=30)


    def init_gui(self):
        self.text_widget()
        self.left_widgets()
        self.bottom_buttons()

if __name__ == "__main__":
    root = Tk()
    DataLogger(root)
    root.mainloop()