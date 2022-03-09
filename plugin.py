import os
from .mc.analyzer import *

def configuration_analysis(iface, scope):
	# Node Configurations
	if scope.nodes.__len__() <= 1:	
		return
	# Architectural Configurations
	print("[MC] Running analysis...")
	analyzer = Analyzer(scope.name, scope.nodes, scope.topics,properties=scope.hpl_properties)
	print("[MC] Model-Checking Specification...")
	rl = analyzer.model_check()
	
	print("[MC] Reporting results...")
	for r in rl:
		iface.report_violation("mc",r)
