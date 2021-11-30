#!/usr/bin/python3
# Copyright © 2021 Pim Nelissen.
# This software is licensed under the MIT license.
# Read more at https://mit-license.org/.

from matplotlib import pyplot as plt
import numpy as np
import pandas

FILE_PATH = 'data/rlc_data.csv'
INDUCTANCE_VALUE = 100*10**-9 # Value for L given by instruction manual.

def parse_data(df, i):
    header_index = df[df['Name']=='Frequency [Hz]'].index[0]
    split_data = df[df.index > header_index]
    split_data.columns = df.iloc[header_index]

    to_float = lambda x: float(x.replace(',','.'))

    freq_list = [to_float(x) for x in split_data['Frequency [Hz]'].tolist()]
    gain_list = [to_float(x) for x in split_data['Magnitude [dBm]'].tolist()]

    return freq_list[i:], gain_list[i:]

def norm_scatter(data, size=10, alpha=1):
    '''
    Converts gain measurements from dBm (decibel milliwatts) to Watts,
    using the formula Gain (Watt) = 10^(sigma/10). Then, these values are
    normalized, that is, Gain (Normalized) = Gain / max(Gain). Finally
    a scatter plot of these normalized datapoints is generated.
    '''
    freq, gain_dbm = data
    gain = [10**(sigma/10) for sigma in gain_dbm]
    max_gain = max(gain)
    normalized_gain = [gain/max_gain for gain in gain]
    plt.scatter(freq, normalized_gain, s=size, alpha=alpha,
                label='Normalized gain datapoints', c='grey')

def g(sigma, R, L, C):
    return 1/np.sqrt(1 + ((1/R**2) * (1/(sigma*C) - (L*sigma))**2))

def lorentz_fit(data, params):
    '''
    Using formula 2.100 from Franklin's Mathematical Methods for Oscillations
    and Waves [2020], a plot of g(sigma) is generated using user defined
    parameters, which are guesses for resistance R and capacitance C of the
    RLC circuit. The inductance L was given in the instruction manual.
    '''
    freq = data[0]
    R, L, C = params.values()
    plt.plot(freq,
             [g(np.pi*2*sigma, R, L, C) for sigma in freq],
             label='Lorentzian g(σ)',
             color='green')

# Import CSV and parse the data to a tuple of lists.
dataframe = pandas.read_csv(FILE_PATH, delimiter=';')
data = parse_data(dataframe, 4)

norm_scatter(data, size=1, alpha=0.5)

# Parameters for g(sigma), where R is in ohm, L in Henry, and C in Farad.
params = {'R': 40, 'L': INDUCTANCE_VALUE, 'C': (2.27*10**-12)}
lorentz_fit(data, params)

# Plot settings & Show plot
plt.xlabel('Frequency [Hz]')
plt.ylabel('Normalized Gain')
plt.legend()
plt.show()
