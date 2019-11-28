#!/usr/bin/python

# CS 510: Introduction to Artificial Intelligence
# Homework 1
# Author: Farhan Muhammad
# Date: 10/15/2019
# 
# Implementing Sliding Brick Puzzle
# A sliding brick puzzle is played on a rectangular w by h board (w cells wide and h cells tall).
# Each cell in the board can be either free, have a wall, or be the goal.
# On top of the board (over some of the free cells) there is a set of solid pieces (or bricks) 
# that can be moved around the board. One of the bricks is special (the master brick).
# A move consists of sliding one of the bricks one cell up, down, left or right.
# Notice that bricks collide with either walls or other bricks, so we cannot move a brick 
# on top of another. Bricks can only slide, they cannot rotate nor be flipped.
# To solve the puzzle, we have to find a sequence of moves that allows you to move the master 
# brick on top of the goal. No other pieces are allowed to be placed on top of the goal

import copy
import random
import Queue
import time

#-----------------------------------Part 1A--------------------------------------------------

# Define a class to represent a given state of the game space (arrangement of bricks)
# Class methods:
# loadState - loads an initial game state from an input text file
#             parses the file and generates a 2D matrix to represent the game space
#             stores the width, height, and state of the game
#
# displayState - displays a selected game state
#
# cloneState - clones the state and returns a new state (with non-referenced parameters)
#
# puzzleCompleteCheck - checks if the current state is the solution state
#
# pieceMoveList - returns a list of moves that can be performed with a given brick for a given state
#
# allMoveList - returns a list of all the moves that can be performed for a given state
#
# normalizeState - normalizes a given state to generalize all bricks that are not the master brick
#                  this ensures that two states with identical arrangement, but different brick placements
#                  are not considered different
class State:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gameState = []

    def loadState(self, fileName):
        inputFile = open(fileName, "r")
        for line in inputFile:
            self.gameState.append(line.strip().split(','))
        for i in range(len(self.gameState)-1):
            for j in range(len(self.gameState[i])-1):
                self.gameState[i][j] = int(self.gameState[i][j])
        self.width = self.gameState[0][0]
        self.height = self.gameState[0][1]
        inputFile.close()

    def displayState(self):
        for line in self.gameState:
            print ','.join(map(str, line))

    def cloneState(self):
        return copy.deepcopy(self)

#-----------------------------------Part 1B--------------------------------------------------

    def puzzleCompleteCheck(self):
        for i in range(1,len(self.gameState)):
            for j in range(0,len(self.gameState[i])-1):
                if self.gameState[i][j] == -1:
                    return False
        return True

    def pieceMoveList(self, piece):
        moveList = []
        allUpClear = True
        allDownClear = True
        allLeftClear = True
        allRightClear = True
        if piece < 2:
            print "Invalid piece number"
        else:
            for i in range(2,len(self.gameState)-1):
                if ('u' in moveList) or allUpClear == False:
                    break
                for j in range(1,len(self.gameState[i])-2):
                    if self.gameState[i][j] == piece:
                        while self.gameState[i][j] == piece:
                            if piece == 2 and (self.gameState[i-1][j] == 0 or self.gameState[i-1][j] == -1):
                                j += 1
                                continue
                            elif piece > 2 and self.gameState[i-1][j] == 0:
                                j += 1
                                continue
                            else:
                                allUpClear = False
                                break
                        if allUpClear == True:
                            moveList.append('u')
                        else:
                            break
            i = len(self.gameState)-2
            while i > 1 :
                if ('d' in moveList) or allDownClear == False:
                    break
                for j in range(1,len(self.gameState[i])-2):
                    if self.gameState[i][j] == piece:
                        while self.gameState[i][j] == piece:
                            if piece == 2 and (self.gameState[i+1][j] == 0 or self.gameState[i+1][j] == -1):
                                j += 1
                                continue
                            elif piece > 2 and self.gameState[i+1][j] == 0:
                                j += 1
                                continue
                            else:
                                allDownClear = False
                                break
                        if allDownClear == True:
                            moveList.append('d')
                        else:
                            break
                i -= 1
            for j in range(1,len(self.gameState[1])-2):
                if ('l' in moveList) or allLeftClear == False:
                    break
                for i in range(2,len(self.gameState)-1):
                    if self.gameState[i][j] == piece:
                        while self.gameState[i][j] == piece:
                            if piece == 2 and (self.gameState[i][j-1] == 0 or self.gameState[i][j-1] == -1):
                                i += 1
                                continue
                            elif piece > 2 and self.gameState[i][j-1] == 0:
                                i += 1
                                continue
                            else:
                                allLeftClear = False
                                break
                        if allLeftClear == True:
                            moveList.append('l')
                        else:
                            break
            j = len(self.gameState[1])-3
            while j > 0:
                if ('r' in moveList) or allRightClear == False:
                    break
                for i in range(2,len(self.gameState)-1):
                    if self.gameState[i][j] == piece:
                        while self.gameState[i][j] == piece:
                            if piece == 2 and (self.gameState[i][j+1] == 0 or self.gameState[i][j+1] == -1):
                                i += 1
                                continue
                            elif piece > 2 and self.gameState[i][j+1] == 0:
                                i += 1
                                continue
                            else:
                                allRightClear = False
                                break
                        if allRightClear == True:
                            moveList.append('r')
                        else:
                            break
                j -= 1
            return moveList

    def allMoveList(self):
        pieceTracker = []
        allMoveList = []
        for i in range(2,len(self.gameState)-1):
            for j in range(1,len(self.gameState[i])-2):
                if self.gameState[i][j] == 0:
                    continue
                else:
                    if (self.gameState[i][j] not in pieceTracker):
                        currentPieceMoveList = self.pieceMoveList(self.gameState[i][j])
                        if len(currentPieceMoveList) != 0:
                            pieceTracker.append(self.gameState[i][j])
                            allMoveList.append([self.gameState[i][j], currentPieceMoveList])
        return allMoveList

