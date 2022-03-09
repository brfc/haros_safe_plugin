import intervals as I

####################################################
############ SPECIFICATION EXTRACTION ##############
####################################################
class Field(object):
    def __init__(self,token,t,topic_type):
        self.token = token
        self.type = t
        self.topic_type = topic_type
        self.field_code = str(token) + str(topic_type)
    def abstract(self):
        signature = self.field_code.replace('.','_')
        signature = signature.replace('[','_')
        signature = signature.replace(']','_')
        signature = signature.replace('/','_')
        return signature
    def declaration(self):
        s = "one sig " + self.abstract() + " extends Field{}\n\n"
        t = ""
        if self.topic_type != -1:
            if self.type in [1,3,4]:
                t = "numeric"
            else:
                t = "string"
            s += "fact " + self.abstract() + "_type" + "{\n"
            s += "\t" + self.abstract() +".(Message.value) in " + t + "\n}\n\n"
        return s
        
class Condition(object):
    def __init__(self,ft, op, v):
        self.lhs = ft
        self.operator = op
        self.rhs = v # value or [value]

    def check_alias(self,m,v):
        if v == -1:
            alias = "m0" if m=="m1" else "m1"
            rt = self.lhs.abstract() + ".(" +alias+".value)"
            return rt  
        else:
            return v

    def specification(self,m,alias=False,negated=False):
        if isinstance(self.rhs,list):
            rt = ""
            sl = []
            for v in self.rhs:
                v = self.check_alias(m,v)
                sub = ("(" + self.lhs.abstract() + ".("+m+".value) " 
                    + str(self.operator) +  " " + str(v) + ")")
                sl.append(sub)
            if negated:
                rt = " and ".join(sl)
            else:
                rt = " or ".join(sl)
            return rt
        else:
            v = self.check_alias(m,self.rhs)
            sub = ("(" + self.lhs.abstract() + ".("+m+".value) " 
                + str(self.operator) +  " " + str(v) + ")")
            return sub


class Event(object):
    def __init__(self,t,cdts,alias=None):
        self.topic = t
        self.conditions = cdts  #[Condition]
        self.alias = alias
        # isReference(-1) isLiteral(1) or isRange(2) or isSet(3)

    def specification(self,m,alias=False,negated=False):
        rs = ""
        if negated:  #alias = False   
            rs = " or ".join(map(lambda x: x.specification(m,negated=True), self.conditions))
        else:
            rs = " and ".join(map(lambda x: x.specification(m), self.conditions))
        return rs



class Observable(object):
    def __init__(self,b):
        self.behaviour = b

class Existence(Observable):
    def __init__(self,b):
        self.behaviour = b  #[Event]
    def specification(self,node=None):
        s = ""
        sl = []
        node = "Node" if node is None else str(node)
        for e in self.behaviour:
            sub_spec = ("(some m0: " + node + ".outbox & " + "topic." + e.topic.replace('/','_') 
                        + " | (" + e.specification("m0") + "))")
            sl.append(sub_spec)
        s = "(" + "or".join(sl) + ")"
        return s

class Absence(Observable):
    def __init__(self,b):
        self.behaviour = b  #[Event]
    def specification(self,node=None):
        s = ""
        sl = []
        node = "Node" if node is None else str(node)
        for e in self.behaviour:
            sub_spec = ("(no m0: " + node + ".outbox & topic." + e.topic.replace('/','_')
                        + " | (" + e.specification("m0",negated=True) + "))")
            sl.append(sub_spec)
        s = "(" + " or ".join(sl) + ")"
        return s

class Cause(Observable):
    def __init__(self,b,t):
        self.trigger = t    #[Event]
        self.behaviour = b  #[Event]
    def specification(self,node=None): # Trigger => eventually Behaviour
        node = "Node" if node is None else str(node)
        alias = False
        trigger_spec = ""
        behaviour_spec = ""
        # Trigger Specification
        if (len(self.trigger) == 1) and (self.trigger[0].alias is not None):
            alias = True
            ts = ("all m0: " + node + ".inbox & topic." + self.trigger[0].topic.replace('/','_') +
                    " | (" + self.trigger[0].specification("m0") + ")")
            trigger_spec = ts
        else:
            tl = []
            for e in self.trigger:
                ts = ("(some m0: " + node + ".inbox & topic." + e.topic.replace('/','_') +
                    " | (" + e.specification("m0") + "))")
                tl.append(ts)
            trigger_spec = "(" + " or ".join(tl) + ")"
        #Behaviour Specification
        bl = []
        for e in self.behaviour:
            spec = ("(some m1: " + node + ".outbox & topic." + e.topic.replace('/','_') +
                " | (" + e.specification("m1",alias=alias) + "))")
            bl.append(spec)
        behaviour_spec = "(" + " or ".join(bl) + ")"
        
        rts = trigger_spec + "\n\t\t\timplies eventually (" + behaviour_spec + ")"
        return rts



