import sys;
import subprocess;

mess_start = 2
mess_end   = 5
filename   = "fsdump.afa"

def is_directory(prefix):
    try:
        result = str(subprocess.check_output('adb shell cd ' + prefix))[mess_start:][:-mess_end]
        subprocess.call('adb shell cd ..')
        return True;
    except:
        return False;

def check_directory(file, prefix):
    try:
        inputs = str(subprocess.check_output('adb shell ls ' + prefix))[mess_start:][:-mess_end]
    except:
        return;
    if inputs=='':
        return;
    inputs = inputs.split('\\r\\n')
    for input in inputs:
        path = input if prefix == '' else prefix + '/' + input
        file.write(path + '\n')
        if is_directory(path):
            check_directory(file, path)
			
def read_file(path):
    with open(path) as f:
        return f.readlines()
			
''' 
Function searches for lines present in both dumps and removed them from both attays.
After that, lines present in first_dump_content were removed, lines present in 
second_dump_content are added
'''
def compare_two_dumps(first_dump, second_dump):
    first_dump_content = read_file(first_dump)
    second_dump_content = read_file(second_dump)
    '''Complexity is too high, need to decompose'''
    for first_line in first_dump_content:
        for second_line in second_dump_content:
            if first_line==second_line:
                first_dump_content = first_dump_content.remove(first_line)
                second_dump_content = second_dump_content.remove(second_line)
    print('Removed:')
    for removed in first_dump_content:
        print(removed)
    print('Added:')
    for added in second_dump_content:
        print(added)
			
def compare():
    if len(sys.argv) < 4:
        print('No dumps to compare')
        return;
    compare_two_dumps(sys.argv[2], sys.argv[3])

def main():
    path = ''
    if len(sys.argv) > 1:
        '''-C argument mush work too'''
        if sys.argv[1]=='-c':
            compare()
            return;
        path = sys.argv[1]
    file = open(filename, 'w')
    check_directory(file, path)
    file.close();

if __name__ == "__main__":
    main()