#-----------------------------------Part 1E--------------------------------------------------

    def normalizeState(self):
        nextIdx = 3
        for i in range(2,len(self.gameState)-1):
            for j in range(1,len(self.gameState[i])-2):
                if self.gameState[i][j] == nextIdx:
                    nextIdx += 1
                elif self.gameState[i][j] > nextIdx:
                    swapIdx(self, nextIdx, self.gameState[i][j])
                    nextIdx += 1
        return self

# Define a class to represent a move in the game:
# Class methods:
# move - define the move given a specific piece and direction
# getPieceNumber - return the brick number
#
# getMoveDirection - return the direction of a given move
class Move:
    def __init__(self, piece, direction):
        self.piece = piece
        self.direction = direction

    def move(self, currentPiece, currentDirection):
        self.piece = currentPiece
        self.direction = currentDirection
        return self

    def getPieceNumber(self):
        return self.piece

    def getMoveDirection(self):
        return self.direction

# Define a funtion to apply a move to an existing game state, resulting in a new state.
# Given a game state and a move class, apply the move to the state.
def applyMove(currentState, nextMove):
    pieceNumber = nextMove.getPieceNumber()
    moveDirection = nextMove.getMoveDirection()
    currentPieceMoveList = currentState.pieceMoveList(pieceNumber)
    if (moveDirection in currentPieceMoveList):
        if moveDirection == 'u':
            for i in range(2,len(currentState.gameState)-1):
                for j in range(1,len(currentState.gameState[i])-2):
                    if currentState.gameState[i][j] == pieceNumber:
                        if currentState.gameState[i-1][j] == -1:
                            currentState.gameState[i-1][j] = 0
                        currentState.gameState[i][j], currentState.gameState[i-1][j] = currentState.gameState[i-1][j], currentState.gameState[i][j]
        elif moveDirection == 'd':
            i = len(currentState.gameState)-2
            while i > 1 :
                for j in range(1,len(currentState.gameState[i])-2):
                    if currentState.gameState[i][j] == pieceNumber:
                        if currentState.gameState[i+1][j] == -1:
                            currentState.gameState[i+1][j] = 0
                        currentState.gameState[i][j], currentState.gameState[i+1][j] = currentState.gameState[i+1][j], currentState.gameState[i][j]
                i -= 1
        elif moveDirection == 'l':
            for i in range(2,len(currentState.gameState)-1):
                for j in range(1,len(currentState.gameState[i])-2):
                    if currentState.gameState[i][j] == pieceNumber:
                        if currentState.gameState[i][j-1] == -1:
                            currentState.gameState[i][j-1] = 0
                        currentState.gameState[i][j], currentState.gameState[i][j-1] = currentState.gameState[i][j-1], currentState.gameState[i][j]
        elif moveDirection == 'r':
            for i in range(2,len(currentState.gameState)-1):
                j = len(currentState.gameState[1])-3
                while j > 0:
                    if currentState.gameState[i][j] == pieceNumber:
                        if currentState.gameState[i][j+1] == -1:
                            currentState.gameState[i][j+1] = 0
                        currentState.gameState[i][j], currentState.gameState[i][j+1] = currentState.gameState[i][j+1], currentState.gameState[i][j]
                    j -= 1
    else:
        print "Move not allowed"
    currentState.normalizeState()
    return currentState

