import pywt
import numpy as np
import matplotlib.pyplot as plt

def stack(chan_list, coef):
    return np.stack([chan_list[i][coef] for i in range(3)], axis = -1)

def apply_filter(image, kind="coif17"):
    chan_3 = []
    for i in range(3):
        coeffs2 = pywt.dwt2(image[:,:,i], kind)
        ll, (lh, hl, hh) = coeffs2
        plt.imshow(ll)
        plt.show()
        chan_3.append((ll, lh, hl, hh))
    LL = stack(chan_3, 0)
    LH = stack(chan_3, 1)
    HL = stack(chan_3, 2)
    HH = stack(chan_3, 3)
    return LL, LH, HL, HH



