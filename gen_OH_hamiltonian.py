import pennylane as qml


# load molecular datasets (OH: 12 qubits)
available_bondlength = ['0.5', '0.54', '0.58', '0.62', '0.66', '0.7', '0.74', '0.78', '0.82', '0.86', '0.9', '0.94', '0.964', '0.98', '1.02', '1.06', '1.1', '1.14', '1.18', '1.22', '1.26', '1.3', '1.34', '1.38', '1.42', '1.46', '1.5', '1.54', '1.58', '1.62', '1.66', '1.7', '1.74', '1.78', '1.82', '1.86', '1.9', '1.94', '1.98', '2.02', '2.06', '2.1']
for bondlength in available_bondlength:
    print('bond length = ', bondlength)
    OHdatasets = qml.data.load("qchem", molname="OH-", basis="STO-3G", bondlength=bondlength)
    OHdata = OHdatasets[0]
    hamiltonian = OHdata.hamiltonian
    print(hamiltonian.coeffs)
