import numpy as np
import itertools

# Solve M * X = B
# M = matrix of good configurations of vertices a,b,c,d, with bad configurations at the end
# B = vector of 0 values with 1 values at the end for each bad configuration
# X = vector of all possible coefficients for the polynomial

# Step 1: generate terms for X, all possible terms of the polynomial
# Inluding constant term, we have 175 terms for q=3
q = 3
nodes = {'a', 'b', 'c', 'd'}
colors = range(1, q+1)
max_degree = (2 * q) - 3

print("Generating terms")
terms = np.array([])
for size in range(1, max_degree + 1):
    for perm in itertools.combinations(nodes, size):
        for cperm in itertools.product(colors, repeat=size):
            terms = np.append(terms, set(zip(perm, cperm)))
print(str(len(terms)) + " terms generated")

print("Generating bad configs")
# Step 1.6: generate all 'bad' configs
bad_configs = np.array([])
for c1 in itertools.permutations(colors, q-1):
    for c2 in itertools.permutations(c1, q-1):
        config = {'a': c1[0], 'b': c1[1],
                  'c': c2[0], 'd': c2[1]}
        bad_configs = np.append(bad_configs, config)
print(str(len(bad_configs)) + " bad configs generated")

print("Generating all configs and filtering bad configs")
# Step 1.5: generate all possible 'good' configs
good_configs = np.array([])
for c in itertools.product(colors, repeat=(2*(q-1))):
    config = {'a': c[0], 'b': c[1], 'c': c[2], 'd': c[3]}
    if config not in bad_configs:
        good_configs = np.append(good_configs, config)
print(str(len(good_configs)) + " good configs generated")

# Filter for which bad configs to include
filtered_configs = bad_configs[:1]
offset = len(good_configs)

print("Generating M and B matrices")
# Step 2: generate M and B
M = np.empty((len(good_configs) + len(filtered_configs), len(terms) + 1))
B = np.empty((len(good_configs) + len(filtered_configs)))

print("Populating M and B matrices")
print(str(len(good_configs)) + " good configs to populate in the matrices")
# # populate M and B with entries for the 'good' configs
for i, config in enumerate(good_configs):
    if i % 100 == 0:
        print("Generating entry nr: " + str(i))
    e = np.empty((len(terms) + 1))
    for j, term in enumerate(terms):
        e[j] = 1
        for var in term:
            if config[var[0]] != var[1]:
                e[j] = 0
    e[len(e) - 1] = 1
    M[i] = e
    B[i] = 0

# populate M and B with entries for the 'bad' configs
for i, config in enumerate(filtered_configs):
    print(config)
    e = np.empty((len(terms) + 1))
    for j, term in enumerate(terms):
        e[j] = 1
        for var in term:
            if config[var[0]] != var[1]:
                e[j] = 0
    e[len(e) - 1] = 1
    M[i + offset] = e
    B[i + offset] = 1

# # Check shape for sanity check
print(M.shape)
print(B.shape)

# # Export to CSV
np.savetxt('M.csv', M, delimiter=',', fmt='%2d')
np.savetxt('B.csv', B, delimiter=',', fmt='%2d')
np.savetxt('configs.csv', bad_configs, delimiter=',', fmt='%s')

# Change terms to a readable format for storage to reference with lin-solver results
readable = np.array([])
for term in terms:
    rterm = ""
    for pair in term:
        rterm += pair[0] + str(pair[1])
    readable = np.append(readable, rterm)
readable = np.append(readable, ['1'])  # constant term
np.savetxt('terms.csv', readable, delimiter=',', fmt='%s')
