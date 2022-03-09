from antlr4 import *
import antlr4
from resultLexer import *
from resultParser import *
from resultListener import *
from ast import *
import re

result_Collection = ResultCollection()
	
class Interpreter(resultListener):
	def field_to_tuple(self,field,regex):
		f = ''.join(field)
		f = re.sub(regex,"",f)
		if f != '':
			f = f.split(',')
		else:
			f = []
		new_f = []
		for x in f:
			aux = x.split('->')
			aux[0] = aux[0].replace(' ','')	
			aux[1] = aux[1].replace(' ','')
			new_f.append((aux[0] , aux[1]))
		f = new_f
		return f

	def field_to_triple(self,field,regex):
		f = ''.join(field)
		f = re.sub(regex,"",f)
		if f != '':
			f = f.split(',')
		else:
			f = []
		new_f = []
		for x in f:
			aux = x.split('->')
			aux[0] = aux[0].replace(' ','')	
			aux[1] = aux[1].replace(' ','')
			aux[2] = aux[2].replace(' ','')	
			new_f.append((aux[0] , aux[1], aux[2]))
		f = new_f
		return f

	def ext_sig(self,s):
		new_s = re.sub(r"this/","",s)
		new_s = re.sub(r"={.*}","",new_s)
		return new_s

	def search_value(self,v_id,st_txt):
		fl = filter(lambda x: v_id in x, st_txt)
		fl = filter(lambda x: 'univ' not in x, fl)
		fl = filter(lambda x: 'this/Message' not in x, fl)
		fl = filter(lambda x: 'this/Value' not in x, fl)
		rl = map(lambda x : self.ext_sig(x),fl)
		return rl

	def search_topic(self,t_id,st_txt):
		fl = filter(lambda x: t_id in x, st_txt)
		fl = filter(lambda x: 'univ' not in x, fl)
		fl = filter(lambda x: 'this/Message' not in x, fl)
		fl = filter(lambda x: 'this/Topic' not in x, fl)
		rl = map(lambda x : self.ext_sig(x),fl)
		return rl

	def transform_values(self,values,lines):
		new_values = []
		for v in values:
			m_id = v[0]
			aux = v[1].split('$')
			f_id = aux[0]
			v_id = v[2]

			abs_l = self.search_value(v_id,lines)
			new_values.append((m_id,f_id,abs_l))


		return new_values

	def transform_topics(self,topics,lines):
		new_topics = []
		for t in topics:
			m_id = t[0]
			t_id = t[1]
			abs_l = self.search_topic(t_id,lines)
			new_topics.append((m_id,abs_l[2]))

		return new_topics

	def state_from_description(self,txt):
		lines = txt.split('\n')	
		inbox = self.field_to_tuple(filter(lambda x: 'this/Node<:inbox' in x,lines),
						"(this/Node<:inbox={)|}")
		outbox = self.field_to_tuple(filter(lambda x: 'this/Node<:outbox' in x,lines),
						"(this/Node<:outbox={)|}")	
		# Values
		values = self.field_to_triple(filter(lambda x: 'this/Message<:value' in x,lines),
						"(this/Message<:value={)|}")
		values = self.transform_values(values,lines)

		# Topics

		topics = self.field_to_tuple(filter(lambda x: 'this/Message<:topic' in x,lines),
						"(this/Message<:topic={)|}")

		topics = self.transform_topics(topics,lines)

		state_obj = State(inbox=inbox,outbox=outbox,values=values,topics=topics)
		return state_obj

	def exitCommand(self, ctx):
	 	name_rule = ctx.name()
	 	name = str(name_rule.NAME()) 			
	 	t = str(name_rule.TYPE())				
	 	scopes = re.findall(r'\d+',str(name_rule.SCOPE())) 
	 	time_scope = scopes[1]
	 	value_scope = scopes[3]
	 	message_scope = scopes[4]
	 	scope_obj = Scope(value_scope,message_scope,time_scope)
	 	result_obj = None
	 	result_rule = None
	 	if ctx.result().unsat() is not None:	
	 		result_rule = ctx.result().unsat()
	 		result_obj = UnsatResult(t,name,scope_obj)
	 	else:									
	 		results_txt = []
	 		states = []							
	 		result_rule = ctx.result().sat()
	 		result_description = result_rule.sts()
	 		while(result_description is not None):
	 			description = str(result_description.st().descriptions().FIELDESCRIPTION())
	 			state_obj = self.state_from_description(description)
	 			states.append(state_obj)			
	 			result_description = result_description.sts()		
	 		instance_obj = Instance(states)
	 		result_obj = SatResult(t,name,scope_obj,instance_obj)

	 	result_Collection.add(result_obj)				

class Parser():
	def __init__(self,f):
		self.file_name = f
	def parse(self):
		with open(self.file_name) as f:
			data = f.read()

		inputStream = antlr4.InputStream(data)
		lexer = resultLexer(inputStream)
		stream = antlr4.CommonTokenStream(lexer)
		parser = resultParser(stream)
		tree = parser.gr()
		interpreter = Interpreter()
		walker = ParseTreeWalker()
		walker.walk(interpreter,tree)
		return result_Collection
