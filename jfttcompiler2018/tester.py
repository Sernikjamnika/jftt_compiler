import os
import subprocess
import re


"""
Script quickly written to automatically compile programs and check their results against correct one.
It needs folder with tests, correct results and place for outputs.
"""

outputs_dir = "../outputs"
machine_dir = "../maszyna_rejestrowa"
results_dir = "../results"
test_dir = "../tests"
compiler_dir = os.getcwd()

def check_same_results(our_results, right_results):
    if len(our_results) != len(right_results):
        return False

    for our, right in zip(our_results, right_results):
        our = our.split()[-1]
        if our != right:
            return False
            
    return True 

if __name__ == "__main__":
    # create outputs of compiler
    os.chdir(compiler_dir)
    subprocess.call(['python', 'main.py', test_dir, outputs_dir, '-test'])
    output_codes = os.listdir(outputs_dir)
    os.chdir(machine_dir)

    # create outputs given by register_machine
    results = [] 
    output_codes.sort()   

    for output_code in output_codes:
        result = subprocess.run(['./maszyna-rejestrowa', outputs_dir+'/'+output_code], stdout=subprocess.PIPE)
        results.append(result.stdout.decode('utf-8'))


    # check if results are correct and print them
    os.chdir(results_dir)
    right_results = os.listdir()
    right_results.sort()

    general_result = True

    for right_result, result in zip(right_results, results):
        file_name = right_result
        #get right results
        with open(right_result, 'r') as file:
            right_result = file.read()
        right_result = right_result.split()
        result = re.findall(r'> [\d]+', result)
        test_result = check_same_results(result, right_result)
            
        general_result = general_result and test_result

        print(file_name, test_result, result, right_result)

    print(general_result)




    
