import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter, filtfilt

SAMPLE_RATE = 1000                                                              #sample frequency (Hz) (atleast 2x the highest frequency in the signal or else -> aliasing
DURATION = 5                                                                    #period analising(s)

T_SAMPLE = 1/SAMPLE_RATE                                                        #time between samples

N = SAMPLE_RATE * DURATION                                                      #number of samples

def sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)        #sine wave generator function
    y = np.sin((2 * np.pi) * x * freq)                                          
    return x, y

#gerar funções sinusoidais
_, yk1 =   sine_wave(100, SAMPLE_RATE, DURATION)  #100Hz
_, yk2 =   sine_wave(150, SAMPLE_RATE, DURATION)  #150Hz                      
_, yk3 =   sine_wave(200, SAMPLE_RATE, DURATION)  #200Hz
_, yk4 =   sine_wave(250, SAMPLE_RATE, DURATION)  #250Hz
_, yk5 =   sine_wave(300, SAMPLE_RATE, DURATION)  #300Hz
_, yk6 =   sine_wave(350, SAMPLE_RATE, DURATION)  #350Hz
    
yk = yk1 + yk2 + yk3 + yk4 + yk5                                                #sum of all components

yfft = fft(yk)
xfft = fftfreq(N, 1 / SAMPLE_RATE)                                              #plot the fft in a sample for each period Ts until the number of samples

                                                     
'''LPF SOLUTION
def butter_lowpass_filter(data, cutoff_low, fs, order):
    normal_cutoff = cutoff_low / nyq                                            #"fs is 2 half-cycles/sample, so these are normalized from 0 to 1, where 1 is the Nyquist frequency" 
    b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)          #b and a polynomial numerators and denominators of the filter
    y = filtfilt(b, a, data)                                                    #"Apply a digital filter forward and backward to a signal."
    return y

HPF SOLUTION
def butter_highpass_filter(data, cutoff_high, fs, order):
    normal_cutoff = cutoff_high / nyq                                           #"fs is 2 half-cycles/sample, so these are normalized from 0 to 1, where 1 is the Nyquist frequency" 
    b, a = butter(order, normal_cutoff, btype='highpass', analog=False)         #b and a polynomial numerators and denominators of the filter
    y = filtfilt(b, a, data)                                                    #"Apply a digital filter forward and backward to a signal."
    return y
'''

#BPF SOLUTION
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs                                                              #nyquist frequency
    low = lowcut / nyq                                                          #low cut, dividing by the Nyquist frequency (Wn needs to be between 0 and 1, where 1 is the Nyquist frequency)
    high = highcut / nyq                                                        #high cut, dividing by the Nyquist frequency (Wn needs to be between 0 and 1, where 1 is the Nyquist frequency)
    b, a = butter(order, [low, high], btype='band')                             #cutting, starting in cut_high*nyq until cut_low*nyq para baixo
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)                    #call the func above
    y = filtfilt(b, a, data)                                                    #filters the data using a rational transfer function defined by coefficients a and b
    return y                                                                    #filter -> rational TF in Z domain -> can be described as a differential equation and a "direct-form II transposed implementation..."
                                                                                                                                                                                                                
#requerimentos do BPF(conseguimos ver só 100Hz?)                                                       
cutoff_high = 115                                                               #high cut
cutoff_low = 85                                                                 #low cut
nyq = 0.5 * SAMPLE_RATE                                                         #nyquist frequency
order = 6                                                                       #filter order

#y = butter_lowpass_filter(yk, cutoff_high, SAMPLE_RATE, order)                 #from cutoff_high down
#k = butter_highpass_filter(yk, cutoff_low, SAMPLE_RATE, order)                 #from cutoff_low up
j = butter_bandpass_filter(yk, cutoff_low, cutoff_high, SAMPLE_RATE, order=5)   #from cutoff_low to cutoff_high

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Time domain (BEFORE/AFTER)')                                      #time domain
ax1.plot(yk[:100])                                                              #original signal
ax2.plot(j[:100])                                                               #sinal after the filter (hopefully only 100Hz component in this example)
  
yfftyk = fft(yk)                                                                #compute the fft of the original signal
xfftyk = fftfreq(N, T_SAMPLE)                                   

yfftj = fft(j)                                                                  #compute the fft of the filtered signal                                           
xfftj = fftfreq(N, T_SAMPLE)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_xlim(0, 500)
ax2.set_xlim(0, 500)
fig.suptitle('Frequency domain (BEFORE/AFTER)')                                 #gráfico no domínio das frequências
ax1.plot(xfftyk, np.abs(yfftyk))                                                #traçar a TF do sinal original
ax2.plot(xfftj, np.abs(yfftj))                                                  #traçar a TF do sinal filtrado
plt.show()                                                                      #rezar que esteja tudo bem





