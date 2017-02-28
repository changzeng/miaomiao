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
		trainMarkovThread.start()

	elif command == "q":
		markov.show_progress = False

	elif command == "show":
		markov.show_progress = True

	elif command == "display":
		markov.display()

	elif command == "compare":
		markov.compare()