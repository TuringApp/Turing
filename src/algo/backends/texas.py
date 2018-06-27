# -*- coding: utf-8 -*-

from algo.stmts import *
from maths.nodes import *
from maths.parser import quick_parse as parse
from util import lstreplace, pairwise

tokens = {
#    'unused': [[0x00]],
    '►DMS': [[0x01]],
    '►Dec': [[0x02]],
    '►Frac': [[0x03]],
    '→': [[0x04]],
    'Boxplot': [[0x05]],
    '[': [[0x06]],
    ']': [[0x07]],
    '{': [[0x08]],
    '}': [[0x09]],
    'r_sym': [[0x0A], "r"],
    '°': [[0x0B]],
    '⁻¹': [[0x0C]],
    '²': [[0x0D]],
    'TR': [[0x0E], "T"], # matrix transpose
    '³': [[0x0F]],
    '(': [[0x10]],
    ')': [[0x11]],
    'round(': [[0x12]],
    'pxl-Test(': [[0x13]],
    'augment(': [[0x14]],
    'rowSwap(': [[0x15]],
    'row+(': [[0x16]],
    '*row(': [[0x17]],
    '*row+(': [[0x18]],
    'max(': [[0x19]],
    'min(': [[0x1A]],
    'R►Pr(': [[0x1B]],
    'R►Pθ(': [[0x1C]],
    'P►Rx(': [[0x1D]],
    'P►Ry': [[0x1E]],
    'median(': [[0x1F]],
    'randM(': [[0x20]],
    'mean(': [[0x21]],
    'solve(': [[0x22]],
    'seq(': [[0x23]],
    'fnInt(': [[0x24]],
    'nDeriv(': [[0x25]],
#    'unused': [[0x26]],
    'fMin(': [[0x27]],
    'fMax(': [[0x28]],
    ' ': [[0x29]],
    '"': [[0x2A]],
    ',': [[0x2B]],
    'ii': [[0x2C], "i"], # imaginary unit
    '!': [[0x2D]],
    'CubicReg': [[0x2E]],
    'QuartReg': [[0x2F]],
    '0': [[0x30]],
    '1': [[0x31]],
    '2': [[0x32]],
    '3': [[0x33]],
    '4': [[0x34]],
    '5': [[0x35]],
    '6': [[0x36]],
    '7': [[0x37]],
    '8': [[0x38]],
    '9': [[0x39]],
    '.': [[0x3A]],
    'EE': [[0x3B], "E"], # exponent
    ' or ': [[0x3C]],
    ' xor ': [[0x3D]],
    ':': [[0x3E]],
    '\n': [[0x3F]],
    ' and ': [[0x40]],
    'A': [[0x41]],
    'B': [[0x42]],
    'C': [[0x43]],
    'D': [[0x44]],
    'E': [[0x45]],
    'F': [[0x46]],
    'G': [[0x47]],
    'H': [[0x48]],
    'I': [[0x49]],
    'J': [[0x4A]],
    'K': [[0x4B]],
    'L': [[0x4C]],
    'M': [[0x4D]],
    'N': [[0x4E]],
    'O': [[0x4F]],
    'P': [[0x50]],
    'Q': [[0x51]],
    'R': [[0x52]],
    'S': [[0x53]],
    'T': [[0x54]],
    'U': [[0x55]],
    'V': [[0x56]],
    'W': [[0x57]],
    'X': [[0x58]],
    'Y': [[0x59]],
    'Z': [[0x5A]],
    'θ': [[0x5B]],
#    '2-byte': [[0x5C]], Matrices
#    '2-byte': [[0x5D]], Lists
#    '2-byte': [[0x5E]], Equations
    'prgm': [[0x5F]],
#    '2-byte': [[0x60]], Pictures
#    '2-byte': [[0x61]], GDBs
#    '2-byte': [[0x62]], Statistics
#    '2-byte': [[0x63]], Window and Finance
    'Radian': [[0x64]],
    'Degree': [[0x65]],
    'Normal': [[0x66]],
    'Sci': [[0x67]],
    'Eng': [[0x68]],
    'Float': [[0x69]],
    '=': [[0x6A]],
    '<': [[0x6B]],
    '>': [[0x6C]],
    '≤': [[0x6D]],
    '≥': [[0x6E]],
    '≠': [[0x6F]],
    '+': [[0x70]],
    '-': [[0x71]],
    'Ans': [[0x72]],
    'Fix': [[0x73]],
    'Horiz': [[0x74]],
    'Full': [[0x75]],
    'Func': [[0x76]],
    'Param': [[0x77]],
    'Polar': [[0x78]],
    'Seq': [[0x79]],
    'IndpntAuto': [[0x7A]],
    'IndpntAsk': [[0x7B]],
    'DependAuto': [[0x7C]],
    'DependAsk': [[0x7D]],
#    '2-byte': [[0x7E]], Graph Format
    '[]': [[0x7F]], # square mark TODO TODO
    '++': [[0x80], "+"], # plus mark TODO
    '⋅': [[0x81]], # product mark TODO
    '*': [[0x82]],
    '/': [[0x83]],
    'Trace': [[0x84]],
    'ClrDraw': [[0x85]],
    'ZStandard': [[0x86]],
    'ZTrig': [[0x87]],
    'ZBox': [[0x88]],
    'Zoom In': [[0x89]],
    'Zoom Out': [[0x8A]],
    'ZSquare': [[0x8B]],
    'ZInteger': [[0x8C]],
    'ZPrevious': [[0x8D]],
    'ZDecimal': [[0x8E]],
    'ZoomStat': [[0x8F]],
    'ZoomRcl': [[0x90]],
    'PrintScreen': [[0x91]],
    'ZoomSto': [[0x92]],
    'Text(': [[0x93]],
    'nPr': [[0x94]],
    'nCr': [[0x95]],
    'FnOn': [[0x96]],
    'FnOff': [[0x97]],
    'StorePic': [[0x98]],
    'RecallPic': [[0x99]],
    'StoreGDB': [[0x9A]],
    'RecallGDB': [[0x9B]],
    'Line(': [[0x9C]],
    'Vertical': [[0x9D]],
    'Pt-On(': [[0x9E]],
    'Pt-Off(': [[0x9F]],
    'Pt-Change(': [[0xA0]],
    'Pxl-On(': [[0xA1]],
    'Pxl-Off(': [[0xA2]],
    'Pxl-Change(': [[0xA3]],
    'Shade(': [[0xA4]],
    'Circle(': [[0xA5]],
    'Horizontal': [[0xA6]],
    'Tangent(': [[0xA7]],
    'DrawInv': [[0xA8]],
    'DrawF': [[0xA9]],
#    '2-byte': [[0xAA]], Strings
    'rand': [[0xAB]],
    'π_const': [[0xAC], "π"],
    'getKey': [[0xAD]],
    "'": [[0xAE]],
    '?': [[0xAF]],
    '--': [[0xB0], "-"], # negative mark TODO
    'int(': [[0xB1]],
    'abs(': [[0xB2]],
    'det(': [[0xB3]],
    'identity(': [[0xB4]],
    'dim(': [[0xB5]],
    'sum(': [[0xB6]],
    'prod(': [[0xB7]],
    'not(': [[0xB8]],
    'iPart(': [[0xB9]],
    'fPart(': [[0xBA]],
#    '2-byte': [[0xBB]], Miscellaneous
    '√(': [[0xBC]],
    '³√(': [[0xBD]],
    'ln(': [[0xBE]],
    'e^(': [[0xBF]],
    'log(': [[0xC0]],
    '10^(': [[0xC1]],
    'sin(': [[0xC2]],
    'sin⁻¹(': [[0xC3]],
    'cos(': [[0xC4]],
    'cos⁻¹(': [[0xC5]],
    'tan(': [[0xC6]],
    'tan⁻¹(': [[0xC7]],
    'sinh(': [[0xC8]],
    'sinh⁻¹(': [[0xC9]], # todo inv
    'cosh(': [[0xCA]],
    'cosh⁻¹(': [[0xCB]],
    'tanh(': [[0xCC]],
    'tanh⁻¹(': [[0xCD]],
    'If ': [[0xCE]],
    'Then': [[0xCF]],
    'Else': [[0xD0]],
    'While ': [[0xD1]],
    'Repeat ': [[0xD2]],
    'For(': [[0xD3]],
    'End': [[0xD4]],
    'Return': [[0xD5]],
    'Lbl ': [[0xD6]],
    'Goto ': [[0xD7]],
    'Pause ': [[0xD8]],
    'Stop': [[0xD9]],
    'IS>(': [[0xDA]],
    'DS<(': [[0xDB]],
    'Input ': [[0xDC]],
    'Prompt ': [[0xDD]],
    'Disp ': [[0xDE]],
    'DispGraph': [[0xDF]],
    'Output(': [[0xE0]],
    'ClrHome': [[0xE1]],
    'Fill(': [[0xE2]],
    'SortA(': [[0xE3]],
    'SortD(': [[0xE4]],
    'DispTable': [[0xE5]],
    'Menu(': [[0xE6]],
    'Send(': [[0xE7]],
    'Get(': [[0xE8]],
    'PlotsOn': [[0xE9]],
    'PlotsOff': [[0xEA]],
    '∟': [[0xEB]], # list todo
    'Plot1(': [[0xEC]],
    'Plot2(': [[0xED]],
    'Plot3(': [[0xEE]],
#    'TI-84+(C(S)E)': [[0xEF]], TI-84+
    '^': [[0xF0]],
    '×√': [[0xF1]],
    '1-Var Stats': [[0xF2]],
    '2-Var Stats': [[0xF3]],
    'LinReg(a+bx)': [[0xF4]],
    'ExpReg': [[0xF5]],
    'LnReg': [[0xF6]],
    'PwrReg': [[0xF7]],
    'Med-Med': [[0xF8]],
    'QuadReg': [[0xF9]],
    'ClrList': [[0xFA]],
    'ClrTable': [[0xFB]],
    'Histogram': [[0xFC]],
    'xyLine': [[0xFD]],
    'Scatter': [[0xFE]],
    'LinReg(ax+b)': [[0xFF]],

    # Matrices
    '[A]': [[0x5C, 0x00]],
    '[B]': [[0x5C, 0x01]],
    '[C]': [[0x5C, 0x02]],
    '[D]': [[0x5C, 0x03]],
    '[E]': [[0x5C, 0x04]],
    '[F]': [[0x5C, 0x05]],
    '[G]': [[0x5C, 0x06]],
    '[H]': [[0x5C, 0x07]],
    '[I]': [[0x5C, 0x08]],
    '[J]': [[0x5C, 0x09]],

    # Lists
    'L1': [[0x5D, 0x00]],
    'L2': [[0x5D, 0x01]],
    'L3': [[0x5D, 0x02]],
    'L4': [[0x5D, 0x03]],
    'L5': [[0x5D, 0x04]],
    'L6': [[0x5D, 0x05]],

    # Equations
    'Y1': [[0x5E, 0x10]],
    'Y2': [[0x5E, 0x11]],
    'Y3': [[0x5E, 0x12]],
    'Y4': [[0x5E, 0x13]],
    'Y5': [[0x5E, 0x14]],
    'Y6': [[0x5E, 0x15]],
    'Y7': [[0x5E, 0x16]],
    'Y8': [[0x5E, 0x17]],
    'Y9': [[0x5E, 0x18]],
    'Y0': [[0x5E, 0x19]],
    'X1T': [[0x5E, 0x20]],
    'Y1T': [[0x5E, 0x21]],
    'X2T': [[0x5E, 0x22]],
    'Y2T': [[0x5E, 0x23]],
    'X3T': [[0x5E, 0x24]],
    'Y3T': [[0x5E, 0x25]],
    'X4T': [[0x5E, 0x26]],
    'Y4T': [[0x5E, 0x27]],
    'X5T': [[0x5E, 0x28]],
    'Y5T': [[0x5E, 0x29]],
    'X6T': [[0x5E, 0x2A]],
    'Y6T': [[0x5E, 0x2B]],
    'r1': [[0x5E, 0x40]],
    'r2': [[0x5E, 0x41]],
    'r3': [[0x5E, 0x42]],
    'r4': [[0x5E, 0x43]],
    'r5': [[0x5E, 0x44]],
    'r6': [[0x5E, 0x45]],
    'u_': [[0x5E, 0x80]], # sequences todo
    'v_': [[0x5E, 0x81]],
    'w_': [[0x5E, 0x82]],

    # Pictures
    'Pic1': [[0x60, 0x00]],
    'Pic2': [[0x60, 0x01]],
    'Pic3': [[0x60, 0x02]],
    'Pic4': [[0x60, 0x03]],
    'Pic5': [[0x60, 0x04]],
    'Pic6': [[0x60, 0x05]],
    'Pic7': [[0x60, 0x06]],
    'Pic8': [[0x60, 0x07]],
    'Pic9': [[0x60, 0x08]],
    'Pic0': [[0x60, 0x09]],

    # GDBs
    'GDB1': [[0x61, 0x00]],
    'GDB2': [[0x61, 0x01]],
    'GDB3': [[0x61, 0x02]],
    'GDB4': [[0x61, 0x03]],
    'GDB5': [[0x61, 0x04]],
    'GDB6': [[0x61, 0x05]],
    'GDB7': [[0x61, 0x06]],
    'GDB8': [[0x61, 0x07]],
    'GDB9': [[0x61, 0x08]],
    'GDB0': [[0x61, 0x09]],

    # Strings
    'Str1': [[0xAA, 0x00]],
    'Str2': [[0xAA, 0x01]],
    'Str3': [[0xAA, 0x02]],
    'Str4': [[0xAA, 0x03]],
    'Str5': [[0xAA, 0x04]],
    'Str6': [[0xAA, 0x05]],
    'Str7': [[0xAA, 0x06]],
    'Str8': [[0xAA, 0x07]],
    'Str9': [[0xAA, 0x08]],
    'Str0': [[0xAA, 0x09]],

    # Statistics
#    'internal use only': [[0x62, 0x00]],
    'RegEq': [[0x62, 0x01]],
    'n_stat': [[0x62, 0x02], "n"],
    'x¯': [[0x62, 0x03]],
    'Σx': [[0x62, 0x04]],
    'Σx²': [[0x62, 0x05]],
    'Sx': [[0x62, 0x06]],
    'σx': [[0x62, 0x07]],
    'minX': [[0x62, 0x08]],
    'maxX': [[0x62, 0x09]],
    'minY': [[0x62, 0x0A]],
    'maxY': [[0x62, 0x0B]],
    'y¯': [[0x62, 0x0C]],
    'Σy': [[0x62, 0x0D]],
    'Σy²': [[0x62, 0x0E]],
    'Sy': [[0x62, 0x0F]],
    'σy': [[0x62, 0x10]],
    'Σxy': [[0x62, 0x11]],
    'r_stat': [[0x62, 0x12]],
    'Med': [[0x62, 0x13]],
    'Q1': [[0x62, 0x14]],
    'Q3': [[0x62, 0x15]],
    'a_stat': [[0x62, 0x16], "a"],
    'b_stat': [[0x62, 0x17], "b"],
    'c_stat': [[0x62, 0x18], "c"],
    'd_stat': [[0x62, 0x19], "d"],
    'e_stat': [[0x62, 0x1A], "e"],
    'x1': [[0x62, 0x1B]],
    'x2': [[0x62, 0x1C]],
    'x3': [[0x62, 0x1D]],
    'y1': [[0x62, 0x1E]],
    'y2': [[0x62, 0x1F]],
    'y3': [[0x62, 0x20]],
    'n_stat_ital': [[0x62, 0x21], "n"],
    'p_stat': [[0x62, 0x22], "p"],
    'z_stat': [[0x62, 0x23], "z"],
    't_stat': [[0x62, 0x24], "t"],
    'χ²': [[0x62, 0x25]],
    'F_stat': [[0x62, 0x26], "F"],
    'df': [[0x62, 0x27]],
    'p^': [[0x62, 0x28]],
    'p^1': [[0x62, 0x29]],
    'p^2': [[0x62, 0x2A]],
    'x¯1': [[0x62, 0x2B]],
    'Sx1': [[0x62, 0x2C]],
    'n1': [[0x62, 0x2D]],
    'x¯2': [[0x62, 0x2E]],
    'Sx2': [[0x62, 0x2F]],
    'n2': [[0x62, 0x30]],
    'Sxp': [[0x62, 0x31]],
    'lower': [[0x62, 0x32]],
    'upper': [[0x62, 0x33]],
    's_stat': [[0x62, 0x34], "s"],
    'r²': [[0x62, 0x35]],
    'R²': [[0x62, 0x36]],
    'Factor df': [[0x62, 0x37]],
    'Factor SS': [[0x62, 0x38]],
    'Factor MS': [[0x62, 0x39]],
    'Error df': [[0x62, 0x3A]],
    'Error SS': [[0x62, 0x3B]],
    'Error MS': [[0x62, 0x3C]],

    # Window and Finance
    'ZXscl': [[0x63, 0x00]],
    'ZYscl': [[0x63, 0x01]],
    'Xscl': [[0x63, 0x02]],
    'Yscl': [[0x63, 0x03]],
    'u(nMin)': [[0x63, 0x04]],
    'v(nMin)': [[0x63, 0x05]],
    'u(n-1)_wnd': [[0x63, 0x06], "u(n-1)"], # TI-82 compatibility
    'v(n-1)_wnd': [[0x63, 0x07], "v(n-1)"],
    'Zu(nMin)': [[0x63, 0x08]],
    'Zv(nMin)': [[0x63, 0x09]],
    'Xmin': [[0x63, 0x0A]],
    'Xmax': [[0x63, 0x0B]],
    'Ymin': [[0x63, 0x0C]],
    'Ymax': [[0x63, 0x0D]],
    'Tmin': [[0x63, 0x0E]],
    'Tmax': [[0x63, 0x0F]],
    'θmin': [[0x63, 0x10]],
    'θmax': [[0x63, 0x11]],
    'ZXmin': [[0x63, 0x12]],
    'ZXmax': [[0x63, 0x13]],
    'ZYmin': [[0x63, 0x14]],
    'ZYmax': [[0x63, 0x15]],
    'Zθmin': [[0x63, 0x16]],
    'Zθmax': [[0x63, 0x17]],
    'ZTmin': [[0x63, 0x18]],
    'ZTmax': [[0x63, 0x19]],
    'TblStart': [[0x63, 0x1A]],
    'PlotStart': [[0x63, 0x1B]],
    'ZPlotStart': [[0x63, 0x1C]],
    'nMax': [[0x63, 0x1D]],
    'ZnMax': [[0x63, 0x1E]],
    'nMin': [[0x63, 0x1F]],
    'ZnMin': [[0x63, 0x20]],
    'ΔTbl': [[0x63, 0x21]],
    'Tstep': [[0x63, 0x22]],
    'θstep': [[0x63, 0x23]],
    'ZTstep': [[0x63, 0x24]],
    'Zθstep': [[0x63, 0x25]],
    'ΔX': [[0x63, 0x26]],
    'ΔY': [[0x63, 0x27]],
    'XFact': [[0x63, 0x28]],
    'YFact': [[0x63, 0x29]],
    'TblInput': [[0x63, 0x2A]],
    'N_wnd': [[0x63, 0x2B], "N"],
    'I%': [[0x63, 0x2C]],
    'PV': [[0x63, 0x2D]],
    'PMT': [[0x63, 0x2E]],
    'FV': [[0x63, 0x2F]],
    'P/Y': [[0x63, 0x30]],
    'C/Y': [[0x63, 0x31]],
    'w(nMin)': [[0x63, 0x32]],
    'Zw(nMin)': [[0x63, 0x33]],
    'PlotStep': [[0x63, 0x34]],
    'ZPlotStep': [[0x63, 0x35]],
    'Xres': [[0x63, 0x36]],
    'ZXres': [[0x63, 0x37]],
    'TraceStep': [[0x63, 0x38]],

    # Graph Format
    'Sequential': [[0x7E, 0x00]],
    'Simul': [[0x7E, 0x01]],
    'PolarGC': [[0x7E, 0x02]],
    'RectGC': [[0x7E, 0x03]],
    'CoordOn': [[0x7E, 0x04]],
    'CoordOff': [[0x7E, 0x05]],
    'Connected': [[0x7E, 0x06]],
    'Dot': [[0x7E, 0x07]],
    'AxesOn': [[0x7E, 0x08]],
    'AxesOff': [[0x7E, 0x09]],
    'GridOn': [[0x7E, 0x0A]],
    'GridOff': [[0x7E, 0x0B]],
    'LabelOn': [[0x7E, 0x0C]],
    'LabelOff': [[0x7E, 0x0D]],
    'Web': [[0x7E, 0x0E]],
    'Time': [[0x7E, 0x0F]],
    'uvAxes': [[0x7E, 0x10]],
    'vwAxes': [[0x7E, 0x11]],
    'uwAxes': [[0x7E, 0x12]],

    # Miscellaneous
    'npv(': [[0xBB, 0x00]],
    'irr(': [[0xBB, 0x01]],
    'bal(': [[0xBB, 0x02]],
    'Σprn(': [[0xBB, 0x03]],
    'ΣInt(': [[0xBB, 0x04]],
    '►Nom(': [[0xBB, 0x05]],
    '►Eff(': [[0xBB, 0x06]],
    'dbd(': [[0xBB, 0x07]],
    'lcm(': [[0xBB, 0x08]],
    'gcd(': [[0xBB, 0x09]],
    'randInt(': [[0xBB, 0x0A]],
    'randBin(': [[0xBB, 0x0B]],
    'sub(': [[0xBB, 0x0C]],
    'stdDev(': [[0xBB, 0x0D]],
    'variance(': [[0xBB, 0x0E]],
    'inString(': [[0xBB, 0x0F]],
    'normalcdf(': [[0xBB, 0x10]],
    'invNorm(': [[0xBB, 0x11]],
    'tcdf(': [[0xBB, 0x12]],
    'χ²cdf(': [[0xBB, 0x13]],
    'Fcdf(': [[0xBB, 0x14]],
    'binompdf(': [[0xBB, 0x15]],
    'binomcdf(': [[0xBB, 0x16]],
    'poissonpdf(': [[0xBB, 0x17]],
    'poissoncdf(': [[0xBB, 0x18]],
    'geometpdf(': [[0xBB, 0x19]],
    'geometcdf(': [[0xBB, 0x1A]],
    'normalpdf(': [[0xBB, 0x1B]],
    'tpdf(': [[0xBB, 0x1C]],
    'χ²pdf(': [[0xBB, 0x1D]],
    'Fpdf(': [[0xBB, 0x1E]],
    'randNorm(': [[0xBB, 0x1F]],
    'tvm_Pmt': [[0xBB, 0x20]],
    'tvm_I%': [[0xBB, 0x21]],
    'tvm_PV': [[0xBB, 0x22]],
    'tvm_N': [[0xBB, 0x23]],
    'tvm_FV': [[0xBB, 0x24]],
    'conj(': [[0xBB, 0x25]],
    'real(': [[0xBB, 0x26]],
    'imag(': [[0xBB, 0x27]],
    'angle(': [[0xBB, 0x28]],
    'cumSum(': [[0xBB, 0x29]],
    'expr(': [[0xBB, 0x2A]],
    'length(': [[0xBB, 0x2B]],
    'ΔList(': [[0xBB, 0x2C]],
    'ref(': [[0xBB, 0x2D]],
    'rref(': [[0xBB, 0x2E]],
    '►Rect': [[0xBB, 0x2F]],
    '►Polar': [[0xBB, 0x30]],
    'e_const': [[0xBB, 0x31]],
    'SinReg': [[0xBB, 0x32]],
    'Logistic': [[0xBB, 0x33]],
    'LinRegTTest': [[0xBB, 0x34]],
    'ShadeNorm(': [[0xBB, 0x35]],
    'Shade_t(': [[0xBB, 0x36]],
    'Shadeχ²': [[0xBB, 0x37]],
    'ShadeF(': [[0xBB, 0x38]],
    'Matr►list(': [[0xBB, 0x39]],
    'List►matr(': [[0xBB, 0x3A]],
    'Z-Test(': [[0xBB, 0x3B]],
    'T-Test': [[0xBB, 0x3C]],
    '2-SampZTest(': [[0xBB, 0x3D]],
    '1-PropZTest(': [[0xBB, 0x3E]],
    '2-PropZTest(': [[0xBB, 0x3F]],
    'χ²-Test(': [[0xBB, 0x40]],
    'ZInterval': [[0xBB, 0x41]],
    '2-SampZInt(': [[0xBB, 0x42]],
    '1-PropZInt(': [[0xBB, 0x43]],
    '2-PropZInt(': [[0xBB, 0x44]],
    'GraphStyle(': [[0xBB, 0x45]],
    '2-SampTTest': [[0xBB, 0x46]],
    '2-SampFTest': [[0xBB, 0x47]],
    'TInterval': [[0xBB, 0x48]],
    '2-SampTInt': [[0xBB, 0x49]],
    'SetUpEditor': [[0xBB, 0x4A]],
    'Pmt_End': [[0xBB, 0x4B]],
    'Pmt_Bgn': [[0xBB, 0x4C]],
    'Real': [[0xBB, 0x4D]],
    're^θi': [[0xBB, 0x4E]],
    'a+bi': [[0xBB, 0x4F]],
    'ExprOn': [[0xBB, 0x50]],
    'ExprOff': [[0xBB, 0x51]],
    'ClrAllLists': [[0xBB, 0x52]],
    'GetCalc(': [[0xBB, 0x53]],
    'DelVar': [[0xBB, 0x54]],
    'Equ►String(': [[0xBB, 0x55]],
    'String►Equ(': [[0xBB, 0x56]],
    'Clear Entries': [[0xBB, 0x57]],
    'Select(': [[0xBB, 0x58]],
    'ANOVA(': [[0xBB, 0x59]],
    'ModBoxplot': [[0xBB, 0x5A]],
    'NormProbPlot': [[0xBB, 0x5B]],
#    'unused': [[0xBB, 0x5C]],
#    'unused': [[0xBB, 0x5D]],
#    'unused': [[0xBB, 0x5E]],
#    'unused': [[0xBB, 0x5F]],
#    'unused': [[0xBB, 0x60]],
#    'unused': [[0xBB, 0x61]],
#    'unused': [[0xBB, 0x62]],
#    'unused': [[0xBB, 0x63]],
    'G-T': [[0xBB, 0x64]],
    'ZoomFit': [[0xBB, 0x65]],
    'DiagnosticOn': [[0xBB, 0x66]],
    'DiagnosticOff': [[0xBB, 0x67]],
    'Archive': [[0xBB, 0x68]],
    'UnArchive': [[0xBB, 0x69]],
    'Asm(': [[0xBB, 0x6A]],
    'AsmComp(': [[0xBB, 0x6B]],
    'AsmPrgm': [[0xBB, 0x6C]],
    'compiled_asm': [[0xBB, 0x6D]],
    'Á': [[0xBB, 0x6E]],
    'À': [[0xBB, 0x6F]],
    'Â': [[0xBB, 0x70]],
    'Ä': [[0xBB, 0x71]],
    'á': [[0xBB, 0x72]],
    'à': [[0xBB, 0x73]],
    'â': [[0xBB, 0x74]],
    'ä': [[0xBB, 0x75]],
    'É': [[0xBB, 0x76]],
    'È': [[0xBB, 0x77]],
    'Ê': [[0xBB, 0x78]],
    'Ë': [[0xBB, 0x79]],
    'é': [[0xBB, 0x7A]],
    'è': [[0xBB, 0x7B]],
    'ê': [[0xBB, 0x7C]],
    'ë': [[0xBB, 0x7D]],
#    'unused': [[0xBB, 0x7E]],
    'Ì': [[0xBB, 0x7F]],
    'Î': [[0xBB, 0x80]],
    'Ï': [[0xBB, 0x81]],
    'í': [[0xBB, 0x82]],
    'ì': [[0xBB, 0x83]],
    'î': [[0xBB, 0x84]],
    'ï': [[0xBB, 0x85]],
    'Ó': [[0xBB, 0x86]],
    'Ò': [[0xBB, 0x87]],
    'Ô': [[0xBB, 0x88]],
    'Ö': [[0xBB, 0x89]],
    'ó': [[0xBB, 0x8A]],
    'ò': [[0xBB, 0x8B]],
    'ô': [[0xBB, 0x8C]],
    'ö': [[0xBB, 0x8D]],
    'Ú': [[0xBB, 0x8E]],
    'Ù': [[0xBB, 0x8F]],
    'Û': [[0xBB, 0x90]],
    'Ü': [[0xBB, 0x91]],
    'ú': [[0xBB, 0x92]],
    'ù': [[0xBB, 0x93]],
    'û': [[0xBB, 0x94]],
    'ü': [[0xBB, 0x95]],
    'Ç': [[0xBB, 0x96]],
    'ç': [[0xBB, 0x97]],
    'Ñ': [[0xBB, 0x98]],
    'ñ': [[0xBB, 0x99]],
    '´': [[0xBB, 0x9A]],
    '`': [[0xBB, 0x9B]],
    '¨': [[0xBB, 0x9C]],
    '¿': [[0xBB, 0x9D]],
    '¡': [[0xBB, 0x9E]],
    'α': [[0xBB, 0x9F]],
    'β': [[0xBB, 0xA0]],
    'γ': [[0xBB, 0xA1]],
    'Δ': [[0xBB, 0xA2]],
    'δ': [[0xBB, 0xA3]],
    'ε': [[0xBB, 0xA4]],
    'λ': [[0xBB, 0xA5]],
    'μ': [[0xBB, 0xA6]],
    'π': [[0xBB, 0xA7]],
    'ρ': [[0xBB, 0xA8]],
    'Σ': [[0xBB, 0xA9]],
#    'unused': [[0xBB, 0xAA]],
    'φ': [[0xBB, 0xAB]],
    'Ω': [[0xBB, 0xAC]],
    'p^_sym': [[0xBB, 0xAD]],
    'χ': [[0xBB, 0xAE]],
    'F_sym': [[0xBB, 0xAF]],
    'a': [[0xBB, 0xB0]],
    'b': [[0xBB, 0xB1]],
    'c': [[0xBB, 0xB2]],
    'd': [[0xBB, 0xB3]],
    'e': [[0xBB, 0xB4]],
    'f': [[0xBB, 0xB5]],
    'g': [[0xBB, 0xB6]],
    'h': [[0xBB, 0xB7]],
    'i': [[0xBB, 0xB8]],
    'j': [[0xBB, 0xB9]],
    'k': [[0xBB, 0xBA]],
#    'unused': [[0xBB, 0xBB]],
    'l': [[0xBB, 0xBC]],
    'm': [[0xBB, 0xBD]],
    'n': [[0xBB, 0xBE]],
    'o': [[0xBB, 0xBF]],
    'p': [[0xBB, 0xC0]],
    'q': [[0xBB, 0xC1]],
    'r': [[0xBB, 0xC2]],
    's': [[0xBB, 0xC3]],
    't': [[0xBB, 0xC4]],
    'u': [[0xBB, 0xC5]],
    'v': [[0xBB, 0xC6]],
    'w': [[0xBB, 0xC7]],
    'x': [[0xBB, 0xC8]],
    'y': [[0xBB, 0xC9]],
    'z': [[0xBB, 0xCA]],
    'σ': [[0xBB, 0xCB]],
    'τ': [[0xBB, 0xCC]],
    'Í': [[0xBB, 0xCD]],
    'GarbageCollect': [[0xBB, 0xCE]],
    '~': [[0xBB, 0xCF]],
    'reserved': [[0xBB, 0xD0]],
    '@': [[0xBB, 0xD1]],
    '#': [[0xBB, 0xD2]],
    '$': [[0xBB, 0xD3]],
    '&': [[0xBB, 0xD4]],
    '`_other': [[0xBB, 0xD5]],
    ';': [[0xBB, 0xD6]],
    '\\': [[0xBB, 0xD7]],
    '|': [[0xBB, 0xD8]],
    '_': [[0xBB, 0xD9]],
    '%': [[0xBB, 0xDA]],
    '…': [[0xBB, 0xDB]],
    '∠': [[0xBB, 0xDC]],
    'ß': [[0xBB, 0xDD]],
    'x_exp': [[0xBB, 0xDE]],
    'T_sub': [[0xBB, 0xDF]],
    '0_sub': [[0xBB, 0xE0]],
    '1_sub': [[0xBB, 0xE1]],
    '2_sub': [[0xBB, 0xE2]],
    '3_sub': [[0xBB, 0xE3]],
    '4_sub': [[0xBB, 0xE4]],
    '5_sub': [[0xBB, 0xE5]],
    '6_sub': [[0xBB, 0xE6]],
    '7_sub': [[0xBB, 0xE7]],
    '8_sub': [[0xBB, 0xE8]],
    '9_sub': [[0xBB, 0xE9]],
    '10_sub': [[0xBB, 0xEA]],
    '←_arr': [[0xBB, 0xEB]],
    '→_arr': [[0xBB, 0xEC]],
    '↑_arr': [[0xBB, 0xED]],
    '↓_arr': [[0xBB, 0xEE]],
#    'unused': [[0xBB, 0xEF]],
    'x_sym': [[0xBB, 0xF0]],
    '∫': [[0xBB, 0xF1]],
    '↑_sym': [[0xBB, 0xF2]],
    '↓_sym': [[0xBB, 0xF3]],
    '√': [[0xBB, 0xF4]],
    '[=]': [[0xBB, 0xF5]],
#    '': [[0xBB, 0xF6]],
#    '': [[0xBB, 0xF7]],
#    '': [[0xBB, 0xF8]],
#    '': [[0xBB, 0xF9]],
#    '': [[0xBB, 0xFA]],
#    '': [[0xBB, 0xFB]],
#    '': [[0xBB, 0xFC]],
#    '': [[0xBB, 0xFD]],
#    '': [[0xBB, 0xFE]],
#    '': [[0xBB, 0xFF]],

    # TI-84+
    'setDate(': [[0xEF, 0x00]],
    'setTime(': [[0xEF, 0x01]],
    'checkTmr(': [[0xEF, 0x02]],
    'setDtFmt(': [[0xEF, 0x03]],
    'setTmFmt(': [[0xEF, 0x04]],
    'timeCnv(': [[0xEF, 0x05]],
    'dayOfWk(': [[0xEF, 0x06]],
    'getDtStr': [[0xEF, 0x07]],
    'getTmStr(': [[0xEF, 0x08]],
    'getDate': [[0xEF, 0x09]],
    'getTime': [[0xEF, 0x0A]],
    'startTmr': [[0xEF, 0x0B]],
    'getDtFmt': [[0xEF, 0x0C]],
    'getTmFmt': [[0xEF, 0x0D]],
    'isClockOn': [[0xEF, 0x0E]],
    'ClockOff': [[0xEF, 0x0F]],
    'ClockOn': [[0xEF, 0x10]],
    'OpenLib(': [[0xEF, 0x11]],
    'ExecLib': [[0xEF, 0x12]],
    'invT(': [[0xEF, 0x13]],
    'χ²GOF-Test(': [[0xEF, 0x14]],
    'LinRegTInt': [[0xEF, 0x15]],
    'Manual-Fit': [[0xEF, 0x16]],
    'ZQuadrant1': [[0xEF, 0x17]],
    'ZFrac1/2': [[0xEF, 0x18]],
    'ZFrac1/3': [[0xEF, 0x19]],
    'ZFrac1/4': [[0xEF, 0x1A]],
    'ZFrac1/5': [[0xEF, 0x1B]],
    'ZFrac1/8': [[0xEF, 0x1C]],
    'ZFrac1/10': [[0xEF, 0x1D]],
    'mathprintbox': [[0xEF, 0x1E]],
#    '': [[0xEF, 0x1F]],
#    '': [[0xEF, 0x20]],
#    '': [[0xEF, 0x21]],
#    '': [[0xEF, 0x22]],
#    '': [[0xEF, 0x23]],
#    '': [[0xEF, 0x24]],
#    '': [[0xEF, 0x25]],
#    '': [[0xEF, 0x26]],
#    '': [[0xEF, 0x27]],
#    '': [[0xEF, 0x28]],
#    '': [[0xEF, 0x29]],
#    '': [[0xEF, 0x2A]],
#    '': [[0xEF, 0x2B]],
#    '': [[0xEF, 0x2C]],
#    '': [[0xEF, 0x2D]],
#    '': [[0xEF, 0x2E]],
#    '': [[0xEF, 0x2F]],
    '►n/d◄►Un/d': [[0xEF, 0x30]],
    '►F◄►D': [[0xEF, 0x31]],
    'remainder(': [[0xEF, 0x32]],
    'Σ(': [[0xEF, 0x33]],
    'logBASE(': [[0xEF, 0x34]],
    'randIntNoRep(': [[0xEF, 0x35]],
    'MATHPRINT': [[0xEF, 0x36]],
    'CLASSIC': [[0xEF, 0x37]],
    'n/d': [[0xEF, 0x38]],
    'Un/d': [[0xEF, 0x39]],
    'AUTO': [[0xEF, 0x3A]],
    'DEC': [[0xEF, 0x3B]],
    'FRAC': [[0xEF, 0x3C]],
    'FRAC-APPROX': [[0xEF, 0x3D]],
#    '': [[0xEF, 0x3E]],
#    '': [[0xEF, 0x3F]],
#    '': [[0xEF, 0x40]],
    'BLUE': [[0xEF, 0x41]],
    'RED': [[0xEF, 0x42]],
    'BLACK': [[0xEF, 0x43]],
    'MAGENTA': [[0xEF, 0x44]],
    'GREEN': [[0xEF, 0x45]],
    'ORANGE': [[0xEF, 0x46]],
    'BROWN': [[0xEF, 0x47]],
    'NAVY': [[0xEF, 0x48]],
    'LTBLUE': [[0xEF, 0x49]],
    'YELLOW': [[0xEF, 0x4A]],
    'WHITE': [[0xEF, 0x4B]],
    'LTGREY': [[0xEF, 0x4C]],
    'MEDGREY': [[0xEF, 0x4D]],
    'GREY': [[0xEF, 0x4E]],
    'DARKGREY': [[0xEF, 0x4F]],
    'Image1': [[0xEF, 0x50]],
    'Image2': [[0xEF, 0x51]],
    'Image3': [[0xEF, 0x52]],
    'Image4': [[0xEF, 0x53]],
    'Image5': [[0xEF, 0x54]],
    'Image6': [[0xEF, 0x55]],
    'Image7': [[0xEF, 0x56]],
    'Image8': [[0xEF, 0x57]],
    'Image9': [[0xEF, 0x58]],
    'Image0': [[0xEF, 0x59]],
    'Gridline': [[0xEF, 0x5A]],
    'BackgroundOn': [[0xEF, 0x5B]],
#    '': [[0xEF, 0x5C]],
#    '': [[0xEF, 0x5D]],
#    '': [[0xEF, 0x5E]],
#    '': [[0xEF, 0x5F]],
#    '': [[0xEF, 0x60]],
#    '': [[0xEF, 0x61]],
#    '': [[0xEF, 0x62]],
#    '': [[0xEF, 0x63]],
    'BackgroundOff': [[0xEF, 0x64]],
    'GraphColor(': [[0xEF, 0x65]],
#    '': [[0xEF, 0x66]],
    'TextColor(': [[0xEF, 0x67]],
    'Asm84CPrgm': [[0xEF, 0x68]],
#    '': [[0xEF, 0x69]],
    'DetectAsymOn': [[0xEF, 0x6A]],
    'DetectAsymOff': [[0xEF, 0x6B]],
    'BorderColor': [[0xEF, 0x6C]],
#    '': [[0xEF, 0x6D]],
#    '': [[0xEF, 0x6E]],
#    '': [[0xEF, 0x6F]],
#    '': [[0xEF, 0x70]],
#    '': [[0xEF, 0x71]],
#    '': [[0xEF, 0x72]],
    'tinydotplot': [[0xEF, 0x73]],
    'Thin': [[0xEF, 0x74]],
    'Dot-Thin': [[0xEF, 0x75]],
#    '': [[0xEF, 0x76]],
#    '': [[0xEF, 0x77]],
#    '': [[0xEF, 0x78]],
    'PlySmth2': [[0xEF, 0x79]],
    'Asm84CEPrgm': [[0xEF, 0x7A]],
#    '': [[0xEF, 0x7B]],
#    '': [[0xEF, 0x7C]],
#    '': [[0xEF, 0x7D]],
#    '': [[0xEF, 0x7E]],
#    '': [[0xEF, 0x7F]],
#    '': [[0xEF, 0x80]],
    'QuartilesSetting…': [[0xEF, 0x81]],
    'u(n-2)': [[0xEF, 0x82]],
    'v(n-2)': [[0xEF, 0x83]],
    'w(n-2)': [[0xEF, 0x84]],
    'u(n-1)': [[0xEF, 0x85]],
    'v(n-1)': [[0xEF, 0x86]],
    'w(n-1)': [[0xEF, 0x87]],
    'u(n)': [[0xEF, 0x88]],
    'v(n)': [[0xEF, 0x89]],
    'w(n)': [[0xEF, 0x8A]],
    'u(n+1)': [[0xEF, 0x8B]],
    'v(n+1)': [[0xEF, 0x8C]],
    'w(n+1)': [[0xEF, 0x8D]],
    'pieceWise(': [[0xEF, 0x8E]],
    'SEQ(n)': [[0xEF, 0x8F]],
    'SEQ(n+1)': [[0xEF, 0x90]],
    'SEQ(n+2)': [[0xEF, 0x91]],
    'LEFT': [[0xEF, 0x92]],
    'CENTER': [[0xEF, 0x93]],
    'RIGHT': [[0xEF, 0x94]],
    'invBinom(': [[0xEF, 0x95]],
    'Wait ': [[0xEF, 0x96]],
    'toString(': [[0xEF, 0x97]],
    'eval': [[0xEF, 0x98]],
#    '': [[0xEF, 0x99]],
#    '': [[0xEF, 0x9A]],
#    '': [[0xEF, 0x9B]],
#    '': [[0xEF, 0x9C]],
#    '': [[0xEF, 0x9D]],
#    '': [[0xEF, 0x9E]],
#    '': [[0xEF, 0x9F]],
}

