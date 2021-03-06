# -*- coding: utf-8 -*-
"""5275_Lab2_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EJ4CLqJDUJmyvVRf0RWiMN27b-rapl1y
"""

!pip install -U mne

from matplotlib import pyplot as plt
import numpy as np
import time, mne

######### Modify BASE_DIR before run this program, 
#     path of sXD_5678.set should be "BASE_DIR/sXD_5678.set"
BASE_DIR = "/content/drive/MyDrive/5275_Lab2_2/"

raw = mne.io.read_raw_eeglab(BASE_DIR + "sXD_5678.set")
#print(raw.info)
mne.rename_channels(raw.info, mapping = 
    {"FP1": "Fp1", "FP2": "Fp2", 
    "PZ": "Pz", "FZ": "Fz", "CZ": "Cz", 
    "FCZ": "FCz", "CPZ": "CPz", "OZ": "Oz"})
print(raw.ch_names)

"""Problem 6"""

## Problem 6
eeg = raw.copy()
#eeg.drop_channels(["vehicle positio"])
# plot 2D channel location map
montage_1020 = mne.channels.make_standard_montage("standard_1020")
eeg.set_montage(montage_1020, on_missing = "warn")
eeg.get_montage().plot()
# re-reference data by (A1+A2)/2
refchan = ["A1", "A2"]
mne.set_eeg_reference(eeg, ref_channels = refchan)
# Down-sampling to 250Hz
eeg = eeg.resample(250)
# drop A1,A2
eeg = eeg.drop_channels(refchan)
# Run ICA
ica = mne.preprocessing.ICA(n_components = len(eeg.ch_names))
ica.fit(eeg)
# plot component map
ica.plot_components()

# denoising by ICA
reconstruct = eeg.copy()
ica.exclude = [0, 2, 3, 7, 8, 11]
ica.apply(reconstruct)

# plot the eeg signal
print("=> original EEG signal")
fig1 = eeg.plot(duration = 10.0, n_channels = 33)
print("=> EEG signal after ICA")
fig2 = reconstruct.plot(duration = 10.0, n_channels = 33)

"""Problem 7"""

## Problem 7
eeg2 = raw.copy()
eeg2.drop_channels(["vehicle positio"])
# plot 2D channel location map
montage_1020 = mne.channels.make_standard_montage("standard_1020")
eeg2.set_montage(montage_1020, on_missing = "warn")
eeg2.get_montage().plot()
# re-reference data by (A1+A2)/2
refchan = ["A1", "A2"]
mne.set_eeg_reference(eeg2, ref_channels = refchan)
# Down-sampling to 250Hz
eeg2 = eeg2.resample(250)
# Bandpass filtering [1,50] Hz
eeg2 = eeg2.filter(1.0, 50.0, filter_length = 826)
# drop A1,A2
eeg2 = eeg2.drop_channels(refchan)
# Run ICA
ica = mne.preprocessing.ICA(n_components = len(eeg2.ch_names))
ica.fit(eeg2)
# plot component map
ica.plot_components()

# denoising by ICA
reconstruct2 = eeg2.copy()
ica.exclude = [0, 1, 10, 23, 24]
ica.apply(reconstruct2)

# plot the eeg signal
print("=> original EEG signal")
fig1 = eeg2.plot(duration = 10.0, n_channels = 33)
print("=> EEG signal after ICA")
fig2 = reconstruct2.plot(duration = 10.0, n_channels = 33)

"""Problem 8"""

## Problem 8
eeg3 = raw.copy()
eeg3.drop_channels(["vehicle positio", "A1", "A2"])
# plot 2D channel location map
montage_1020 = mne.channels.make_standard_montage("standard_1020")
eeg3.set_montage(montage_1020, on_missing = "warn")
eeg3.get_montage().plot()
# re-reference data by avg
mne.set_eeg_reference(eeg3, ref_channels = "average")
# Down-sampling to 250Hz
eeg3 = eeg3.resample(250)
# Bandpass filtering [1,50] Hz
eeg3 = eeg3.filter(1.0, 50.0, filter_length = 826)
ica = mne.preprocessing.ICA(n_components = len(eeg3.ch_names))
ica.fit(eeg3)
# plot component map
ica.plot_components()

# denoising by ICA
reconstruct3 = eeg3.copy()
# detect_artifact() automatic pick bad components
ica_clean = ica.detect_artifacts(eeg3)
ica_clean.apply(reconstruct3)

# plot the eeg signal
print("=> original EEG signal")
fig1 = eeg3.plot(duration = 10.0, n_channels = 33)
print("=> EEG signal after ICA")
fig2 = reconstruct3.plot(duration = 10.0, n_channels = 33)