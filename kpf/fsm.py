class StateNotDefined(Exception):
	def __init__(self,fsm,state):
		super(StateNotDefined,self).__init__("State {!r} not defined for state machine {!r}".format(state,fsm))

class FiniteStateMachine:
	def __init__(self,state="begin"):
		self.state = state
	def input(self,*args,**kwargs):
		if not hasattr(self,"do_"+self.state): raise StateNotDefined(self.__class__,self.state)
		return getattr(self,"do_"+self.state)(*args,**kwargs)
	def change(self,new):
		self.state = new