def linify(lst):
    if lst:
        return lst + ["\n"]

    return []

def paren(lst):
    return ["("] + lst + [")"]

def listjoin(args, sep):
    res = []

    for a in args:
        res.extend(a)
        res.append(sep)

    if res:
        res = res[:-1]

    return res

def convert_color(node):
    colors = [
        'BLUE',
        'RED',
        'BLACK',
        'MAGENTA',
        'GREEN',
        'ORANGE',
        'BROWN'
        'NAVY',
        'LTBLUE',
        'YELLOW',
        'WHITE',
        'LTGREY',
        'MEDGREY',
        'GREY',
        'DARKGREY',
    ]

    if isinstance(node, StringNode):
        fix = node.value.upper().strip()
        if fix in colors:
            return fix

    return "BLUE"


def convert_node(node):
    if isinstance(node, StringNode):
        return ['"'] + list(node.value) + ['"']

    if isinstance(node, NumberNode):
        return lstreplace(lstreplace(list(str(node.value)), "e", "EE"), "-", "--")

    if isinstance(node, IdentifierNode):
        return list(node.value.upper())

    if isinstance(node, ListNode):
        return ["{"] + listjoin((convert_node(a) for a in node.value), ",") + ["}"]

    if isinstance(node, UnaryOpNode):
        table = {
            "NOT": ["not("],
            "-": ["--", "("],
        }
        return table[node.operator] + [convert_node(node.value), ")"]

    if isinstance(node, BinOpNode):
        table = {
            "^": "",
            "**": "",
            "<=": "≤",
            ">=": "≥",
            "==": "=",
            "!=": "≠",
            "&": " and ",
            "|": " or ",
            "XOR": " xor "
        }

        ftable = {
            "%": "remainder("
        }

        left = convert_node(node.left)
        right = convert_node(node.right)

        if node.operator.upper() in ftable:
            return [ftable[node.operator.upper()]] + left + [","] + right + [")"]

        if node.need_fix(node.left):
            left = paren(left)

        if node.need_fix(node.right, True):
            right = paren(right)

        return left + [table.get(node.operator.upper(), node.operator)] + right

    if isinstance(node, ArrayAccessNode):
        return ["∟"] + convert_node(node.array) + ["("] + convert_node(node.index) + [")"]

    if isinstance(node, CallNode):
        return convert_node(node.func) + ["("] + listjoin((convert_node(a) for a in node.args), ",") + [")"]

    print("unimpl node %s" % type(node))

