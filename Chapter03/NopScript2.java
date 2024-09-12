//This simple script allows you to patch bytes with NOP opcode
//@author Packt
//@category Memory
//@keybinding ctrl alt shift n 
//@menupath Tools.Packt.nop
//@toolbar 

import ghidra.app.script.GhidraScript;
import ghidra.program.model.mem.*;
import ghidra.program.model.address.*;

public class NopScript2 extends GhidraScript {

    public void run() throws Exception {
        Address startAddr = currentLocation.getByteAddress();
        byte nop = (byte)0x90; 
        try {
            int istructionSize = getInstructionAt(startAddr).getDefaultFallThroughOffset();
            removeInstructionAt(startAddr);
            for(int i=0; i<istructionSize; i++){
                setByte(startAddr.addWrap(i), nop);
            }
            disassemble(startAddr);
        }
        catch (MemoryAccessException e) {
            popup("Unable to nop this byte");
            return;
        }
    }
}