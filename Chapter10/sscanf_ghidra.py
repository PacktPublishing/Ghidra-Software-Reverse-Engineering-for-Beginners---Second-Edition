from ghidra.program.database.symbol import FunctionSymbol
from ghidra.program.model.pcode import PcodeOp
from ghidra.app.decompiler import DecompInterface
from ghidra.app.decompiler import DecompileOptions
from docking.options import OptionsService

# From https://github.com/0xAlexei/INFILTRATE2019/blob/master/PCodeMallocDemo/MallocTrace.java#L724
def get_decompiler(state, program):
    tool = state.getTool()
    decompiler_options = DecompileOptions()
    decompiler = DecompInterface()
    if tool is not None:
        service = tool.getService(OptionsService)
        if service is not None:
            opt = service.getOptions("Decompiler")
            decompiler_options.grabFromToolAndProgram(None, opt, program)

    decompiler.setOptions(decompiler_options)

    decompiler.toggleCCode(True)
    decompiler.toggleSyntaxTree(True)
    decompiler.setSimplificationStyle("decompile")

    return decompiler

def process_sscanf_caller(hcaller, sscanf):
    for op in hcaller.pcodeOps:
        if op.opcode == PcodeOp.CALL and op.inputs[0].offset == sscanf.address.offset:
            # input[0] is the call target
            # input[1] is the destination
            # input[2] is the format string
            # input[3:] are the args
            num_args = len(op.inputs) - 3
            # Can track defs via input[X].def

            if op.output is None:
                # No use of return value
                print("The sscanf call at 0x%s is worth looking at, no comparisons were found despite %d arguments" % (op.seqnum.target, num_args))
            else:
                for use in op.output.descendants:
                    if use.opcode == PcodeOp.INT_EQUAL:
                        if use.inputs[0].getDef() == op:
                            comparand_var = use.inputs[1]
                        elif use.inputs[1].getDef() == op:
                            comparand_var = use.inputs[0]
                        else:
                            raise Exception("Should not have reached here")

                        if comparand_var.isConstant():
                            comparand = comparand_var.offset
                            if comparand < num_args:
                                print("The sscanf call at 0x%s may be worth looking at, there is a comparison against %d but there are %d arguments" % (op.seqnum.target, comparand, num_args))

def find_sscanf_vulns():
    # currentProgram and state are globals that are provided for us
    program = currentProgram
    symbolTable = program.getSymbolTable()
    list_of_sscanfs = list(symbolTable.getSymbols('_sscanf'))
    list_of_sscanfs.append(symbolTable.getSymbols('sscanf').next())
    if len(list_of_sscanfs) == 0:
        print("sscanf not found")
        return

    decompiler = get_decompiler(state, program)
    if not decompiler.openProgram(program):
        print("Decompiler error")
        return

    functionManager = program.getFunctionManager()
    for sscanf in list_of_sscanfs:
        if isinstance(sscanf, FunctionSymbol):
            seen_functions = set()
            for ref in sscanf.references:
                if ref.fromAddress in seen_functions:
                    continue

                caller = functionManager.getFunctionContaining(ref.fromAddress)
                if caller is None:
                    continue

                seen_functions.add(ref.fromAddress)

                result = decompiler.decompileFunction(caller, decompiler.options.defaultTimeout, None)
                if result is None or result.highFunction is None:
                    print('Unable to decompile function at %s' % caller.entryPoint)
                    continue
                process_sscanf_caller(result.highFunction, sscanf)

if __name__ == '__main__':
    find_sscanf_vulns()

