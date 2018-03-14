# -*- coding: utf-8 -*-

__desc__ = "Physics"

from .docs import *

doc_c("celerity", "c", "Speed of light in vacuum", "m*s<sup>-1</sup>")
c_celerity = 299792458

doc_c("planck", "h", "Planck constant", "J*s<sup>-1</sup>")
c_planck = 6.62607004081e-34

doc_c("red_planck", "ħ", "Reduced Planck constant", "J*s<sup>-1</sup>")
c_red_planck = 1.054571629e-34

doc_c("planck_time", "t<sub>P</sub>", "Planck time", "s")
c_planck_time = 5.3911413e-44

doc_c("planck_temp", "T<sub>P</sub>", "Planck temperature", "K")
c_planck_temp = 1.41680833e32

doc_c("planck_mass", "m<sub>P</sub>", "Planck mass", "kg")
c_planck_mass = 2.17647051e-8

doc_c("planck_length", "l<sub>P</sub>", "Planck length", "m")
c_planck_length = 1.61622938e-35

doc_c("planck_charge", "q<sub>P</sub>", "Planck charge", "C")
c_planck_charge = 1.8755459e-18

doc_c("gravity", "G", "Gravitational constant", "N*m<sup>2</sup>*kg<sup>-2</sup>")
c_gravity = 6.6740831e-11

doc_c("vacuum_permit", "ε<sub>0</sub>", "Vacuum permittivity", "F*m<sup>-1</sup>")
c_vacuum_permit = 8.8541878176203898505365630317107502606083701665994e-12

doc_c("vacuum_permea", "μ<sub>0</sub>", "Vacuum permeability", "N*A<sup>-2</sup>")
c_vacuum_permea = 1.25663706143591729538505735331180115367886775975e-6

doc_c("vacuum_imped", "Z<sub>0</sub>", "Impedance of free space", "Ω")
c_vacuum_imped = 376.73031346177065546819840042031930826862350835242