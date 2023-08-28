import pickle
import pennylane as qml
from pennylane import numpy as np
from math import pi
from ChemModel import translator, quantum_net
from Arguments import Arguments


# load molecular datasets (OH: 12 qubits)
# OHdatasets = qml.data.load("qchem", molname="OH", basis="STO-3G", bondlength=0.9)
# OHdata = OHdatasets[0]
# hamiltonian = OHdata.hamiltonian
# print(OHdata.molecule)
# print("molecular dataset used: {}".format(OHdata))


def chemistry(design):
    np.random.seed(42)
    args = Arguments()

    symbols = ["O", "H"]
    coordinates = np.array([0.0, 0.0, 0.0, 0.45, -0.1525, -0.8454])

    # Building the molecular hamiltonian
    hamiltonian, qubits = qml.qchem.molecular_hamiltonian(symbols, coordinates, charge=1)


    dev = qml.device("lightning.qubit", wires=args.n_qubits)

    @qml.qnode(dev, diff_method="adjoint")
    def cost_fn(theta):
        quantum_net(theta, design)
        return qml.expval(hamiltonian)
        print(hamiltonian)

    energy = []
    for i in range(5):
        q_params = 2 * pi * np.random.rand(design['layer_repe'] * args.n_qubits * 2)
        opt = qml.GradientDescentOptimizer(stepsize=0.4)

        for n in range(50):
            q_params, prev_energy = opt.step_and_cost(cost_fn, q_params)
            print(f"--- Step: {n}, Energy: {cost_fn(q_params):.8f}")
        energy.append(cost_fn(q_params))

    metrics = np.mean(energy)
    report = {'energy': metrics}
    print(metrics)
    return report


if __name__ == '__main__':
    # with open('data/chemistry_dataset', 'rb') as json_data:
    #     data = pickle.load(json_data)
    net = [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 4, 3, 4, 3, 1, 0, 1, 2, 3, 4, 5]
    design = translator(net)
    report = chemistry(design)
