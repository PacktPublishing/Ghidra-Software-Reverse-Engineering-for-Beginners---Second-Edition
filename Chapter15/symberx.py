from miasm.analysis.binary import Container
from miasm.analysis.machine import Machine
from miasm.core.locationdb import LocationDB
from miasm.ir.symbexec import SymbolicExecutionEngine

from z3 import *
from miasm.ir.translators.z3_ir import  TranslatorZ3

start_addr = 0x402300
loc_db = LocationDB()
target_file = open("hello_world.exe", 'rb')
container = Container.from_stream(target_file, loc_db)

machine = Machine(container.arch)
mdis = machine.dis_engine(container.bin_stream, 
                          loc_db=loc_db)
ira = machine.lifter_model_call(mdis.loc_db)
asm_cfg = mdis.dis_multiblock(start_addr)
ira_cfg = ira.new_ircfg_from_asmcfg(asm_cfg)
symbex = SymbolicExecutionEngine(ira)
symbex_state = symbex.run_block_at(ira_cfg, start_addr)
print (symbex_state)

translatorZ3 = TranslatorZ3()

solver = Solver()
solver.add(translatorZ3.from_expr(symbex_state)  == 0x402302)

print(solver.check())

if (solver.check() == sat):
    print(solver.model())

solver = Solver()
solver.add(translatorZ3.from_expr(symbex_state)  == 0x4022E0)

print(solver.check())

if (solver.check() == sat):
    print(solver.model())
