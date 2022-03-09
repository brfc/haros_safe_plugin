import os
from configuration import *
import yaml
import intervals as I
from .translator.result import *
from .translator.ast import *

##########################################
####### Result-Configuration Linker ######
##########################################
class Linker(object):
	def __init__(self,configuration, resultObject):
		self.configuration = configuration
		self.result = resultObject
	def issue_header(self,prop_name):
		prop_name = prop_name.strip()
		hpl_prop = self.configuration.hpl_map.get(str(prop_name))
		prop_spec = hpl_prop.__str__()
		header = "<h4> Property '" + prop_spec + "' broken. </h4>"
		return header
	# Node_Signature -> String
	def real_name(self,n):
		nodes = self.configuration.nodes
		for k in nodes.keys():
			node_obj = nodes.get(k)
			if (node_obj.signature).strip() == n.strip():
				return (node_obj.rosname) 
		return "NODE NAME NOT FOUND"
	# Message x dict(Message_id: [Field]) -> String
	def real_value(self,m,values):
		values = values.get(m)	#[Field]
		fd = self.configuration.field
		conditions = []
		for f in values:
			# Getting the field.
			fo = None
			fn = (f.field_name).strip()
			for v in fd.values():
				if (v.abstract() == fn):
					fo = v
					break		
			field_real_name = fo.token	# Field Name
			op, real_value = self.configuration.values_concretization(f.values)
			if not isinstance(real_value, float):
				real_value = str(real_value.lower) + " to " + str(real_value.upper)
			condition = str(field_real_name) + " " + str(op) + " " + str(real_value)
			conditions.append(condition)
		result = ', '.join(conditions)
		return result
	# Message x dict(Message_id: Abstract_topic_name) -> String
	def real_topic(self,m,topics):
		t = topics.get(m)
		topics = self.configuration.topics
		for k in topics.keys():
			topic_obj = topics.get(k)
			if (topic_obj.signature).strip() == t.strip():
				return (topic_obj.rosname)
		return "TOPIC NAME NOT FOUND"
	# Node_Signature x State x State -> [Message_id]
	def receive(self,n,p,a):
		rm = [] 
		pm = (p.inbox).get(n)
		am = (a.inbox).get(n)
		am = [] if am is None else am
		pm = [] if pm is None else pm
		for m in am:
			if m not in pm:
				rm.append(m)
		return rm
	# Node_Signature x State x State -> [Message_id]
	def sends(self,n,p,a):
		sm = []
		pm = (p.outbox).get(n)
		am = (a.outbox).get(n)
		am = [] if am is None else am
		pm = [] if pm is None else pm
		for m in am:
			if m not in pm:
				sm.append(m)
		return sm
	# Node_Signature x [Message_id] x [Message_id] ... -> HTML
	def to_items(self,n,rl,sl,topics,values):
		html = ""
		node = self.real_name(n)
		for m in sl:
			topic = self.real_topic(m,topics) 
			value = self.real_value(m,values)
			html += "<li>" + "The " + node + " sends { " + value + " } through the " + topic + " topic. " + "</li>"
		for m in rl:
			topic = self.real_topic(m,topics)
			value = self.real_value(m,values)
			html += "<li>" + "The " + node + " receives { " + value + " } through the " + topic + " topic." + "</li>"
		return html
	# State x State -> HTML
	def events_html(self,p,a):
		topics = p.topics
		values = p.values
		html = ""
		nodes_dict = self.configuration.nodes
		nodes = nodes_dict.keys()
		nodes_sigs = map(lambda x: ((self.configuration.nodes).get(x)).signature, nodes)
		for n in nodes_sigs:
			n = n.strip() #=
			rm = self.receive(n,p,a)
			sm = self.sends(n,p,a)
			html += self.to_items(n,rm,sm,topics,values)
		return html
	# Instance -> HTML
	def trace_html(self,instance): 
		html = "<ol>"
		states = instance.states
		for i in range(1,len(states)):
			p = states[i-1]
			a = states[i]
			html += self.events_html(p,a)
		# Closing Loop
		p = states[len(states)-1]
		a = states[0]
		html += self.events_html(p,a)
		html += "</ol>"
		return html
	# SatResult -> HTML
	def generate_issue(self,r):
		html = "<br>"
		html += self.issue_header(r.property_name)
		html += "<p> <strong> Counter-example trace: </strong> </p>"
		html += self.trace_html(r.result)
		return html
	# Void -> [HTML]
	def html(self):
		rl = []
		sdict = self.result.getSAT()
		sl = sdict.values()
		for v in sl:
			rl.append(self.generate_issue(v))
		return rl



############################################
############### Analyzer ###################
############################################
class Analyzer(object):
	def __init__(self, c_name, nodes, topics, properties=None):
		module_name = "module " + str(c_name) + "\n\n"
		meta_model, scopes = self.load_configuration()
		self.configuration = Configuration(c_name, nodes, topics,scopes, properties=properties)
		self.specification = (module_name + meta_model + self.configuration.specification())
	def run_dir(self):
		d = os.getcwd()
		return d 
		
	def load_configuration(self):
		scopes = None
		meta_model = None
		with open("/.plugin_mc/plugin.yaml") as f:
			data = f.read()
			l = yaml.load(data)
			scopes = l['scope']
		with open("/.plugin_mc/meta.ele") as f:
			meta_model = f.read()
		return meta_model, scopes

	def model_check(self):
		try:
			with open('/.plugin_mc/model.ele', 'w' ) as f:
				f.write(self.specification)
		except Exception as error:
			print(error)
			return None			
		cmd = "java -cp /.plugin_mc/electrum_pi.jar edu.mit.csail.sdg.alloy4whole.PluginInterface /.plugin_mc/model.ele"
		os.system(cmd)	# Executing Electrum Call
		d = self.run_dir() + "/results.txt"
		parser = Parser(d)
		result = parser.parse()
		linker = Linker(self.configuration, result)
		rl = linker.html()
		return rl
