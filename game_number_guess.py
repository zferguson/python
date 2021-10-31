# game to guess number between minNum and maxNum

# import
import random as rd

# introduciton and set variables
minNum = 1
maxNum = 100

hiddenNumber = rd.randint(minNum,maxNum)

print("Let's play a number guessing game!\n")

userGuess = 0
triesLeft = int(input("How many guesses would you like? "))

# game loop
while userGuess != hiddenNumber:
	userGuess = int(input("\nGuess a number between {0} and {1}: ".format(minNum,maxNum)))
	if triesLeft > 0:
		if userGuess > hiddenNumber:
			triesLeft -= 1
			print("\nToo high, you have {0} tries left!".format(triesLeft))
		elif userGuess < hiddenNumber:
			triesLeft -= 1
			print("\nToo low, you have {0} tries left!".format(triesLeft))
		else:
			print("\nThat's right!")
	else:
		print("\nNo more tries, sorry! The answer was {0}.".format(hiddenNumber))
		break
	