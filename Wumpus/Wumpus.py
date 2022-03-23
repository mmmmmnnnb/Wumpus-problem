import clyngor
import os


#Author Tianyu Jin

#the class of agent
class KBAgent:
    def makechoice(self):
        #get current working directory
        CWD = os.getcwd()

        #different kind od options
        newsafe = set()
        newrisky = set()
        oldsafe = set()
        
        #get the possible moving option
        movementanswers = clyngor.solve(CWD + r'\WumpusWorldPossibleMoving.gr')
        for answer in movementanswers:
            for term in answer:
                print(term)
                it = iter(term)
                next(it)
                args = next(it)
                if args[2] == 'old':
                    oldsafe.add(term)
                elif args[3] == 'risky':
                    newrisky.add(term)
                elif args[3] == 'safe':
                    newsafe.add(term)
        
        #make decision
        if len(newsafe) != 0:
            choice = newsafe.pop()
            return choice
        elif len(newrisky) != 0:
            choice = newrisky.pop()
            return choice
        elif len(oldsafe) != 0:
            choice = oldsafe.pop()
            return choice

    def savePosition(self):
        #get current working directory
        CWD = os.getcwd()
        
        
        #Current State file
        CSf = open(CWD+r'\WumpusWorldCurrentState.gr', "r")
        positionStr = CSf.read()
        oldStr = "old(" + positionStr[16] + "," + positionStr[18] + ")." + "\r"
        #Position History file
        Hf = open(CWD + r'\WumpusWorldHistory.gr', "a")
        Hf.write(oldStr)
        Hf.close()

        #get the current percept
        perceptanswers = clyngor.solve(CWD + r'\WumpusWorldCurrentPercept.gr')
        for answer in perceptanswers:
            for term in answer:
                
                it = iter(term)
                pred = next(it)
                args = next(it)
                perceptStr = pred + str(args) + "." + "\r"
                #percept history file
                PHf = open(CWD + r'\WumpusWorldPerceptHistory.gr', "a")
                PHf.write(perceptStr)
                PHf.close()

        return positionStr







agent = KBAgent()
#get current working directory
CWD = os.getcwd()

currentPositionStr = agent.savePosition()
print("Wumpus World: Game Started, " + currentPositionStr)

terminate = False
while not terminate:

    #show the percept first
    currentPerceptAnswers = clyngor.solve(CWD + r'\WumpusWorldCurrentPercept.gr')
    for answer in currentPerceptAnswers:
        for term in answer:
            print(term)

    #prepare a string to show information of the screen

    systemStr = "Wumpus World: "
    termination = clyngor.solve(CWD + r'\WumpusWorldTermination.gr')
    for answer in termination:
        for term in answer:
            #when there is a term in the answer, it terminates.
            terminate = True
            it = iter(term)
            pred = next(it)
            args = next(it)
            if args[0] == 'gold':
                systemStr += "Find Gold, Congratulations! "
            elif args[0] == 'pit':
                systemStr += "Fall in a Pit, Sorry. "
            elif args[0] == 'wumpus':
                systemStr += "Eat by Wumpus, Sorry. "
    
    if terminate:
        #when terminate, print how it terminate, and delete all the history
        systemStr += currentPositionStr
        print(systemStr)
        PHf = open(CWD + r'\WumpusWorldPerceptHistory.gr', "w")
        PHf.write("")
        PHf.close()
        Hf = open(CWD + r'\WumpusWorldHistory.gr', "w")
        Hf.write("")
        Hf.close()
        CSf = open(CWD + r'\WumpusWorldCurrentState.gr', "w")
        CSf.write("currentposition(1,1).")
        CSf.close()

    else:
        #while not terminate let the agent make choice, and do the hostory recording, change the position.
        currentPositionStr = agent.savePosition()
        systemStr += "Moved, "
        choice = agent.makechoice()
        it = iter(choice)
        pred = next(it)
        args = next(it)
        currentPositionStr = "currentposition("+ str(args[0]) +","+ str(args[1]) +")."
        CSf = open(CWD + r'\WumpusWorldCurrentState.gr', "w")
        CSf.write(currentPositionStr)
        CSf.close()
        
        systemStr += currentPositionStr
        print(systemStr)
        print("Continue?")




    
