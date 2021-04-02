from collections import defaultdict
from graphviz import *

class DFA: 

	def __init__(self, states, alphabet, transitions, start, accept):
		self.states = states
		self.alphabet = alphabet
		# map from (state, transition letter) -> state
		self.transitions = transitions
		self.start = start
		self.accept = accept
		self.current = start
		self.inverse_trans = defaultdict(list)
		for k, v in self.transitions.items():
			self.inverse_trans[(v, k[1])].append(k[0])

	def next_state(self, letter, current = None):

		if current is None:
			current = self.current

		if (current, letter) in self.transitions:
			return self.transitions[(current, letter)]

		return None


	# determine if accept or reject
	# do not change any values of object
	def simulate(self, string, start = None):

		if start is None:
			start = self.start

		next_state = None
		path = [start]
		curr = start
		for s in string:
			next_state = self.next_state(s, curr)
			if next_state :
				path.append(next_state)
				curr = next_state
			else:
				return (False, path)

		if curr in self.accept:
			return (True, path)
		return (False, path)


	def moore_reduction(self):
		P = [set(self.states) - set(self.accept), set(self.accept)]
		print(P)
		new_P = None
		n = 0
		while new_P != P:
			new_P = P
			for curr_set in new_P:
				for letter in self.alphabet:
					I = set()
					for s in curr_set:
						if (s, letter) in self.inverse_trans:
							for x in self.inverse_trans[(s, letter)]:
								I.add(x)
					# split the classes based on I
					temp_P = []
					for C in P:
						common = C.intersection(I)
						diff = C.difference(I)
						if len(common) > 0 and len(diff) > 0:
							temp_P.append(common)
							temp_P.append(diff)
						else:
							temp_P.append(C)
					P = temp_P

		new_state_names = []
		new_accept = []
		new_start = None

		for new_states in P:
			accept = False
			start = False
			new_state = ""
			for s in new_states:
				if s in self.accept:
					accept = True
				if s == self.start:
					start = True
				new_state += str(s) + ","
			new_state = new_state[:-1]

			if accept:
				new_accept.append(new_state)
			if start:
				new_start = new_state

			new_state_names.append(new_state)

		new_transitions = {}
		for s in new_state_names:
			orig_state = s[0]
			for l in self.alphabet:
				if self.transitions[(orig_state, l)]:
					for poss_dest in new_state_names:
						if str(self.transitions[(orig_state, l)]) in poss_dest:
							new_transitions[(s, l)] = poss_dest

		minimized_DFA = DFA(new_state_names, self.alphabet, new_transitions, new_start, new_accept)
		return minimized_DFA


	# draws the current node green
	# if stopped draws current node red
	# if completed draws current node green
	def get_viz(self, current = None, stopped = False, completed = False):

		g = Digraph()

		if stopped:
			color = 'red'
		else:
			if completed:
				color = 'green'
			else:
				color = 'yellow'


		if current is None or current == self.start:
			start_color = color
			if self.start in self.accept:
				g.node(self.start, shape='doublecircle', color=start_color, style='filled')
			else:
				g.node(self.start, color=start_color, style='filled')

		else:
			if self.start in self.accept:
				g.node(self.start, shape='doublecircle')
			else:
				g.node(self.start)


		for s in self.accept:
			if s != self.start:
				if s == current:
					g.node(s, color = color, shape='doublecircle', style='filled')
				else:
					g.node(s, shape='doublecircle')

		for s in self.states:
			if s not in self.accept and s != self.start:
				if s == current:
					g.node(s, s, color=color, style='filled')
				else:
					g.node(s, s)

		edges = defaultdict(list)
		for k, v in self.transitions.items():
			edges[(k[0], v)].append(k[1])

		for k, v in edges.items():
			label = "  " + ", ".join(v)
			g.edge(k[0],k[1], label)
		
		return g


	def get_svg(self, current = None, stopped = False, completed = False):

		viz = self.get_viz(current, stopped, completed)
		g = viz.unflatten()
		return g.pipe(format='svg').decode('utf-8')



states = ["0", "1", "2", "3", "4", "5", "6"]
alphabet = ["a", "b"]
transitions = {("0", "a"): "1", ("0", "b"): "4", 
				("1", "a"): "5", ("1", "b"): "2", 
				("2", "a"): "0", ("2", "b"): "2", 
				("3", "a"): "6", ("3", "b"): "4", 
				("4", "a"): "2", ("4", "b"): "5", 
				("5", "a"): "5", ("5", "b"): "3", 
				("6", "a"): "5", ("6", "b"): "2"}
start = "0"
accept = ["2"]
dfa = DFA(states, alphabet, transitions, start, accept)



			






