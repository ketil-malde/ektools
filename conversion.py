from math import log10, pi
import numpy as np

def calc_sv(P_c, alpha, pt, sound_vel, wavelen, transducer_gain, sample_interval, eq_beam_angle, pulse_length, sa_corr):
    '''Converting EK60 raw power to s_v using Type 3 definition from the NetCDF standard'''
    # capitalized variables are vectors, lower case are scalars
    TVG_CORRECTION = 2 # Receiver delay, from pyEcholab

    # factor used to calculate TVG, reduction of the signal as it expands in area as range increases
    gain = pt * wavelen**2 / (16*pi**2)

    # the effective pulse lenght needs to be adjusted by sa_correction
    pulse_duration = pulse_length * 10**(2*sa_corr/10)

    # EK60 stores received signal as fixpoint log2 values
    P_received = 10 * log10(2)/256 * P_c 

    # Range is sample interval times the speed of sound.  In pyEcholab, it starts with two extra zeros, due to "receiver delay" (line 1563, EK60.py).
    # After this shift, the values are still slightly higher than pyEcholab.
    # this? c_range -= (2.0 * power_data.sample_thickness) <- if TVG-correction

    # https://support.echoview.com/WebHelp/Reference/Algorithms/Echosounder/Simrad/Simrad_Time_Varied_Gain_Range_Correction.htm#Ex60
    # range <- r - c*tau/4, where c = sound_vel, and tau is transmitted pulse length in seconds.  1475*0.001 ~ 1.5m/4 = 0.375m
    # sample interval is typically 1/4 tau, so...this should mean one initial zero?
    n = P_received.shape[0]
    thickness = sound_vel/2 * sample_interval
    Rng = np.zeros(n)
    Rng[TVG_CORRECTION:] = np.linspace(start = 0,stop = (n-TVG_CORRECTION) * sound_vel/2 * sample_interval, num=n-TVG_CORRECTION)

    # TVG.  Set any negative values to zero.  
    TVG = np.maximum(np.zeros(n), 20 * np.log10(Rng))

    Absorption = 2*alpha*Rng
    print('Absorption:', Absorption[:50])

    # TS = P_received + 2*TVG + Absorption - 10*log10(gain) - 2*transducer_gain
    Sv = P_received + TVG + Absorption - 10*log10 (gain * sound_vel * 10**(eq_beam_angle/10) * pulse_duration /2) - 2*transducer_gain
    sv = 10**(Sv/10)
    return(sv)


def calc_angles():
    '''Convert angles as returned by EK60 to standard angles.'''
    return None
