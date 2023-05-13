assembler_path = "C:\modeltech64_10.5\examples\\risc-v\\riscv_assembler"
assembly_path = "C:\modeltech64_10.5\examples\\risc-v\Test"
result_path = 'C:\modeltech64_10.5\examples\\risc-v\Test\\results\\test'

import os
import sys
sys.path.insert(0, assembler_path)
import convert
import shutil
import main as pymodel


cnv = convert.AssemblyConverter(output_type = "t", nibble = False, hexMode = True)
cnv.convert(assembly_path+'\\assembly.s') 
shutil.copyfile(assembly_path+'\\assembly.txt','instruction.mem')

print("Starting up Modelsim simulation...")
os.system("vsim -c -do simulate.tcl")

print("Simulation finished. \n Storing result")

i = 1
while True:
    if not os.path.exists(result_path+ str(i)):
        os.makedirs(result_path+ str(i))
        break
    else :
        i = i+1

# shutil.copy(assembly_path+'\\assembly.s', result_path+ str(i))
shutil.copy('instruction.mem' , result_path+ str(i))
shutil.copy('data.mem' , result_path+ str(i))
shutil.copy('regbank.mem' , result_path+ str(i))

print("Running python model")
pymodel.main()

shutil.copy('regbank_python.mem' , result_path+ str(i))

# adds assembly to instruction 
newfile=''
with open('instruction.mem') as fh1, open(assembly_path+'\\assembly.s') as fh2:
    for line1, line2 in zip(fh1, fh2):
        newfile += line1.strip()+ '\t\t//'+line2
with open(result_path+ str(i)+"\\instruction.mem", 'w') as f:
    f.write(newfile)


# adds reg number to file
errorno = 0
regbank =''


log =''
with open('regbank.mem', 'r') as in_file , open('regbank_python.mem' , 'r') as py_mem:
    lines = in_file.readlines()
    lines = lines[3:]
    py_lines = py_mem.readlines()

    for l, line in  enumerate(lines):
        
        if line.strip() != py_lines[l].strip():

            if line.strip() == "xxxxxxxx" and py_lines[l].strip() == "00000000":
                pass
            else:
                errorno += 1
                log += "mismatch at r"+ str(l)+" py: "+ py_lines[l].strip() +"\t v: "+line.strip() +"\n"

        regbank+= line.strip()+ '\t\t//r' +str(l) +'\n'
        
with open(result_path+ str(i)+"\\regbank.mem", 'w') as out_file:
    out_file.write(regbank)


#write log

print('saving logs')

with open(result_path+ str(i)+"\\log.txt", 'w') as logfile:
    log = "Total no of mismatchas: "+ str(errorno) +"\n\n" +log 
    logfile.write(log)




print ("\n\nReport \n\tTotal no of mismatches : " +str(errorno))
print('\t detailed log '+result_path+ str(i)+"\\log.txt")


 