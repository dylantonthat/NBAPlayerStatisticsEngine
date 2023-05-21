def validateInput(self):
        global playerLink, playerImageLink
        playerLink = "https://www.basketball-reference.com/players/{}/{}01.html".format(playerNameForLink[1][0], playerNameForLink[1][0:5] + playerNameForLink[0][0:2])
        validation = validators.url(playerLink)
        
        if not validation:
            return False
        
        playerImageLink ="https://www.basketball-reference.com/req/202106291/images/headshots/{}01.jpg".format(playerNameForLink[1][0:5] + playerNameForLink[0][0:2])
        return True
                