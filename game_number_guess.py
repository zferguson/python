import random

minNum = 1
maxNum = 100

hiddenNumber = random.randint(minNum,maxNum)

print("Let's play a number guessing game!\n")

userGuess = 0
triesLeft = int(input("How many guesses would you like? "))

while userGuess != hiddenNumber:
	userGuess = int(input("\nGuess a number between {0} and {1}: ".format(minNum,maxNum)))
	if triesLeft > 1:
		if userGuess > hiddenNumber:
			triesLeft -= 1
			#print()
			print("\nToo high, you have {0} tries left!".format(triesLeft))
		elif userGuess < hiddenNumber:
			triesLeft -= 1
			#print()
			print("\nToo low, you have {0} tries left!".format(triesLeft))
		else:
			#print()
			print("\nThat's right!")
	else:
		print()
		print("No more tries, sorry! The answer was {0}.".format(hiddenNumber))
		break
	