class Requirement(Observable):
    def __init__(self,b,t):
        self.behaviour = b  #[Event]
        self.trigger = t    #[Event]
    def specification(self,node=None): # Behaviour => before once Trigger
        node = "Node" if node is None else str(node)
        alias = False
        behaviour_spec = ""
        trigger_spec = ""
        # Behaviour Specification
        if (len(self.behaviour) == 1) and (self.behaviour[0].alias is not None):
            alias = True
            bs = ("all m1: " + str(node) + ".outbox & topic." + self.behaviour[0].topic.replace('/','_') +
                 "| (" + self.behaviour[0].specification("m1") + ")")
            behaviour_spec = bs
        else:
            bl = []
            for e in self.behaviour:
                bs = ("(some m1: " + str(node) + ".outbox & topic." + e.topic.replace('/','_') + 
                    " | (" + e.specification("m1") + "))")
                bl.append(bs)
            behaviour_spec = "(" + " or ".join(bl) + ")"
        # Trigger Specification
        trigger_specs = []
        for e in self.trigger:
            spec = ("(some m0: " + str(node) + ".inbox & topic." + e.topic.replace('/','_') +
                    " | (" + e.specification("m0",alias=alias) + "))")
            trigger_specs.append(spec)
        trigger_spec = "(" + " or ".join(trigger_specs) + ")"
        rts = behaviour_spec + "\n\t\t\timplies before once (" + trigger_spec + ")"
        return rts


class Property(object): 
    def __init__(self,p,o):
        self.pattern = p
        self.observable = o

    def specification(self,signature=None):
        spec = ""
        if signature is not None:
            spec = self.observable.specification(node=signature)
        else:
            spec = self.observable.specification()
        return spec
        
####################################################
############## META-MODEL EXTRACTION ###############
####################################################
class Topic(object):
    def __init__(self, rosname, type_name):
        self.rosname = rosname
        self.type = type_name
        self.signature = self.abstract(rosname)
        self.vf = []    # VALID FIELDS

    def include_field(self,f_obj):
        aux = map(lambda x: str(x.token), self.vf)
        if str(f_obj.token) not in aux:
            self.vf.append(f_obj)

    def field_constraint(self):
        s = ""
        if self.vf == []:
            s = "\tno topic." + self.signature + "\n"
        else:
            fl = []
            for f in self.vf:
                fl.append(f.abstract())
            fs = "(" + " + ".join(fl) + ")"
            #"in" operator can be used instead
            s = "\t((topic."+self.signature+").value).Value in (" + fs + ")\n" 
        return s

    def abstract(self,rosname):
		signature = rosname.replace('/', '_')
		return signature

    def declaration(self):
        declaration = ("one sig " + self.signature + " extends Topic{}\n\n")
        return declaration


class Node(object):
    def __init__(self, rosname, subscribes=[], advertises=[],properties=[]):
        self.rosname = rosname
        self.signature = self.abstract(rosname)
        self.subscribes = map(lambda x: self.translate(x), subscribes)
        self.advertises = map(lambda y: self.translate(y), advertises)
        self.properties = properties
	
    def abstract(self,rosname):
        signature = rosname.replace('/', '_')
        return signature
	
    def translate(self,rosname):
        signature = self.abstract(rosname)
        signature = signature.replace('~', str(self.signature))
        return signature

    def declaration(self):
        subscribes = "none" if (self.subscribes == []) else ' + '.join(self.subscribes)
        advertises = "none" if (self.advertises == []) else ' + '.join(self.advertises)
        declaration = ("one sig " +
                       self.signature + " extends Node{}{\n" +
                       "\tsubscribes = " + subscribes +
                       "\n\tadvertises = " + advertises + "\n}\n\n")
        if self.properties != []:
            declaration += "fact " + self.signature + "_behaviour{\n"
            declaration += "\talways{\n\t" 
            for p in self.properties:
                declaration += "\t" + p.specification(signature=self.signature) + "\n\t"
            declaration += "\n\t}\n}\n\n"
        return declaration

