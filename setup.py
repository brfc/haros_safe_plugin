import os

def install():
	print("[MC] Installing ...")
	environment_dir = "/.plugin_mc/"
	mode = 0o777
	print("[MC] Generating Cache ...")
	os.mkdir(environment_dir, mode)
	cmd = "cp ./mc/electrum/electrum_pi.jar /.plugin_mc/"
	os.system(cmd)
	cmd = "cp plugin.yaml /.plugin_mc/"
	os.system(cmd)
	cmd =  ""
	cmd = "cp ./mc/electrum/meta.ele /.plugin_mc/"
	os.system(cmd)
	try:
		with open("/.plugin_mc/model.ele","w") as f:
			f.write("Empty Cache")
	except Exception as error:
		print(error)
	os.chmod("/.plugin_mc/model.ele", mode)
	

if __name__=="__main__":
	install()
