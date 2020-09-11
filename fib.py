# Import statements
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
import sys, re, time, multiprocessing

# Window interface class
class Window(QMainWindow):
    # Initalization function
    def __init__(self): 
        super().__init__()
        self.title = 'Fibonacci Sequence'
        self.x, self.y, self.w, self.h = 400, 300, 500, 300
        self.initUI()

    # UI intialization function
    def initUI(self):
        # Sets window title and size
        self.setWindowTitle(self.title) 
        self.setGeometry(self.x, self.y, self.w, self.h)

        # Creates text on the screen
        self.l1 = QLabel('Enter a number and watch the two functions find', self) 
        self.l1.move(100, 10)
        self.l1.resize(300,30)
        
        self.l2 = QLabel('the nth number in the fibonacci sequence', self) 
        self.l2.move(120, 30)
        self.l2.resize(300,30)

        self.l3 = QLabel('Recursion', self) 
        self.l3.move(70, 130)
        self.l3.resize(300,30)

        self.l4 = QLabel('Recursion and', self) 
        self.l4.move(330, 120)
        self.l4.resize(300,30)

        self.l5 = QLabel('Memoization', self) 
        self.l5.move(335, 135)
        self.l5.resize(300,30)

        self.fibtxt = QLabel('', self)
        self.fibtxt.move(60, 170)
        self.fibtxt.resize(300,30)

        self.fibmtxt = QLabel('', self)
        self.fibmtxt.move(325, 170)
        self.fibmtxt.resize(300,30)

        self.fibtime = QLabel('', self)
        self.fibtime.move(30, 200)
        self.fibtime.resize(300,30)

        self.fibmtime = QLabel('', self)
        self.fibmtime.move(295, 200)
        self.fibmtime.resize(300,30)

        # Creates an input box on the screen
        self.t1 = QLineEdit(self)
        self.t1.move(230, 60)
        self.t1.resize(50,20)

        # Creates a button on the screen
        self.b1 = QPushButton('Go', self)
        self.b1.move(230,90)
        self.b1.clicked.connect(self.onClick)
        self.b1.resize(50,30)

        self.show()                                                             # Draws the screen

    # Function when the button is clicked
    def onClick(self):
        self.num = self.t1.text()
        if self.num.isdigit() and int(self.num) > 0:                            # Checks if the input is a number that is greater than zero
            # Times how long it takes the fibonacci and memoization sequence to run
            start = time.perf_counter()
            fibNum = fibmemo(int(self.num))
            self.fibmtxt.setText('fib(' + self.num + ') = ' + str(fibNum))      # Sets the fibonacci number in the label
            memt = str(round(time.perf_counter()-start,5))                      # The time taken to find the number 
            # Formats the time taken to find the number and sets it as the label
            if 'e' in memt:
                memt = '0.0000' + memt[0]
            elif memt[0] != '0':
                memt = str(round(float(memt),2))
            self.fibmtime.setText(memt + ' seconds to calculate')
            # Times how long it takes the fibonacci sequence to run
            start = time.perf_counter()
            p = multiprocessing.Process(target=fib, name="fib", args=(int(self.num),))
            p.start()
            p.join(20)
            # If the sequence is still running after 20 seconds the fibonacci sequence will stop calculating
            if p.is_alive():
                p.terminate()
                p.join()
                self.fibtxt.setText('Took too long to calculate')               # Displays the error message on the screen
                self.fibtime.setText('')
            # If the sequence finished running sets the time and number in the labels
            else:
                self.fibtxt.setText('fib(' + self.num + ') = ' + str(fibNum))
                fibt = str(round(time.perf_counter()-start,2))
                self.fibtime.setText(fibt + ' seconds to calculate')
                
# Fibonacci sequence function
def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n-1) + fib(n-2)

# Fibonacci and memoization function
fibCache = {}
def fibmemo(n):
    if n in fibCache:
        return fibCache[n]
    elif n == 1 or n == 2:
        value = 1
    else:
        value = fibmemo(n-1) + fibmemo(n-2)
    fibCache[n] = value
    return value

# Runs the code  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
