from automata_app import app
from flask import render_template, jsonify, request, url_for, redirect
from graphviz import *
from automata_app.forms import *
from collections import defaultdict

@app.route("/")
@app.route("/home")
def home():
	return render_template('index.html')

@app.route("/dfa/create", methods=["GET", "POST"])
def createDFA():

	form = createDFAForm()

	states = form.states.data
	alphabet = form.alphabet.data
	start_state = form.start_state.data
	accept_states = form.accept_states.data


	if accept_states is None:
		form.accept_states.choices = [("", "")]

	if request.method == "POST":

		g = Digraph()


		dfa_states = states.split(",")
		alphabet = alphabet.split(",")

		print(accept_states)

		if start_state in accept_states:
			g.node(start_state, shape='doublecircle', color='green', style='filled')
		else:
			g.node(start_state, color='green', style='filled')

		for s in accept_states:
			if s != start_state:
				g.node(s, shape='doublecircle')

		for s in dfa_states:
			if s not in accept_states and s != start_state:
				g.node(s, s)

		edges = defaultdict(list)
		for t in form.transitions.data:
			edges[(t["source_state"],t["destination_state"])].append(t["transition"])

		for k, v in edges.items():
			label = "  " + ", ".join(v)
			g.edge(k[0],k[1], label)
				

		g = g.unflatten()

		graph = g.pipe(format='svg').decode('utf-8')

		form.start_state.choices = [(s, s) for s in dfa_states]
		form.accept_states.choices = [(s, s) for s in dfa_states]

		for trans_form in form.transitions:
			trans_form.source_state.choices = [(s, s) for s in dfa_states]
			trans_form.destination_state.choices = [(s, s) for s in dfa_states]
			trans_form.transition.choices = [(a, a) for a in alphabet]

		return render_template('dfa.html', form = form, graph=graph)

	return render_template('dfa.html', form = form)

@app.route("/nfa")
def nfa():
	return render_template('nfa.html')

@app.route("/turingMachine")
def turingMachine():
	return render_template('turingMachine.html')