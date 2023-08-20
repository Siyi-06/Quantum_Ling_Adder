# Reducing Depth of Quantum Adder using Ling Structure - Code Repository

This repository contains the code implementation for the paper titled "Reducing Depth of Quantum Adder using Ling Structure." The code is developed using the Qiskit framework and provides functions for drawing quantum circuits as well as implementations of classical and quantum adders based on the Ling structure.

## Files

### Drawing Quantum Circuits Cost Functions

- `QC.py`: This file contains functions to draw the qubit count of different quantum addition circuits.

- `TC.py`:  This file contains functions to draw the T Count of different quantum addition circuits.

- `TD.py`:  This file contains functions to draw the T Depth of different quantum addition circuits.
### Classical Ling Adder

- `Classical_Ling_Adder.py`: This file contains the implementation of an n-bit classical Ling based Brent-Kung adder. 

### Quantum Ling Adder

- `4_bits_Quantum_Ling_Adder.py`: This file contains the implementation of a 4-bit quantum Ling adder. This quantum adder is designed using the Ling structure to efficiently perform addition operations.

- `n_bits_Quantum_Ling_Adder.py`: This file includes the implementation of an n-bit quantum Ling adder. (Users can customize 'n'.)
## Usage

To use the code provided in this repository, follow these steps:

1. Ensure you have Qiskit installed. You can install it using the following command:
pip install qiskit


2. Browse and run the various implementation files, such as `4_bits_Quantum_Ling_Adder.py` and `n_bits_Quantum_Ling_Adder.py`, to see how the quantum adders are implemented using the Ling structure.

## Acknowledgments

If you use this code for your research or find it helpful, please cite the original paper "Reducing Depth of Quantum Adder using Ling Structure" and providing a link to this repository.

---

For any questions or issues regarding the code, feel free to contact Siyi at siyi002@e.ntu.edu.sg.