# Implement applyMove but for a cloned game state
def applyMoveCloning(currentState, nextMove):
    newState = currentState.cloneState()
    return applyMove(newState, nextMove)

#-----------------------------------Part 1D--------------------------------------------------

# Compare two states
def compareStates(state1, state2):
    if state1.width == state2.width and state1.height == state2.height:
        for i in range(1,len(state1.gameState)):
            for j in range(len(state1.gameState[i])):
                if state1.gameState[i][j] == state2.gameState[i][j]:
                    continue
                else:
                    return False
    else:
        return False
    return True

#-----------------------------------Part 1E--------------------------------------------------

def swapIdx(state, idx1, idx2):
    for i in range(2,len(state.gameState)-1):
        for j in range(1,len(state.gameState[i])-2):
            if state.gameState[i][j] == idx1:
                state.gameState[i][j] = idx2
            elif state.gameState[i][j] == idx2:
                state.gameState[i][j] = idx1
    return state

#-----------------------------------Part 1F--------------------------------------------------

# Generate a random move for a given state and repeat the process N times
def randomWalks(state, nextMove, N):
    for move in range(N):
        currentPossibleMoves = state.allMoveList()
        pieceIdx = random.randint(0, len(currentPossibleMoves)-1)
        directionIdx = random.randint(0, len(currentPossibleMoves[pieceIdx][1])-1)
        print ("\n(%d,%s)\n" % (currentPossibleMoves[pieceIdx][0], currentPossibleMoves[pieceIdx][1][directionIdx]))
        applyMove(state, nextMove.move(currentPossibleMoves[pieceIdx][0], currentPossibleMoves[pieceIdx][1][directionIdx]))
        state.displayState()
        if state.puzzleCompleteCheck():
            break

#-----------------------------------Part 2---------------------------------------------------

# Define a Node class which will represent each state in the game, store the parent node, move that created
# this node, and depth of node as parameters.
class Node:
    def __init__(self, state):
        self.state = state
        self.parent = 0
        self.move = []
        self.depth = 0

# Implement a breadth-first strategy to solve the puzzle.
# Search for the solution state in a tree in a breadth-first manner.
def bfSolution(state, nextMove):
    rootNode = Node(state)
    bfsQ = Queue.Queue()
    bfsQ.put(rootNode)
    graphTraversed = False
    searchedStates = []
    searchedStates.append(rootNode.state.gameState)
    nodeCount = 0
    while not graphTraversed:
        currentNode = bfsQ.get()
        nodeCount += 1
        if currentNode.state.puzzleCompleteCheck():
            path = [currentNode.move]
            parentNode = currentNode.parent
            while parentNode.move:
                path.append(parentNode.move)
                parentNode = parentNode.parent
            path.reverse()
            for node in path:
                print ("(%d,%s)" % (node[0], node[1]))
            currentNode.state.displayState()
            return len(path), nodeCount
        nextStates = []
        currentPossibleMoves = []
        for move in currentNode.state.allMoveList():
            for direction in move[1]:
                possibleState = applyMoveCloning(currentNode.state, nextMove.move(move[0], direction))
                nextStates.append(possibleState)
                currentPossibleMoves.append([move[0], direction])
        for nextState in nextStates:
            if (nextState.gameState not in searchedStates):
                searchedStates.append(nextState.gameState)
                nextNode = Node(nextState)
                nextNode.parent = currentNode
                nextNode.move = currentPossibleMoves[nextStates.index(nextState)]
                nextNode.depth = nextNode.parent.depth + 1
                bfsQ.put(nextNode)

