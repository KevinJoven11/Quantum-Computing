# Linear Combination of Unitaries (LCU)

## This repository builds step-by-step (file-by-file) the entire circuit of LCU.

The LCU circuit can be designed as the following image.

<div align="center">
    <img src="images/LCU.png" width="600">
</div>

The different building blocks, prepare (Prep.) and select (Selec) are developed in different files. Each implements the following design strategy, as shown in the following two figures.

<div align="center">
    <img src="images/Prep.png" width="600">
</div>

<div align="center">
    <img src="images/Select.png" width="600">
</div>

Combining them, we can implement the LCU circuit, which, in our case, will be the building block of a more complex quantum circuit (Hint: QSVT).

Feel free to leave any questions!
