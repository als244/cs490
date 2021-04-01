from automata_app import app
from flask import render_template, jsonify, request, url_for, redirect
from automata_app.forms import *
from collections import defaultdict
from automata_app.DFA import *


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


		dfa_states = states.split(",")
		alphabet = alphabet.split(",")

		transitions = {}
		for t in form.transitions.data:
			transitions[(t["source_state"],t["transition"])] = t["destination_state"]

		dfa = DFA(dfa_states, alphabet, transitions, start_state, accept_states)
		
		graph = dfa.get_svg()


		# fill form back out
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