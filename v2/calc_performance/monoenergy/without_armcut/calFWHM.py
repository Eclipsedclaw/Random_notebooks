#!/usr/bin/env python
# coding: UTF-8

import ROOT
import numpy as np

def _getFWHMhist(hist, maximumbin, maximumbincontent):
    bincenter_low = [0, 0]
    bincontent_low = [0, 0]
    for ibin in range(maximumbin, 0, -1):
        bincontent = hist.GetBinContent(ibin)
        if bincontent > 0.5 * maximumbincontent:
            bincenter_low[0] = hist.GetBinCenter(ibin)
            bincontent_low[0] = np.abs(bincontent - 0.5 * maximumbincontent)
        else:
            bincenter_low[1] = hist.GetBinCenter(ibin)
            bincontent_low[1] = np.abs(bincontent - 0.5 * maximumbincontent)
            break

    low_end = (bincenter_low[0] * bincontent_low[1] + bincenter_low[1] * bincontent_low[0]) / (bincontent_low[0] + bincontent_low[1])

    bincenter_upper = [0, 0]
    bincontent_upper = [0, 0]
    for ibin in range(maximumbin, hist.GetNbinsX() + 1, 1):
        bincontent = hist.GetBinContent(ibin)
        if bincontent > 0.5 * maximumbincontent:
            bincenter_upper[0] = hist.GetBinCenter(ibin)
            bincontent_upper[0] = np.abs(bincontent - 0.5 * maximumbincontent)
        else:
            bincenter_upper[1] = hist.GetBinCenter(ibin);
            bincontent_upper[1] = np.abs(bincontent - 0.5 * maximumbincontent)
            break

    upper_end = (bincenter_upper[0] * bincontent_upper[1] + bincenter_upper[1] * bincontent_upper[0]) / (bincontent_upper[0] + bincontent_upper[1])

    return upper_end - low_end;

def getFWHMhist(hist):
    maximumbin = hist.GetMaximumBin()
    maximumbincontent = hist.GetBinContent(maximumbin)
    return _getFWHMhist(hist, maximumbin, maximumbincontent)
