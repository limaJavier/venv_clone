import shutil
import sys
import os
from magic import Magic

if __name__ == '__main__':
    SOURCE_ENV = os.path.abspath(sys.argv[1])
    DEST_ENV = os.path.abspath(sys.argv[2])
    SOURCE_SCRIPT_DIR = SOURCE_ENV + '/bin/'
    DEST_SCRIPT_DIR = DEST_ENV + '/bin/'

    shutil.copytree(SOURCE_ENV, DEST_ENV)

    mime = Magic(mime=True)
    scripts = []
    for file in os.listdir(SOURCE_SCRIPT_DIR):
        if mime.from_file(SOURCE_SCRIPT_DIR + file)[:4] == 'text':
            scripts.append(file)

    for script in scripts:
        source_script = SOURCE_SCRIPT_DIR + script
        dest_script = DEST_SCRIPT_DIR + script
        os.remove(dest_script)

        with open(source_script, 'r') as file:
            lines = file.readlines()

        processed_lines = []
        for line in lines:
            processed_lines.append(line.replace(SOURCE_ENV[:-5], DEST_ENV[:-5]))

        with open(dest_script, 'w') as file:
            file.writelines(processed_lines)

        os.chmod(dest_script, 0o755)
    
    print('Done')