def convert_block(block):
    return [tok for a, b in pairwise(block) for tok in convert_stmt(a, b)]

def convert_stmt(stmt, next=None):
    if isinstance(stmt, AssignStmt):
        return convert_node(stmt.value) + ["→"] + convert_node(stmt.variable)

    if isinstance(stmt, InputStmt):
        res = ["Input "]

        if stmt.prompt is not None:
            res.extend(convert_node(stmt.prompt))
            res.append(",")

        res.extend(convert_node(stmt.variable))
        return res

    if isinstance(stmt, DisplayStmt):
        return ["Disp "] + convert_node(stmt.content)

    if isinstance(stmt, StopStmt):
        return ["Pause "] + (convert_node(stmt.message) if stmt.message is not None else [])

    if isinstance(stmt, SleepStmt):
        return ["Wait "] + convert_node(stmt.duration)

    if isinstance(stmt, ForStmt):
        res = ["For("] + list(stmt.variable.upper()) + [","] + convert_node(stmt.begin) + [","] + convert_node(stmt.end)

        if stmt.step is not None:
            res.append(",")
            res.extend(convert_node(stmt.step))

        res.append(")")
        res.append("\n")

        for line, n in pairwise(stmt.children):
            res.extend(linify(convert_stmt(line, n)))

        res.append("End")
        return res

    if isinstance(stmt, WhileStmt):
        res = ["While "] + convert_node(stmt.condition) + ["\n"]

        for line, n in pairwise(stmt.children):
            res.extend(linify(convert_stmt(line, n)))

        res.append("End")
        return res

    if isinstance(stmt, IfStmt):
        res = ["If "] + convert_node(stmt.condition) + ["\n", "Then", "\n"]

        for line, n in pairwise(stmt.children):
            res.extend(linify(convert_stmt(line, n)))

        if isinstance(next, ElseStmt):
            res.append("Else")
            res.append("\n")

            for line, n in pairwise(next.children):
                res.extend(linify(convert_stmt(line, n)))

        res.append("End")
        return res

    if isinstance(stmt, ElseStmt):
        return []

    if isinstance(stmt, CommentStmt):
        return ['"'] + list(stmt.content)

    if isinstance(stmt, GClearStmt):
        return ["ClrDraw"]

    if isinstance(stmt, GWindowStmt):
        return convert_node(stmt.x_min) + ["→", "Xmin", ":"] + \
               convert_node(stmt.x_max) + ["→", "Xmax", ":"] + \
               convert_node(stmt.y_min) + ["→", "Ymin", ":"] + \
               convert_node(stmt.y_max) + ["→", "Ymax"]

    if isinstance(stmt, GLineStmt):
        return ["Line("] + \
               convert_node(stmt.start_x) + [","] + \
               convert_node(stmt.start_y) + [","] + \
               convert_node(stmt.end_x) + [","] + \
               convert_node(stmt.end_y) + [","] + \
               convert_color(stmt.color) + [")"]

    if isinstance(stmt, GPointStmt):
        return ["Pt-On("] + \
               convert_node(stmt.x) + [","] + \
               convert_node(stmt.y) + [")"]

    if isinstance(stmt, CallStmt):
        return convert_node(stmt.function) + ["("] + listjoin((convert_node(a) for a in stmt.arguments), ",") + [")"]

    print("unimpl stmt %s" % type(stmt))

def stringify(toklst):
    res = ""

    if toklst:
        for tok in toklst:
            if len(tokens[tok]) == 2:
                res += tokens[tok][1]
            else:
                res += tok

    return res

algo = [
    ForStmt("i", parse("1"), parse("16"), [
        IfStmt(parse("i % 15 == 0"), [
            DisplayStmt(parse("\"FizzBuzz\""))
        ]),
        ElseStmt([
            IfStmt(parse("i % 3 == 0"), [
                DisplayStmt(parse("\"Fizz\""))
            ]),
            ElseStmt([
                IfStmt(parse("i % 5 == 0"), [
                    DisplayStmt(parse("\"Buzz\""))
                ]),
                ElseStmt([
                    DisplayStmt(parse("i"))
                ])
            ])
        ]),
    ])
        ]

print(stringify(convert_block(algo)))

