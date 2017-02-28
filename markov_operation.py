#encoding:utf-8

from markov import Markov
from threading import Thread

markov = Markov()

def trainMarkov():
	while True:
		markov.train()
		markov.save()

trainMarkovThread = Thread(target=trainMarkov)

while True:
	command = input()
	if command == "train":
		print("start to tain markov mold")
		trainMarkovThread.start()

	elif command == "q":
		print("hidden progress tips")
		markov.show_progress = False

	elif command == "show":
		print("display progress tips")
		markov.show_progress = True

	elif command == "display":
		print("display all matrix and sum of all matrix each row")
		markov.display()

	elif command == "compare":
		print("compare all matrix beteewn two iterations")
		markov.compare()

	elif command.startswith("cut "):
		command = command.replace("cut ","")
		print("cut result:")
		markov.cut(command)

	elif command == "exit":
		print("exit from program")
		break