# Implement a depth-first strategy to solve the puzzle.
# Search for the solution state in a tree in a depth-first manner.
def dfSolution(state, nextMove, searchDepth):
    rootNode = Node(state)
    dfsStack = []
    dfsStack.append(rootNode)
    graphTraversed = False
    searchedStates = []
    searchedStates.append(rootNode.state.gameState)
    lenPath = 0
    nodeCount = 0
    while not graphTraversed and dfsStack:
        currentNode = dfsStack.pop()
        nodeCount += 1
        if currentNode.state.puzzleCompleteCheck():
            path = [currentNode.move]
            parentNode = currentNode.parent
            while parentNode.move:
                path.append(parentNode.move)
                parentNode = parentNode.parent
            path.reverse()
            for node in path:
                print ("(%d,%s)" % (node[0], node[1]))
            currentNode.state.displayState()
            graphTraversed = True
            lenPath = len(path)
            break
        if currentNode.depth < searchDepth:
            nextStates = []
            currentPossibleMoves = []
            for move in currentNode.state.allMoveList():
                for direction in move[1]:
                    possibleState = applyMoveCloning(currentNode.state, nextMove.move(move[0], direction))
                    nextStates.append(possibleState)
                    currentPossibleMoves.append([move[0], direction])
            for nextState in nextStates:
                if (nextState.gameState not in searchedStates):
                    searchedStates.append(nextState.gameState)
                    nextNode = Node(nextState)
                    nextNode.parent = currentNode
                    nextNode.move = currentPossibleMoves[nextStates.index(nextState)]
                    nextNode.depth = nextNode.parent.depth + 1
                    dfsStack.append(nextNode)
    return graphTraversed, lenPath, nodeCount

# Implement an iterative deepening strategy to solve the puzzle.
# Search for the solution state in a tree in an iterative depth-first manner.
def idSolution(state, nextMove):
    puzzleSolved = False
    searchDepth = 0
    lenPath = 0
    nodeCount = 0
    totalNodeCount = 0
    while not puzzleSolved:
        puzzleSolved, lenPath, nodeCount = dfSolution(state, nextMove, searchDepth)
        totalNodeCount += nodeCount
        searchDepth += 1
    return lenPath, totalNodeCount

# Initialize game and move and perform random walk, BFS, DFS, and IDS for level 0, 1, 2, and 3.
# Time each puzzle solution and display the number of nodes visited, time taken, and number of moves.
gameState = State(0, 0)
nextMove = Move(0, 0)

gameState.loadState("SBP-level0.txt")
print "Initial State Level 0:"
gameState.displayState()
print "--------------------------------"

gameStateRandom = gameState.cloneState()
print ""
print "Random Walk Test:"
randomWalks(gameStateRandom, nextMove, 3)
print "--------------------------------"

print ""
print "Breadth-First Strategy:"
startBFS = time.time()
numMovesBFS, numNodesBFS = bfSolution(gameState, nextMove)
stopBFS = time.time()
print ("Number of nodes visited: %d" % numNodesBFS) 
print ("Search time: %.4fs" % (stopBFS-startBFS))
print ("Length of solution: %d" % numMovesBFS)
print "--------------------------------"

print ""
print "Depth-First Strategy:"
startDFS = time.time()
_, numMovesDFS, numNodesDFS = dfSolution(gameState, nextMove, 1000)
stopDFS = time.time()
print ("Number of nodes visited: %d" % numNodesDFS)
print ("Search time: %.4fs" % (stopDFS-startDFS))
print ("Length of solution: %d" % numMovesDFS)
print "--------------------------------"

print ""
print "Iterative Deepening Strategy:"
startIDS = time.time()
numMovesIDS, numNodesIDS = idSolution(gameState, nextMove)
stopIDS = time.time()
print ("Number of nodes visited: %d" % numNodesIDS)
print ("Search time: %.4fs" % (stopIDS-startIDS))
print ("Length of solution: %d" % numMovesIDS)
print "--------------------------------"

print ""
gameState = State(0, 0)
nextMove = Move(0, 0)

gameState.loadState("SBP-level1.txt")
print "Initial State Level 1:"
gameState.displayState()
print "--------------------------------"

gameStateRandom = gameState.cloneState()
print ""
print "Random Walk Test:"
randomWalks(gameStateRandom, nextMove, 3)
print "--------------------------------"

