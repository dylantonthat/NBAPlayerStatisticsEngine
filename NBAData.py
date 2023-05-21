import requests
from bs4 import BeautifulSoup

import validators


def getData():
    
    userInput()
    try:
        #first letter of second word, first five letters of second word, and first two letters of first name based on user input
        #Example: Kobe Bryant --> /{b}/{bryanko}01.html
        infoLink = "https://www.basketball-reference.com/players/{}/{}01.html".format(playerName[1][0], playerName[1][0:5] + playerName[0][0:2])
        
        
        #first five letters of second word, and first two letters of first name based on user input
        #for player Image
        picLink = "https://www.basketball-reference.com/req/202106291/images/headshots/{}01.jpg".format(playerName[1][0:5] + playerName[0][0:2])
        
        if validateLink(playerName, infoLink):
            None
        # data scraping ----------------------------------------------------------------------------------------
        scrapWebsite(infoLink)
        
    except IndexError or validateLink(playerName, infoLink) == False or (len(playerName) < 2 or len(playerName[0]) < 5 or len(playerName[1] < 5)):
        print("Invalid name.")
     
# user input -------------------------------------------------------------------------------------------
def userInput():
    global n, p, playerName
    
    n = input('Enter an NBA Players Full Name!')
    p = n.lower()
    playerName = p.split(" ") # splits input into a list of elements separated by spaces
    
# validate the link (because input might not be formatted correctly)
def validateLink(pN, l):
    validation = validators.url(l, public = True)
    if (not validation):
        return False
    
    return True
        
# retreive player data from Basketball Reference using BeautifulSoup
def scrapWebsite(l):
    
    spaceIndex = p.index(" ") # for printing statement
    ref = requests.get(l)
        
    #BeautifulSoup allows us to access stats link as an html document and is therefore able to read in its data
    soup = BeautifulSoup(ref.content, 'html.parser')
        
    #access html part of link, then to the body to access stat
    html = list(soup.children)[3]
    body = list(html.children)[3]
        
    #player's stats are located in the div class p1
    stats = body.find('div', class_="p1")
    playerStats = stats.find_all('p')
        
    playerPoints = playerStats[3].get_text()
    playerRebounds = playerStats[5].get_text()
    playerAssists = playerStats[7].get_text()
    
        
    print(n[:spaceIndex].capitalize() + " " + n[spaceIndex + 1:].capitalize() + " averages/ed " + "{} points, {} rebounds, and {} assists a game for his career.".format(playerPoints, playerRebounds, playerAssists))

  
if __name__ == "__main__":
    getData()



    






