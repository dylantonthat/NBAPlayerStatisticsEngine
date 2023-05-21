#import data scraping modules + verify the links scraped
from bs4 import BeautifulSoup
import validators

#import GUI modules
import customtkinter
from PIL import Image


#import modules to get and open urls
import requests
import webbrowser
import urllib.request





#GUI ---------------------------------------------------------------------------------------------------------

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #window title + size
        self.title("NBA Player Statistics Engine")
        self.geometry("700x600")
        
        self.minsize(700, 600)
        self.maxsize(700, 600)

        '''
        main window
        '''
        #4 by 5 main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.frame = customtkinter.CTkFrame(master = self,width = 650, height = 600)
        
        #title
        self.header = customtkinter.CTkLabel(master = self, text = "NBA Player Statistics Engine", font = ("Roboto", 24))
        self.header.grid(row = 0, column = 1, columnspan = 2, padx = 25, pady = (10,0), sticky = "news")
        
        #enter input (sticky new)
        self.entry = customtkinter.CTkEntry(master = self, placeholder_text = "Enter Player Name: ")
        self.entry.grid(row = 1, column = 1, rowspan = 2, padx = 20, pady = 5, ipadx = 3, ipady = 3, sticky = "new")
        
        #search button (sticky new)
        self.button = customtkinter.CTkButton(master=self,text="Search", command=self.get_value)
        self.button.grid(row = 1, column = 2, rowspan = 2, padx = 20, pady = 5, ipadx = 3, ipady = 3, sticky = "new")
        
        #player image (sticky ews)
        self.playerImg = customtkinter.CTkImage(Image.open("images/background.png"), size = (200, 250))
        playerImg = customtkinter.CTkLabel(master = self, text = "Player Image Goes Here: ", image = self.playerImg)
        playerImg.grid(row = 2, column = 1, rowspan = 1, columnspan = 2, padx = 10, pady = 5, sticky = "news")
    
        #output textbox (sticky ews)
        self.output = customtkinter.CTkTextbox(master = self, width = 200, height = 100, font = ("Roboto", 13))
        self.output.grid(row = 3, column = 1, rowspan = 2, columnspan = 2, padx = 20, pady = (5,20), ipadx = 10, ipady = 10, sticky = "ews")
        self.output.insert("0.0","Player Data Goes Here:")
        self.output.configure(state = 'disabled')
        
        
        '''
        sidebar
        '''
        self.sidebarFrame = customtkinter.CTkFrame(self, width = 150, corner_radius = 0)
        self.sidebarFrame.grid(row = 0, column = 0, rowspan = 4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        #logo image button (sticky news)
        self.logoImg = customtkinter.CTkImage(Image.open("images/nbaLogo.png"), size = (125, 200))
        logoImg_button = customtkinter.CTkButton(master = self.sidebarFrame, text = " ",image = self.logoImg, command = self.openProjectLink,
                                            fg_color=("black", "lightgray"), hover_color = ("black", "gray"))
        logoImg_button.grid(row = 0, column = 0, rowspan = 3, padx = 20, pady = 10, sticky = "news")
        
        #description textbox (sticky news)
        self.description = customtkinter.CTkTextbox(master = self.sidebarFrame, width = 150, height = 300, font = ("Roboto", 13))
        self.description.insert("0.0", "\nHello! This application" +
                                "\nallows you to input an " +
                                "\nNBA player's full name " +
                                "\n(current or former) in order to retrieve his career" +
                                "\nstatistics." +
                                "\n\nSpecifically, this includes \npoints, rebounds, and" +
                                "\nassists per game played." +
                                "\n\nFor more information in" +
                                "\nregards to the making of" +
                                "\nthis program, click on the " +
                                "\nbutton above.")
        self.description.grid(row = 3, column = 0, rowspan = 2, padx = 20, pady = (10,20), ipadx = 10, sticky = "ews")
        self.description.configure(state="disabled")

        
        
    #obtain user input
    def get_value(self):
        e = self.entry.get()
        self.getData(e)
    
    #when clicking NBA button a link to the project will open in the user's window
    def openProjectLink(self):
        webbrowser.open("https://github.com/dylantonthat/NBAPlayerStatisticsEngine", new = 0, autoraise = True)
        
    #download image from Basketball Reference using urllib
    def retrievePlayerImage(self, imageLink):
        urllib.request.urlretrieve(imageLink, "images/" + playerNameForLink[1][0:5] + playerNameForLink[0][0:2] + ".jpg")
        imgData = requests.get(imageLink).content
        with open("images/" + playerNameForLink[1][0:5] + playerNameForLink[0][0:2] + ".jpg", 'wb') as handler:
            handler.write(imgData)
        
        
        
        
        
        
    #Data Scraping ---------------------------------------------------------------------------------------------------------
    '''
    This section contains all of the methods used to read the user's input and return the necessary information
    (image + stats, or invalid player name)
    '''
    
    
    #user input -------------------------------------------------------------------------------------------
    def userInput(self, n):
        global p, playerNameForLink, pWithoutHyphen, hyphenIndex, pWithoutApostrophe, apostropheIndex
        p = n.lower()
        hyphenIndex = p.find("-") #for printing statement
        apostropheIndex = p.find("'") #for printing statement

        
        if "-" in p:
            pWithoutHyphen = p.replace("-", "")
            playerNameForLink = pWithoutHyphen.split(" ")
            
        if "'" in p:
            pWithoutApostrophe = p.replace("'", "")
            playerNameForLink = pWithoutApostrophe.split(" ")
            
        else:
            playerNameForLink = p.split(" ") #splits input into a list of elements separated by spaces
        
    
    #validate the link (because input might not be formatted correctly)
    def validateInput(self, infoLink, pN):
        validation = validators.url(infoLink, public = True)
        if not validation:
            return False
        elif len(pN) != 2:
            return False
        
        return True
                
        
        
        
        
    #obtain player data from Basketball Reference using BeautifulSoup
    def scrapWebsite(self, infoLink):
        spaceIndex = p.find(" ") #for printing statement
        ref = requests.get(infoLink)
        
        #BeautifulSoup allows us to access stats link as an html document and is therefore able to read in its data
        soup = BeautifulSoup(ref.content, 'html.parser')
        
        #access html part of link, then to the body to access stat
        html = list(soup.children)[3]
        body = list(html.children)[3]
        
        #player's stats are located in the div class p1
        stats = body.find('div', class_ = "p1")
        playerStats = stats.find_all('p')
        
        playerPoints = playerStats[3].get_text()
        playerRebounds = playerStats[5].get_text()
        playerAssists = playerStats[7].get_text()
    
    
    
        self.output.configure(state='normal')
        self.output.delete("0.0", "end")
        
        #if hyphen or single apostrophe
        if (hyphenIndex > 0): #hyphen
            if (hyphenIndex < spaceIndex): #ex. Karl-Anthony Towns
                self.output.insert("0.0", p[:hyphenIndex].capitalize() + "-" + p[hyphenIndex + 1:spaceIndex].capitalize() + " " + p[spaceIndex + 1:].capitalize() + " averages/ed:  \n\n" +
                           "{} points \n{} rebounds \n{} assists \nper game for his career."
                           .format(playerPoints, playerRebounds, playerAssists))
            elif (hyphenIndex > spaceIndex): #ex. Kentavious Caldwell-Pope
                self.output.insert("0.0", p[:spaceIndex].capitalize() + " " + p[spaceIndex + 1:hyphenIndex].capitalize() + "-" + p[hyphenIndex + 1:].capitalize() + " averages/ed:  \n\n" +
                           "{} points \n{} rebounds \n{} assists \nper game for his career."
                           .format(playerPoints, playerRebounds, playerAssists))
        
        elif (apostropheIndex > 0): #apostrophe
            if (apostropheIndex < spaceIndex): #ex. no clue
                self.output.insert("0.0", p[:apostropheIndex].capitalize() + "'" + p[apostropheIndex + 1:spaceIndex].capitalize() + p[spaceIndex + 1:].capitalize() + " averages/ed:  \n\n" +
                           "{} points \n{} rebounds \n{} assists \nper game for his career."
                           .format(playerPoints, playerRebounds, playerAssists))
            elif (apostropheIndex > spaceIndex): #ex. Shaquille O'Neal
                self.output.insert("0.0", p[:spaceIndex].capitalize() + " " + p[spaceIndex + 1:apostropheIndex].capitalize() + "'" + p[apostropheIndex + 1:].capitalize() + " averages/ed:  \n\n" +
                           "{} points \n{} rebounds \n{} assists \nper game for his career."
                           .format(playerPoints, playerRebounds, playerAssists))
                
        else:
            self.output.insert("0.0", p[:spaceIndex].capitalize() + " " + p[spaceIndex + 1:].capitalize() + " averages/ed:  \n\n" +
                           "{} points \n{} rebounds \n{} assists \nper game for his career."
                           .format(playerPoints, playerRebounds, playerAssists))
            
        
        self.output.configure(state = 'disabled')
        
        
        self.playerImg = customtkinter.CTkImage(Image.open("images/" + playerNameForLink[1][0:5] + playerNameForLink[0][0:2] + ".jpg"), size = (200, 250))
        playerImg = customtkinter.CTkLabel(master = self, text = " ", image = self.playerImg)
        playerImg.grid(row = 2, column = 1, rowspan = 1, columnspan = 2, padx = 10, pady = 5, sticky = "news")
        
        
    # running all methods
    def getData(self, e):
        self.userInput(e)
        try:
            #first letter of second word, first five letters of second word, and first two letters of first name based on user input
            #Example: Kobe Bryant --> /{b}/{bryanko}01.html
            playerLink = "https://www.basketball-reference.com/players/{}/{}01.html".format(playerNameForLink[1][0], playerNameForLink[1][0:5] + playerNameForLink[0][0:2])
            playerImageLink ="https://www.basketball-reference.com/req/202106291/images/headshots/{}01.jpg".format(playerNameForLink[1][0:5] + playerNameForLink[0][0:2])
            
            
            if self.validateInput(playerLink, playerNameForLink):
                pass
                #BeautifulSoup retrieves/displays data ----------------------------------------------------------------------------------------
                self.retrievePlayerImage(playerImageLink)
                self.scrapWebsite(playerLink)
                
            else:
                self.output.configure(state = "normal")
                self.output.delete("0.0", "end")
                self.output.insert("0.0","Invalid Name")
                self.output.configure(state = "disabled")
            
            
            

            #self.output.configure(state="disabled")

        
        except IndexError or self.validateInput(playerLink, playerNameForLink) == False:
            #blank textbox again
            self.output.configure(state = "normal")
            self.output.delete("0.0", "end")
            self.output.insert("0.0","Invalid Name")
            self.output.configure(state = "disabled")
            
            #blank image again
            self.playerImg = customtkinter.CTkImage(Image.open("images/background.png"), size = (200, 250))
            playerImg = customtkinter.CTkLabel(master = self, text = "Player Image:", image = self.playerImg)
            playerImg.grid(row = 2, column = 1, rowspan = 1, columnspan = 2, padx = 10, pady = 5, sticky = "news")






if __name__ == "__main__":
    app = App()
    app.mainloop()