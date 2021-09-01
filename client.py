import socket
from tkinter import *
import tkinter as tk
from  threading import Thread
import random
from PIL import ImageTk, Image
from tkmacosx import Button
import platform


screen_width = None
screen_height = None

SERVER = None
PORT  = 8080
IP_ADDRESS = '127.0.0.1'
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

ticketGrid  = []
currentNumberList = []
markedNumberList = []
flashNumberList = []
flashNumberLabel = None
gameOver = False

#bp
def showWrongMarking():
    global ticketGrid
    global flashNumberList

    # changing background color of number which is not flash yet on screen
    for row in ticketGrid:
        for numberBox in row:
            if(numberBox['text']):
                if(int(numberBox['text']) not in flashNumberList):
                    if(platform.system() == 'Darwin'):
                        # For Mac Users
                        numberBox.configure(state='disabled', disabledbackground='#f48fb1',
                            disabledforeground="white")
                    else:
                        # For Windows Users
                        numberBox.configure(state='disabled', background='#f48fb1',
                            foreground="white")

#bp
def markNumber(button):
    global markedNumberList
    global flashNumberList
    global playerName
    global SERVER
    global currentNumberList
    global gameOver
    global flashNumberLabel
    global canvas2

    buttonText = int(button['text'])
    markedNumberList.append(buttonText)

    # Make button disabled and changing color to green
    if(platform.system() == 'Darwin'):
        # For Mac Users
        button.configure(state='disabled',disabledbackground='#c5e1a5', disabledforeground="black", highlightbackground="#c5e1a5")
    else:
        # For Windows Users
        button.configure(state='disabled',background='#c5e1a5', foreground="black")




    # NOTE: Example
    # List1
    # List1 = ['python' ,  'javascript', 'csharp', 'go', 'c', 'c++']

    # List2
    # List2 = ['csharp1' , 'go', 'python']

    # print("The list {} contains all elements of the list {}".format(List1, List2))
    # The list ['python', 'javascript', 'csharp', 'go', 'c', 'c++'] contains all elements of the list ['csharp', 'go', 'python']


    winner =  all(item in flashNumberList for item in markedNumberList)

    if(winner and sorted(currentNumberList) == sorted(markedNumberList)):
        message = playerName + ' wins the game.'
        SERVER.send(message.encode())
        return

    # When user lose the game
    if(len(currentNumberList) == len(markedNumberList)):
        winner =  all(item in flashNumberList for item in markedNumberList)
        if(not winner):
            gameOver = True
            message = 'You Lose the Game'
            canvas2.itemconfigure(flashNumberLabel, text = message, font = ('Chalkboard SE', 40))
            showWrongMarking()



def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        # getting random 5 cols
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1

        # Here key is index and values are numbers
        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }

        # placing a number to particular position in the ticket
        counter = 0
        while (counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black")
                currentNumberList.append(randomNumber)

                counter+=1


    # changing background color of blank number box to different color
    for row in ticketGrid:
        for numberBox in row:
            if(not numberBox['text']):
                if(platform.system() == 'Darwin'):
                    # For Mac Users
                    numberBox.configure(state='disabled', disabledbackground='#ff8a65', highlightbackground='#ff8a65')
                else:
                    # For Windows users
                    numberBox.configure(state='disabled', background='#ff8a65')


def createTicket():
    global gameWindow
    global ticketGrid
    # Ticket Frame
    mianLable = Label(gameWindow, width=65, height=16,relief='ridge', borderwidth=5, bg='white')
    mianLable.place(x=95, y=119)

    xPos = 105
    yPos = 130
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            if(platform.system() == 'Darwin'):
                # For Mac users
                boxButton = Button(gameWindow,
                font = ("Chalkboard SE",18),
                borderwidth=3,
                pady=23,
                padx=-22,
                bg="#fff176", # Initial Yellow color
                highlightbackground='#fff176',
                activebackground='#c5e1a5') # onPress Green Color

                # Using Lambda Function
                boxButton.configure(command = lambda boxButton : markNumber(boxButton))

                boxButton.place(x=xPos, y=yPos)
            else:
                # For windows users
                boxButton = tk.Button(gameWindow, font = ("Chalkboard SE",30), width=3, height=2,borderwidth=5, bg="#fff176")
                boxButton.configure(command = lambda boxButton : markNumber(boxButton))
                boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64
        ticketGrid.append(rowList)
        xPos = 105
        yPos +=82



def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton
    global flashNumberLabel


    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/4.5,50, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="#3e2723")

    createTicket()
    placeNumbers()


    # Flash Number Label
    flashNumberLabel = canvas2.create_text(400,screen_height/2.3, text = "Waiting for other to join...", font=("Chalkboard SE",30), fill="#3e2723")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/4.5,screen_height/8, text = "Enter Name", font=("Chalkboard SE",60), fill="#3e2723")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/7, y=screen_height/5.5 )

    button = tk.Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=11, command=saveName, height=2, bd=3)
    button.place(x = screen_width/6, y=screen_height/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def recivedMsg():
    global SERVER
    global displayedNumberList
    global flashNumberLabel
    global canvas2
    global gameOver

    numbers = [ str(i) for i in range(1, 91)]

    while True:
        chunk = SERVER.recv(2048).decode()
        if(chunk in numbers and flashNumberLabel and not gameOver):
            flashNumberList.append(int(chunk))
            canvas2.itemconfigure(flashNumberLabel, text = chunk, font = ('Chalkboard SE', 60))
        elif('wins the game.' in chunk):
            gameOver = True
            canvas2.itemconfigure(flashNumberLabel, text = chunk, font = ('Chalkboard SE', 40))


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()



setup()


#CHANGES MADE
# First recv message from server
# Show the Flash Number
# chnaged marked number button background to green
# check player is win or lose the game
# change game over to True when player lose the game
# show wrong marking
# chnage game over to True when one of the player win the game
