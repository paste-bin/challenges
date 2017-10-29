#!/usr/bin/env python

import angr
import claripy
# from angr import Project, SimProcedure
from angr.simos import SimProcedure
# p = angr.project.load_shellcode(open("main.bin").read(), "x86", start_offset=0x7C00, load_address=0x7C00)

entry = 0x8000000
win	  = 0x800005c

# proj = angr.Project("./old.bin")
proj = angr.Project("./32.bin")
# state = proj.factory.entry_state(add_options=simuvex.o.unicorn)
# state = p.factory.blank_state(addr=0x7C6F)0x800005c
state = proj.factory.blank_state(addr=entry)

x = claripy.BVS('x', 0x3c*8)

state.memory.store(0x1234, x)

paths = proj.factory.path_group(state) 

# proj.factory.block(paths.active[0].addr).vex.pp()



# @proj.hook(0x8000000, length=5)
# def set_rax(state):
# 	state.regs.rax = 1



# class BugFree(SimProcedure):
#     def run(self):
#     	print "hi"
#         return 0

# fucked = 0x8000026
# proj.hook(fucked, BugFree)
# # 0x8000026,

# while paths.active:
#     # in order to save memory, we only keep the recent 1 deadended or errored paths
#     paths.run(n=1)
#     if len(paths.active) > 0:
#     	try:
#     		proj.factory.block(paths.active[0].addr).vex.pp()
#     		paths.active[0].state.se.any_str(x)
#     	except:
#     		pass
#     print paths

#     # print "INPUT"
#     # print paths.active[0].state.posix.dumps(0)
#     # print "OUTPUT"
#     # print paths.active[0].state.posix.dumps(1)

#     if 'deadended' in paths.stashes and paths.deadended:
#         paths.stashes['deadended'] = paths.deadended[-1:]
#     if 'errored' in paths.stashes and paths.errored:
#         paths.stashes['errored'] = paths.errored[-1:]

# paths.explore(find=win) 

# win = 0x800000c
# win = 0x8000057
win = 0x800002b
paths.explore(find=win) 


# print paths.active
print paths
if paths.found:
	flag = paths.found[0].state.se.any_str(x)
	print flag
	print flag.encode('hex')
