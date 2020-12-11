from math import log10, pi
import numpy as np

def calc_sv(P_c, alpha, pt, sound_vel, wavelen, transducer_gain, sample_interval, eq_beam_angle, pulse_length, sa_corr):
    '''Converting raw power to s_v using Type 3 definition from the NetCDF standard'''
    # capitalized variables are vectors, lower case are scalars
    TVG_CORRECTION = 2 # Receiver delay.

    gain = pt * wavelen**2 / (16*pi**2)
    pulse_duration = pulse_length * 10**(2*sa_corr/10)

    P_received = 10 * log10(2)/256 * P_c  # is this really correct?  Matches Rick exactly
    print('P_r:', P_received[:50])

    n = P_received.shape[0]
    Rng = np.zeros(n)
    Rng[TVG_CORRECTION:] = np.linspace(start = 0,stop = n * sound_vel/2 * sample_interval, num=n-TVG_CORRECTION)
    print('Rng:', Rng[:50])   # Ricks start with two extra zeros.  Due to receiver delay (line 1563, EK60.py)? And valuers are roughly 0.2% lower...

    Beam_expansion = np.maximum(np.zeros(n), 20 * np.log10(Rng))  # this is the same as time varied gain, TVG.  Rick only uses positive values.
    print('Beam_exp:', Beam_expansion[:50])   # this matches well with range, is -Inf when Rng is 0

    Absorption = 2*alpha*Rng
    print('Absorption:', Absorption[:50])

    # TS = P_received + 2*Beam_expansion + Absorption - 10*log10(gain) - 2*transducer_gain
    sv = P_received + Beam_expansion + Absorption - 10*log10 (gain * sound_vel * 10**(eq_beam_angle/10) * pulse_duration /2) - 2*transducer_gain
    return(sv)
