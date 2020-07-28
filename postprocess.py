import numpy as np

terms = np.genfromtxt('q4/terms.csv', dtype='str')
results = np.genfromtxt('q4/X.csv', dtype='str')

formula = ""
counter = 0
for i, term in enumerate(terms):
    if results[i] == "1":
        counter += 1
        formula += " + " + term

print(formula)
print(counter)
