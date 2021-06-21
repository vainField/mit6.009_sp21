# No Imports Allowed!


def backwards(sound):
    sound_l = sound['left']
    sound_r = sound['right']

    len_l = len(sound_l)
    len_r = len(sound_r)

    bl = []
    br = []
    brt = sound['rate']

    for i in range(len_l):
        bl.append(sound_l[len_l - 1 - i])

    for j in range(len_r):
        br.append(sound_r[len_r - 1 - j])

    return {'rate': brt, 'left': bl, 'right': br}      


def mix(sound1, sound2, p):
    if sound1['rate'] != sound2['rate']:
        return None

    s1_l = sound1['left']
    s1_r = sound1['right']
    s2_l = sound2['left']
    s2_r = sound2['right']

    len_m = min(len(s1_l), len(s2_l))
    m_l=[]
    m_r=[]
    for i in range(len_m):
        m_l.append(s1_l[i]*p + s2_l[i]*(1-p))
        m_r.append(s1_r[i]*p + s2_r[i]*(1-p))
    
    return {'rate': sound1['rate'], 'left': m_l, 'right': m_r}   

def echo(sound, num_echos, delay, scale):
    s_l = sound['left'][:]
    s_r = sound['right'][:]

    sample_delay = round(delay * sound['rate'])
    sample_num = len(s_l) + sample_delay * num_echos

    echo_l = [0]*sample_num
    echo_r = [0]*sample_num
    for i in range(num_echos + 1):
        for j in range(len(s_l)):
            echo_l[j + i * sample_delay] += s_l[j] * (scale**i)
            echo_r[j + i * sample_delay] += s_r[j] * (scale**i)
    
    return {'rate': sound['rate'], 'left': echo_l, 'right': echo_r} 

def pan(sound):
    s_l = sound['left']
    s_r = sound['right']

    s_len = len(s_l)

    p_l = []
    p_r = []

    for i in range(s_len):
        p_l.append(s_l[i] * (s_len-1-i) / (s_len-1))
        p_r.append(s_r[i] * i / (s_len-1))

    return {'rate': sound['rate'], 'left': p_l, 'right': p_r} 

def remove_vocals(sound):
    s_l = sound['left']
    s_r = sound['right']

    s_len = len(s_l)

    rv_l = []
    rv_r = []

    for i in range(s_len):
        rv_l.append(s_l[i]-s_r[i])
        rv_r = rv_l

    return {'rate': sound['rate'], 'left': rv_l, 'right': rv_r}     


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':

    # s = load_wav('sounds/mystery.wav')
    # s1 = load_wav('sounds/synth.wav')
    # s2 = load_wav('sounds/water.wav')
    # s_e = load_wav('sounds/chord.wav')
    # s_p = load_wav('sounds/car.wav')
    s_rv = load_wav('sounds/coffee.wav')

    # write_wav(backwards(s), 'mystery_reversed.wav')
    # write_wav(mix(s1, s2, 0.2), 'mix.wav')
    # write_wav(echo(s_e, 5, 0.3, 0.6), 'echo.wav')
    # write_wav(pan(s_p), 'pan.wav')
    write_wav(remove_vocals(s_rv), 'romove_vocals.wav')
