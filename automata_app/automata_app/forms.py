from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from random import *


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class DFAStateTransitionForm(FlaskForm):
	source_state = SelectField("Source State", choices=[("", "")])
	# multiple select for NFA
	destination_state = SelectField("Destination State", choices = [("", "")])
	transition = SelectField("Transition Label", choices = [("", "")])

	

class createDFAForm(FlaskForm):

	states = StringField("States", validators=[DataRequired()])

	alphabet = StringField("Alphabet", validators=[DataRequired()])

	start_state = SelectField("Start State", choices = [("", "")])

	accept_states = MultiCheckboxField('Accept States')

	# will be 
	transitions =  FieldList(FormField(DFAStateTransitionForm), min_entries=1)

	submit = SubmitField("Create DFA")