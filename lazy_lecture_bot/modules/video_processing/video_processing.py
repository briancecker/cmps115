import io
import logging
import subprocess
import sys
import wave

# STRIP_AUDIO_CMD = "ffmpeg -i - -y -ab 160k -ac 2 -ar 16000 -vn -"
NUM_CHANNELS = 2
SAMPLE_FORMAT = "s16"  # 16 bit depth
SAMPLE_RATE = 16000
STRIP_AUDIO_CMD = "ffmpeg -vcodec h264 -acodec aac -i - -y -ab 160k -ac {num_channels} -ar {sample_rate} " \
                  "-vn -sample_fmt {sample_fmt} -f wav -".format(num_channels=NUM_CHANNELS, sample_rate=SAMPLE_RATE,
                                                                 sample_fmt=SAMPLE_FORMAT)

logger = logging.Logger("django")


def strip_audio(video):
    """
    Gets the audio from a video

    Args:
        video: The video as a file wrapper, BytesIO wrapper, etc.

    Returns: The audio as bytes and the ffmpeg return code

    """
    p = subprocess.Popen(STRIP_AUDIO_CMD.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    audio, err = p.communicate(input=video)
    logger.warn(err.decode("utf-8"))
    return_code = p.returncode

    return audio, return_code


def read_audio_frames(audio, n_frames):
    """
    Reads an audio file as smaller audio segments based on the number of frames specified.
    Args:
        audio: path to the audio file to segment
        n_frames

    Yields: at most n_frames frames from the audio file as a string of bytes

    """
    n_at_once = 10000000
    with wave.open(io.BytesIO(audio), 'rb') as wave_read:
        # total_frames = wave_read.getnframes()  # getnframes IS BUGGED
        frame_size = wave_read.getnchannels() * wave_read.getsampwidth()
        all_frames = b''
        while True:
            frames = wave_read.readframes(n_at_once)
            all_frames += frames
            if len(frames) < (n_at_once * frame_size):
                break

        current = 0
        while (current * frame_size) < len(all_frames):
            yield all_frames[current * frame_size:(current+n_frames) * frame_size]
            current += n_frames


def read_audio_segments_by_time(audio, time):
    """
    Reads an audio file as smaller audio segments based on a time length for each segment.
    Args:
        audio: path to the audio file to segment
        time: how long each segment should be in seconds, decimals are acceptable

    Yields: An audio segment as a string of bytes

    """
    params = get_audio_params(audio)
    frames_per_segment = int(time * params["framerate"])
    return read_audio_frames(audio, frames_per_segment)


def get_audio_duration(audio):
    params = get_audio_params(audio)
    n_frames = sum(bytes_to_n_frames(frame_group, params["nchannels"], params["sampwidth"])
                   for frame_group in read_audio_frames(audio, 5000))
    return n_frames / params["framerate"]


def get_audio_params(audio):
    with wave.open(io.BytesIO(audio), "rb") as wave_read:
        params = wave_read.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        return {"nchannels": nchannels,
                "sampwidth": sampwidth,
                "framerate": framerate,
                "nframes": nframes,
                "comptype": comptype,
                "compname": compname
                }


def new_audio_buffer(from_buffer):
    buffer = io.BytesIO()
    wave_write = wave.open(buffer, 'wb')
    with wave.open(io.BytesIO(from_buffer), 'rb') as wave_read:
        # For some reason setparams(getparams()) does not work with a BytesIO()...
        nchannels, sampwidth, framerate, nframes, comptype, compname = wave_read.getparams()
        wave_write.setnchannels(nchannels)
        wave_write.setsampwidth(sampwidth)
        wave_write.setframerate(framerate)
        wave_write.setcomptype(comptype, compname)

    return wave_write, buffer


def copy_audio_file_settings(audio_in, audio_out):
    """
    Creates a new file with the settings (nchannels, samplewidth, etc.) copied from another file.
    Args:
        audio_in: The file to copy from
        audio_out: The file to copy to

    Returns: An open Wave_write object

    """
    wave_write = wave.open(audio_out, 'wb')
    with wave.open(audio_in, 'rb') as wave_read:
        wave_write.setparams(wave_read.getparams())

    return wave_write


def bytes_to_n_frames(frame_bytes, n_channels, sample_width):
    """
    Calculate how many frames are represented by the bytes object (which represents some audio)
    Args:
        frame_bytes: The bytes object representing some frames as bytes
        n_channels: The number of channels in this audio
        sample_width: The sample width of this audio

    Returns: The number of frames that the frame_bytes object actually is

    """
    # Get base size of an empty bytes object
    empty_bytes_size = sys.getsizeof(b'')
    # Calculate the size of each frame:
    # the number of channels * the number of bytes to represent each channel
    bytes_per_frame = n_channels * sample_width

    return (sys.getsizeof(frame_bytes) - empty_bytes_size) / bytes_per_frame
