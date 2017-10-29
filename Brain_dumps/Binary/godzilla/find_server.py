#!/usr/bin/env python
from simuvex import SimProcedure
from angr import Hook, Project
import angr
import claripy
import simuvex

from pwn import *

# nc pwnable.kr 9004
# conn = process("./godzilla")

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
        print 'alarm called with' + str(alarm_arg)
        return 1

alarm_plt = 0x12dc # todo get this automagically
proj = angr.Project('./godzilla_server',load_options={'main_opts': {'custom_base_addr': 0}})
proj.hook(alarm_plt,Hook(alarm_hook))
state = proj.factory.entry_state()#add_options=simuvex.o.unicorn, concrete_fs=True
path_group = proj.factory.path_group(state)#, save_unconstrained=True)

# dump(path_group.active[0].state.posix)

find = 0x7003730 #+ 0x400000

# path_group.explore(find=find)

# while path_group.active:
# 	# in order to save memory, we only keep the recent 1 deadended or errored paths
# 	print "INPUT"
# 	print path_group.active[0].state.posix.dumps(0)
# 	print "OUTPUT"
# 	print path_group.active[0].state.posix.dumps(1)
# 	# if 'deadended' in path_group.stashes and path_group.deadended:
# 	# 	path_group.stashes['deadended'] = path_group.deadended[-1:]
# 	# if 'errored' in path_group.stashes and path_group.errored:
# 	# 	path_group.stashes['errored'] = path_group.errored[-1:]
# 	path_group.run(n=1)

# def step_func(lpg):
#     lpg.stash(filter_func=lambda path: path.addr == 0x400c06, from_stash='active', to_stash='avoid')
#     lpg.stash(filter_func=lambda path: path.addr == 0x400bc7, from_stash='active', to_stash='avoid')
#     lpg.stash(filter_func=lambda path: path.addr == 0x400c10, from_stash='active', to_stash='found')
#     return lpg

# path_group.step(step_func=step_func, until=lambda lpg: len(lpg.found) > 0)

# path_group.explore(find=lambda p: "The World Will Remember You As" in p.state.posix.dumps(1))

# print path_group.found[0].state.posix.dumps(0)
# print path_group
# if not path_group.found:
# 	print "naw that didn't work"
# 	# exit(1)

# s=path_group.found[0].state
# print s.posix.dumps(0)
# print s.posix.dumps(1)

