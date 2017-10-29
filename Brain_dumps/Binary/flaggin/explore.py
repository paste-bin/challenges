#!/usr/bin/env python
from simuvex import SimProcedure
from angr import Hook, Project
import angr
import claripy
import simuvex

from pwn import *
import sys

prog = "./faggin"

# binary
# nc pwnable.kr 9004
# conn = process()

# set logging level
angr.path_group.l.level = 1

def dump(obj):
	for attr in dir(obj):
		try:
			print "obj.%s = %s" % (attr, getattr(obj, attr))
		except:
			pass
class alarm_hook(SimProcedure):
    def run(self, alarm_arg):
        print 'alarm c alled with' + str(alarm_arg)
        return 1

# alarm_plt = 0x1690#0x12dc # todo get this automagically

error = 0xb0003d0

proj = Project(prog, load_options={'auto_load_libs': False})#,load_options={'main_opts': {'custom_base_addr': 0}}
proj.hook(error,Hook(alarm_hook))

state = proj.factory.entry_state()#add_options=simuvex.o.unicorn, concrete_fs=True

path_group = proj.factory.path_group(state)#, save_unconstrained=True)
path_group.explore(find=lambda p: len(p.state.posix.dumps(1)) > 0)



# cfg = proj.analyses.CFGAccurate(keep_state=True)


# # Symbolic buffer of size 15
# password_len = 2072 # from binary
# modulus_len = 10
# pe_len = 10
# s_password = state.se.BVV("modulus:")
# for x in range(modulus_len):
# 	mod_char = state.se.BVS('modulus_char', 8)
# 	state.add_constraints(mod_char >= ord("0"))
# 	state.add_constraints(mod_char <= ord("9"))
# 	s_password = s_password.concat(mod_char)
	
# s_password = s_password.concat(state.se.BVV("\nprivateExponent:"))
# for x in range(pe_len):
# 	mod_char = state.se.BVS('exp_char', 8)
# 	state.add_constraints(mod_char >= ord("0"))
# 	state.add_constraints(mod_char <= ord("9"))
# 	s_password = s_password.concat(mod_char)
# password_filename = "/home/godzilla/private.key"

# # Symbolic memory region containing the symbolic buffer
# content = simuvex.SimSymbolicMemory(memory_id='file_{}'.format(password_filename))
# content.set_state(state)
# content.store(0, s_password)

# # Symbolic file which associates the symbolic memory region with a filename
# password_file = simuvex.SimFile(password_filename, 'rw', size=password_len, content=content)
# fs = {
# 	password_filename: password_file
# }
# state.posix.fs = fs

# path_group = proj.factory.path_group(state)#, save_unconstrained=True)

# avoid = [0x18A6]

# next_inst = 0x183c

# path_group.explore(find=next_inst, avoid=avoid)

# def fucked(path):
# 	fucked = None
# 	try:
# 		s = path.state.se.any_str(s_password)
# 		fucked = len(s) > 0
# 		print hex(path.addr)
# 		print "private key file"
# 		print s
# 	except:
# 		fucked = False
# 		pass	
# 	return not fucked


# def step_func(lpg):
#     lpg.stash(filter_func=lambda path: path.addr == 0x400c06, from_stash='active', to_stash='avoid')
#     lpg.stash(filter_func=lambda path: path.addr == 0x400bc7, from_stash='active', to_stash='avoid')
#     lpg.stash(filter_func=lambda path: path.addr == 0x400c10, from_stash='active', to_stash='found')
#     return lpg

# while path_group.active:
# 	# in order to save memory, we only keep the recent 1 deadended or errored paths
# 	path_group.run(n=1)
# 	found = False
# 	for ac in path_group.active:
# 		try:
# 			print hex(ac.addr)
# 			print "private key file"
# 			print ac.state.se.any_str(s_password)

# 		except:
# 			pass
# 	path_group.stash(fucked, from_stash='active', to_stash='bad')

	# if path_group.active[0].addr > 0x185f and path_group.active[0].addr < 0x19c0:
	# 	break
	# print "INPUT"
	# print path_group.active[0].state.posix.dumps(0)
	# print "OUTPUT"
	# print path_group.active[0].state.posix.dumps(1)


	# Grab current files from our files dict
	# files = path_group.active[0].state.posix.files

	# The largest file ID is the content of the file we care about
	# """
	# {0: <simuvex.storage.file.SimFile object at 0x7ffff0aa1410>, 1: <simuvex.storage.file.SimFile object at 0x7ffff0aa1690>, 2: <simuvex.storage.file.SimFile object at 0x7ffff0aa1910>, 3: <simuvex.storage.file.SimFile object at 0x7ffff5694960>, 4: <simuvex.storage.file.SimFile object at 0x7ffff5694960>, 3221227200L: <simuvex.storage.file.SimFile object at 0x7ffff089f5f0>}
	# """
	# curr_file_id = max(files.keys())

	# print "[+] solving rsa file" 
	# Print contents of our file
	# print path_group.active[0].state.posix.dumps(curr_file_id) 
	# print path_group.active[0].state.se.any_str(s_password)
	# sys.stdout.flush()


# path_group.step(step_func=step_func, until=lambda lpg: len(lpg.found) > 0)

# path_group.explore(find=lambda p: "The World Will Remember You As" in p.state.posix.dumps(1))

# path_group.deadended[0].state.posix.dumps(0)
# print path_group
# if not path_group.found:
# 	print "naw that didn't work"
# 	# exit(1)

# s=path_group.found[0].state
# print s.posix.dumps(0)
# print s.posix.dumps(1)