####################################################
############## VALUE DISCRETIZATION ################
####################################################
class NumericTree(object):
    def __init__(self):
        self.values = dict()
    #Float -> String
    def toString(self,n):
        str_v = str(n)
        str_v = str_v.replace('.','p')
        str_v = str_v.replace('-','m')
        return str_v
    
    def has_key(self,values):
        if (values[0].strip()) == "numeric":
            values.pop(0)
            return True
        else:
            return (values[0].strip()) in self.values.keys()
    
    # [String] -> Operator x Interval
    def conjunction(self,values):
        interval = I.closed(-I.inf,I.inf)
        for v in values:
            v = v.strip()
            new_i = self.values.get(v)
            interval = interval & new_i
        if len(interval) == 1:  # one interval
            if interval.lower == interval.upper:
                return "=", interval.lower
            else:
                return "in", interval
        else:
            "UNKNOWN", "UNKNOWN"
    # Float -> Void
    def values_repartition(self,f):
        # DOING
        print("will do value repartition")

    #HplLiteral -> [String]
    def include_literal(self,v,operator=None):
        v = float(v.value)
        #if operator is not None and operator in ["!=", "not in"]:
            #self.values_repartition(v)
        str_v = self.toString(v)
        signature = "num_" + str_v
        interval = I.singleton(v)
        self.values.update({signature:interval})
        return [signature]
    
    #HplSet -> [String]
    def include_set(self,vls,operator=None):
        rt = []
        values = vls.values
        #if operator is not None and operator in ["!=", "not in"]:
        #    for v in values:
        #        self.values_repartition(v)
        for v in values:
            v = float(v.value)
            str_v = self.toString(v)
            signature = "num_" + str_v
            interval = I.singleton(v)
            self.values.update({signature:interval})
            rt.append(signature)
        return rt
    #HplRange -> [String]
    def include_range(self,v,operator=None):
        #if operator is not None and operator in ["!=","not in"]:
        #    self.value_repartition(v)
        lower_bound = v.lower_bound.value
        upper_bound = v.upper_bound.value
        lbstr = self.toString(lower_bound)
        upstr = self.toString(upper_bound)
        signature = "num_from_" + lbstr + "_to_" + upstr
        interval = I.closed(lower_bound,upper_bound)
        self.values.update({signature:interval})
        return [signature]
    # String -> [String]
    def independence_list(self,signature):
        il = []
        v = self.values.get(signature)
        for key in self.values.keys():
            if ((self.values[key] & v) == I.empty()):
                il.append(key)
        return il
    # String -> [String]
    def inclusion_list(self,signature):
        il = []
        v = self.values.get(signature)
        for key in self.values.keys():
            if v in self.values[key] and signature != key:
                il.append(key)
        return il
    def declaration(self):
        s = ""
        independence_fact = ""
        inclusion_fact = ""
        singleton_fact = ""
        for k in self.values.keys():
            s += "sig " + str(k) + " in numeric{}\n\n"
            independence_list = self.independence_list(k)
            if independence_list != []:
                independence_fact +=("\t no " + str(k) + " & (" +
                                    ' + '.join(independence_list) + ")\n")
            inclusion_list = self.inclusion_list(k)
            if inclusion_list != []:
                inclusion_fact += ("\t" + str(k) + " in (" +
                                ' + '.join(inclusion_list) + ")\n")
            v = self.values.get(k)
            if v.is_atomic() and v.upper == v.lower:
                singleton_fact += "\t lone " + k + "\n"
        if len(independence_fact)>0:
            s += "fact Independence {\n" + independence_fact + "}\n\n"
        if len(inclusion_fact)>0:
            s += "fact Inclusions {\n" + inclusion_fact + "}\n\n"
        if len(singleton_fact)>0:
            s += "fact Singletons {\n" + singleton_fact + "}\n\n"
        return s


