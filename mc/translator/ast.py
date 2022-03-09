import re

class ResultCollection():
	def __init__(self):
		self.results = dict()
	def add(self,result_obj):
		self.results.update({result_obj.property_name:result_obj})
	def getSAT(self):
		result = dict()
		for k in self.results.keys():
			so = self.results.get(k)
			if isinstance(so,SatResult):
				result.update({k:so})
		return result

class ResultObject():
	def __init__(self):
		pass

class UnsatResult(ResultObject):
	def __init__(self,t,property_name,scope):
		self.property_type = t
		self.property_name = property_name
		self.scope = scope

class SatResult(ResultObject):
	def __init__(self,t,property_name,scope,instance_obj):
		self.property_type = t
		self.property_name = property_name
		self.scope = scope 					#Scope Object
		self.result = instance_obj			#Instance()

class Scope():
	def __init__(self,value,message,time):
		self.value_scope = value
		self.message_scope = message
		self.time_scope = time

class Instance():
	def __init__(self,states):
		self.states = states	#[State]	
		# self.values and self.topics should be placed here.s
class Field():
	def __init__(self,field_name,values):
		self.field_name = field_name
		self.values = values
	
	def __str__(self):
		return self.field_name

class State():
	def __init__(self,inbox=[],outbox=[],values=[],topics=[]):
		self.values = dict()	# dict{Message_id : [Field]} 	
		self.topics = dict()	# dict{Message_id : topic_name}
		self.inbox = dict()		# dict{Node_signature: [Message_id]}
		self.outbox = dict()	# dict{Node_signature: [Message_id]}	
		self.set_values(values)
		self.set_topics(topics)		
		self.set_state(inbox,outbox)

	def remove_id(self,s):
		return re.sub(r"\$[0-9]+","",s)
	
	def set_values(self,values):
		for v in values:
			message_id = v[0]
			new_field = Field(v[1],v[2])
			fields = [new_field]
			if message_id in self.values.keys():
				fields = self.values.get(message_id)
				fields.append(new_field)
			self.values.update({message_id:fields})

	def set_topics(self,topics):
		for t in topics:
			message_id = t[0]
			topic_name = t[1]
			self.topics.update({message_id:topic_name})

	def set_state(self,inbox,outbox):
		inbox_d = dict()
		outbox_d = dict()
		# Update inbox dictionary
		for v in inbox:
			node_name = self.remove_id(v[0])
			node_name = node_name.strip()
			message_id = v[1]
			if node_name in inbox_d.keys():
				ml = inbox_d.get(node_name)
				ml.append(message_id)
				inbox_d.update({node_name: ml})
			else:
				inbox_d.update({node_name: [message_id]})
		self.inbox = inbox_d
		# Update outbox dictionary
		for v in outbox:
			node_name = self.remove_id(v[0])
			message_id = v[1]
			if node_name in outbox_d.keys():
				ml = outbox_d.get(node_name)
				ml.append(message_id)
				outbox_d.update({node_name: ml})
			else:
				outbox_d.update({node_name: [message_id]})
		self.outbox = outbox_d