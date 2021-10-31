import random

minNum = 1
maxNum = 100

hiddenNumber = random.randint(minNum,maxNum)

userGuess = 0
triesLeft = 5

while userGuess != hiddenNumber:
	userGuess = int(input("Guess a number between {0} and {1}: ".format(minNum,maxNum)))
	if triesLeft > 1:
		if userGuess > hiddenNumber:
			triesLeft -= 1
			print()
			print("Too high, you have {0} tries left!".format(triesLeft))
		elif userGuess < hiddenNumber:
			triesLeft -= 1
			print()
			print("Too low, you have {0} tries left!".format(triesLeft))
		else:
			print()
			print("That's right!")
	else:
		print()
		print("No more tries, sorry! The answer was {0}.".format(hiddenNumber))
		break