print ""
print "Breadth-First Strategy:"
startBFS = time.time()
numMovesBFS, numNodesBFS = bfSolution(gameState, nextMove)
stopBFS = time.time()
print ("Number of nodes visited: %d" % numNodesBFS)
print ("Search time: %.4fs" % (stopBFS-startBFS))
print ("Length of solution: %d" % numMovesBFS)
print "--------------------------------"

print ""
print "Depth-First Strategy:"
startDFS = time.time()
_, numMovesDFS, numNodesDFS = dfSolution(gameState, nextMove, 1000)
stopDFS = time.time()
print ("Number of nodes visited: %d" % numNodesDFS)
print ("Search time: %.4fs" % (stopDFS-startDFS))
print ("Length of solution: %d" % numMovesDFS)
print "--------------------------------"

print ""
print "Iterative Deepening Strategy:"
startIDS = time.time()
numMovesIDS, numNodesIDS = idSolution(gameState, nextMove)
stopIDS = time.time()
print ("Number of nodes visited: %d" % numNodesIDS)
print ("Search time: %.4fs" % (stopIDS-startIDS))
print ("Length of solution: %d" % numMovesIDS)
print "--------------------------------"

print ""
gameState = State(0, 0)
nextMove = Move(0, 0)

gameState.loadState("SBP-level2.txt")
print "Initial State Level 2:"
gameState.displayState()
print "--------------------------------"

gameStateRandom = gameState.cloneState()
print ""
print "Random Walk Test:"
randomWalks(gameStateRandom, nextMove, 3)
print "--------------------------------"

print ""
print "Breadth-First Strategy:"
startBFS = time.time()
numMovesBFS, numNodesBFS = bfSolution(gameState, nextMove)
stopBFS = time.time()
print ("Number of nodes visited: %d" % numNodesBFS)
print ("Search time: %.4fs" % (stopBFS-startBFS))
print ("Length of solution: %d" % numMovesBFS)
print "--------------------------------"

print ""
print "Depth-First Strategy:"
startDFS = time.time()
_, numMovesDFS, numNodesDFS = dfSolution(gameState, nextMove, 1000)
stopDFS = time.time()
print ("Number of nodes visited: %d" % numNodesDFS)
print ("Search time: %.4fs" % (stopDFS-startDFS))
print ("Length of solution: %d" % numMovesDFS)
print "--------------------------------"

print ""
print "Iterative Deepening Strategy:"
startIDS = time.time()
numMovesIDS, numNodesIDS = idSolution(gameState, nextMove)
stopIDS = time.time()
print ("Number of nodes visited: %d" % numNodesIDS)
print ("Search time: %.4fs" % (stopIDS-startIDS))
print ("Length of solution: %d" % numMovesIDS)
print "--------------------------------"

print ""
gameState = State(0, 0)
nextMove = Move(0, 0)

gameState.loadState("SBP-level3.txt")
print "Initial State Level 3:"
gameState.displayState()
print "--------------------------------"

gameStateRandom = gameState.cloneState()
print ""
print "Random Walk Test:"
randomWalks(gameStateRandom, nextMove, 3)
print "--------------------------------"

print ""
print "Breadth-First Strategy:"
startBFS = time.time()
numMovesBFS, numNodesBFS = bfSolution(gameState, nextMove)
stopBFS = time.time()
print ("Number of nodes visited: %d" % numNodesBFS)
print ("Search time: %.4fs" % (stopBFS-startBFS))
print ("Length of solution: %d" % numMovesBFS)
print "--------------------------------"

print ""
print "Depth-First Strategy:"
startDFS = time.time()
_, numMovesDFS, numNodesDFS = dfSolution(gameState, nextMove, 1000)
stopDFS = time.time()
print ("Number of nodes visited: %d" % numNodesDFS)
print ("Search time: %.4fs" % (stopDFS-startDFS))
print ("Length of solution: %d" % numMovesDFS)
print "--------------------------------"

print ""
print "Iterative Deepening Strategy:"
startIDS = time.time()
numMovesIDS, numNodesIDS = idSolution(gameState, nextMove)
stopIDS = time.time()
print ("Number of nodes visited: %d" % numNodesIDS)
print ("Search time: %.4fs" % (stopIDS-startIDS))
print ("Length of solution: %d" % numMovesIDS)
print "--------------------------------"
