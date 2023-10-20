import os
import sys

# ---
'''
python3 I:/mdwiki/newupdater/test_med.py Retinol
'''
# ---
title = sys.argv[1]
# ---
command1 = f"python3 I:/mdwiki/medUpdater/med.py {title} from_toolforge xx"
# ---
command2 = f"python3 I:/mdwiki/newupdater/med.py {title} from_toolforge xx"
# ---
print(f'command1: {command1}')
ux = os.system(command1)
# ---
print(f'result1: {ux}')
# ---
print(f'command2: {command2}')
uu = os.system(command2)
# ---
print(f'result2: {uu}')
# ---
