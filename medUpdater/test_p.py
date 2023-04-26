import codecs
import txtlib2
import os
#---
'''
<!-- Names -->

<!-- Clinical data -->

<!-- External links -->

<!-- Legal data --><!-- Legal status -->

<!-- Pharmacokinetic data -->

<!-- Chemical and physical data -->


'''
#---
dir = os.path.dirname(os.path.realpath(__file__))
#---
text = codecs.open(dir + "/test_p.txt", "r", "utf-8").read()
#---
params = txtlib2.extract_templates_and_params(text)[0]['params']
#---
for param, value in params.items():
    print(f"|{param} = {value.strip()}")