class StringTree(object):
    def __init__(self):
        self.values = dict()
    #String -> String
    def toString(self,s):
        s = s.replace('\"','')
        return s
    def conjunction(self,values):
        return "NOT IMPLEMENTED"
    #HplLiteral -> [String]
    def include_literal(self,v):
        v = v.value
        str_v = self.toString(v)
        signature = "str_" + str_v
        self.values.update({signature:v})
        return [signature]
    #HplSet -> [String]
    def include_set(self,vls):
        rt = []
        values = vls.values
        for v in values:
            v = v.value
            str_v = self.toString(v)
            signature = "str_" + str_v
            self.values.update({signature:v})
            rt.append(signature)
        return rt
    
    def declaration(self):
        s = ""
        independence_fact = ""
        singleton_fact = ""
        for k in self.values.keys():
            s += "lone sig " + str(k) + " extends string{}\n\n"
        return s


####################################################
############# CONCRETE-CONFIGURATION ###############
####################################################
class Configuration(object):
    def __init__(self, name, nodes, topics, scopes, properties=None):
        self.name = name
        if properties is None:
            raise Exception("Configuration Specification is Required.")
        self.topics = dict()
        self.nodes = dict()
        self.field = dict()
        self.properties = dict()
        self.hpl_map = dict()
        self.numeric_tree = NumericTree()  
        self.string_tree = StringTree()
        self.value_scope = scopes['Value']
        self.message_scope = scopes['Message']
        self.time_scope = scopes['Time']
        self.create_structure(nodes, topics)
        self.create_properties(properties)
        self.prune_model()
    # [String] -> Value Type x Interval
    def values_concretization(self,values):
        if self.numeric_tree.has_key(values) is True:
            return self.numeric_tree.conjunction(values)
        else:
            return self.string_tree.conjunction(values)
        return None, None
    # String -> Bool
    def validate_operator(self,op):
        if op in ["!=","=","in","not in"]:
            return op
        else:
            raise Exception('Unsupported Operator Use.')

    #Token String x Topic x Type -> Field
    def gen_field(self,token,topic,t):
        topic_obj = self.topics.get(topic)
        topic_type = topic_obj.type
        field_obj = Field(token,t,topic_type)
        field_code = str(token) + str(topic_type)
        self.field.update({field_code: field_obj})
        topic_obj.include_field(field_obj)
        return field_obj

    #HplValue -> TYPE, [Value]
    def gen_value(self,hplvalue,op): # Including the Operator to solve the issue of the values.
        if hplvalue.is_reference:
            return -1, []
        if hplvalue.is_literal:
            if isinstance(hplvalue.value,(int,long,float)):
                sigl = self.numeric_tree.include_literal(hplvalue,operator=op)
                return 1, sigl
            else:
                sigl = self.string_tree.include_literal(hplvalue)
                return 2, sigl
        if hplvalue.is_range:   
            sigl = self.numeric_tree.include_range(hplvalue,operator=op)
            return 3, sigl
        if hplvalue.is_set:
            sigl = []
            values = hplvalue.values
            nums = (filter(lambda x: isinstance(x.value,(int,long,float)), values) == values)
            if nums is True:
                sigl = self.numeric_tree.include_set(hplvalue,operator=op)
                return 4,sigl
            else:
                sigl = self.string_tree.include_set(hplvalue)
                return 5, sigl   

    #[HplFieldCondition] -> [Condition]
    def gen_conditions(self,hplconditions,t):
        conditions = []
        for c in hplconditions:
            op = self.validate_operator(c.operator)
            tp, vlist = self.gen_value(c.value,op) 
            ftoken = self.gen_field(c.field.token,t,tp)
            if tp == -1:
                condition = Condition(ftoken, op, -1)
                conditions.append(condition)
            if tp == 4 or tp == 5:
                condition = Condition(ftoken, op, vlist)
                conditions.append(condition)
            else:
                for v in vlist:
                    condition = Condition(ftoken, op ,v)
                    conditions.append(condition)
        return tp, conditions

    #HplEvent -> Event
    def econversion(self,e):
        t = e.topic
        a = e.alias
        tp, cds = self.gen_conditions(e.msg_filter.conditions,t)
        rt = Event(t,cds,alias=a)
        return rt

    #HplChainDisjunction -> [Event]
    def create_events(self,tle):
        events = []
        for hpleventchain in tle.chains:
            if len(hpleventchain.events) > 1:
                raise Exception ("Event-Chains are not Supported.")
            else:
                e = hpleventchain.events[0]
                events.append(e)
        rt = map(lambda x: self.econversion(x) ,events)
        return rt

    #HplObservable -> Observable
    def create_obs(self,pattern,obs):
        o = None
        b = self.create_events(obs.behaviour)
        if pattern == 1: 
            o = Existence(b)
        elif pattern == 2: 
            o = Absence(b)
        else:
            t = self.create_events(obs.trigger)
            if pattern == 3:        
                o = Cause(b,t)
            if pattern == 4:        
                o = Requirement(b,t)
        return o

    #HplProperty -> Property
    def create_prop(self,hpl_prop): 
        scope_type = hpl_prop.scope.scope_type
        if scope_type == 1:    
            pattern = hpl_prop.observable.pattern
            o = self.create_obs(pattern,hpl_prop.observable)
            p = Property(pattern,o)
            return p
        else:
            raise Exception("Property Scope Unsupported.")
        return hpl_prop

    def create_structure(self, nodes, topics):
        for t in topics:  # Extract Type and Topic
            name = str(t.rosname.full)
            if name.__contains__('?') is True:
                continue
            topic_obj = Topic(name, t.type)
            self.topics.update({name: topic_obj})
        for n in nodes:  # Extract Node
            name = str(n.rosname.full)
            if name.__contains__('?') is True:
                continue
            subscribes = map(lambda x: x.rosname.full , n.subscribers)
            subscribes = filter(lambda x: not x.__contains__("?"), subscribes)
            advertises = map(lambda x: x.rosname.full, n.publishers)
            advertises = filter(lambda x: not x.__contains__("?"), advertises)          
            properties = map(lambda x: self.create_prop(x), n.node.hpl_properties)
            node_obj = Node(name, subscribes=subscribes, advertises=advertises,
                            properties=properties)
            self.nodes.update({name: node_obj})

    def create_properties(self,hpl_props):
        c = 0
        for p in hpl_props:
            prop = self.create_prop(p)
            name = "prop_" + str(c)
            self.properties.update({name: prop})
            self.hpl_map.update({name: p})
            c +=1

    def delete_node(self,k):
        n = self.nodes.pop(k)
        del n
        return 

    def delete_topic(self,t):
        for k in self.nodes.keys():
            node = self.nodes[k]
            if t.signature in node.subscribes:
                node.subscribes.remove(t.signature)
            if t.signature in node.advertises:
                node.advertises.remove(t.signature)
        mt = t.rosname
        topic_obj = self.topics.pop(mt)
        del topic_obj
        return 

    def prune_model(self):  
        subscribers = []
        advertisers = [] 
        for k in self.nodes.keys():
            node = self.nodes[k]
            subscribers = subscribers + node.subscribes
            advertisers = advertisers + node.advertises
        # Delete Dead Topics.
        for k in self.topics.keys():
            topic = self.topics[k]
            topic_name = topic.signature
            if (topic_name not in subscribers) or (topic_name not in advertisers):
                self.delete_topic(topic)   
        # Delete Dead Nodes.
        for k in self.nodes.keys():
            node = self.nodes.get(k)
            if node.subscribes == [] and node.advertises == []:
                self.delete_node(k)
        return 

    def write_specification(self):
        s = ""
        for k in self.properties:
            p = self.properties.get(k)
            ps = p.specification()
            s += ("check " + str(k) + "{\n\talways {\n\t\t" + ps 
                + "\n\t}\n} for 4 but exactly " + 
                str(self.value_scope) + " Value, " + str(self.message_scope) + " Message, exactly " +
                str(self.time_scope) + " Time\n\n")
        return s

    # Void -> String
    def type_coherency_fact(self):
        spec = "fact type_coherency{\n"
        for k in self.topics.keys():
            topic_obj = self.topics.get(k)
            spec += topic_obj.field_constraint()
        spec +="\n}\n\n"
        return spec

    def specification(self):
        spec = ""
        # Value Declaration (Both String and Numeric Tree.)
        spec += self.numeric_tree.declaration()
        spec += self.string_tree.declaration()
        for k in self.field.keys():
            spec += self.field[k].declaration()
        for k in self.topics.keys():
            spec += self.topics[k].declaration()
        spec += self.type_coherency_fact()
        for k in self.nodes.keys():
            spec += self.nodes[k].declaration()
        spec += self.write_specification() 
        return spec  