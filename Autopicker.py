# MIT License
#
# Copyright (c) [2024] [HenStei]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.




import segyio
import numpy as np
import matplotlib.pyplot as plt
from obspy.io.segy.segy import _read_segy

def find_first_positive_y(trace, time_range):
    start_time, end_time = time_range
    for i, x in enumerate(trace[start_time:end_time]):
        if x != 0 and x != -5.877471754111438e-39 and x != 5.877471754111438e-39:
            return x, start_time + i
    return None, None

def find_time_ranges(trace):
    time_ranges = []
    start_time = None
    for i, x in enumerate(trace):
        if x != 0 and x != -5.877471754111438e-39 and start_time is None:
            start_time = i
        elif (x == 0 or x == -5.877471754111438e-39) and start_time is not None:
            time_ranges.append((start_time, i))
            start_time = None
    if start_time is not None:
        time_ranges.append((start_time, len(trace)))
    return time_ranges

def find_first_maximum(trace, time_range):
    start_time, end_time = time_range
    max_value = None
    max_index = None
    for i, x in enumerate(trace[start_time:end_time]):
        if max_value is None or x > max_value:
            max_value = x
            max_index = start_time + i
    return max_value, max_index

file_path = '/content/syn.sgy'
segyfile = _read_segy(file_path)
traces = [tr.data for tr in segyfile.traces]

# Arrays für Einsatzzeiten und Amplituden
p_wave_times = []
s_wave_times = []
a_ns = []
a_ew = []

for idx in range(0, len(traces), 2):
    trace_ns = traces[idx]
    trace_ew = traces[idx + 1]
    station_number = idx // 2 + 1

    time_ranges_ns = find_time_ranges(trace_ns)
    time_ranges_ew = find_time_ranges(trace_ew)

    if len(time_ranges_ns) >= 2:
        # P-Welle NS-Komponente
        y_value_p_ns, time_index_p_ns = find_first_positive_y(trace_ns, time_ranges_ns[0])
        max_value_p_ns, max_index_p_ns = find_first_maximum(trace_ns, time_ranges_ns[0])
        p_wave_times.append(time_index_p_ns)
        a_ns.append(max_value_p_ns)
        print(f"Station {station_number} (NS): Erster positiver y-Wert: {y_value_p_ns} bei Zeitindex: {time_index_p_ns} für P-Welle")
        print(f"Station {station_number} (NS): Erste maximale Amplitude: {max_value_p_ns} bei Zeitindex: {max_index_p_ns} für P-Welle")

        # S-Welle NS-Komponente
        y_value_s_ns, time_index_s_ns = find_first_positive_y(trace_ns, time_ranges_ns[1])
        s_wave_times.append(time_index_s_ns)
        print(f"Station {station_number} (NS): Erster positiver y-Wert: {y_value_s_ns} bei Zeitindex: {time_index_s_ns} für S-Welle")

        # Plotten der Spur NS-Komponente
        plt.figure()
        plt.plot(trace_ns)
        if y_value_p_ns is not None:
            plt.plot(time_index_p_ns, y_value_p_ns, 'ro', label='P-Welle')
        if max_value_p_ns is not None:
            plt.plot(max_index_p_ns, max_value_p_ns, 'kx', label='Maximale Amplitude P-Welle')
        if y_value_s_ns is not None:
            plt.plot(time_index_s_ns, y_value_s_ns, 'bo', label='S-Welle')
        plt.xlabel('Zeitindex')
        plt.legend()
        plt.title(f'Station {station_number} (NS)')
        plt.show()

    if len(time_ranges_ew) >= 2:
        # P-Welle EW-Komponente
        y_value_p_ew, time_index_p_ew = find_first_positive_y(trace_ew, time_ranges_ew[0])
        max_value_p_ew, max_index_p_ew = find_first_maximum(trace_ew, time_ranges_ew[0])
        p_wave_times.append(time_index_p_ew)
        a_ew.append(max_value_p_ew)
        print(f"Station {station_number} (EW): Erster positiver y-Wert: {y_value_p_ew} bei Zeitindex: {time_index_p_ew} für P-Welle")
        print(f"Station {station_number} (EW): Erste maximale Amplitude: {max_value_p_ew} bei Zeitindex: {max_index_p_ew} für P-Welle")

        # S-Welle EW-Komponente
        y_value_s_ew, time_index_s_ew = find_first_positive_y(trace_ew, time_ranges_ew[1])
        s_wave_times.append(time_index_s_ew)
        print(f"Station {station_number} (EW): Erster positiver y-Wert: {y_value_s_ew} bei Zeitindex: {time_index_s_ew} für S-Welle")

        # Plotten der Spur EW-Komponente
        plt.figure()
        plt.plot(trace_ew)
        if y_value_p_ew is not None:
            plt.plot(time_index_p_ew, y_value_p_ew, 'ro', label='P-Welle')
        if max_value_p_ew is not None:
            plt.plot(max_index_p_ew, max_value_p_ew, 'kx', label='Maximale Amplitude P-Welle')
        if y_value_s_ew is not None:
            plt.plot(time_index_s_ew, y_value_s_ew, 'bo', label='S-Welle')
        plt.xlabel('Zeitindex')
        plt.legend()
        plt.title(f'Station {station_number} (EW)')
        plt.show()

# Ausgabe der Arrays
print("Einsatzzeiten der P-Welle:", p_wave_times)
print("Einsatzzeiten der S-Welle:", s_wave_times)
print("Maximale Amplituden der NS-Komponente (A_NS):", a_ns)
print("Maximale Amplituden der EW-Komponente (A_EW):", a_ew)

