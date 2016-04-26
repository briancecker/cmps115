import subprocess
import wave

import sys

import os
from modules import file_utilities

STRIP_AUDIO_CMD = "ffmpeg -i {input_file} -y -ab 160k -ac 2 -ar 16000 -vn {output_file}"


def strip_audio(video):
    """
    Gets the audio from a video file.

    Args:
        video: The path to the video to take audio from

    Returns: The path to an audio file and the ffmpeg return code

    """
    if not os.path.exists(video):
        raise FileNotFoundError("video file {0} does not exist, refusing to pass it to ffmpeg".format(video))
    # tmp file to hold audio output
    audio = os.path.abspath(os.path.join(
        file_utilities.TMP_DIR, "audio_{0}.wav".format(file_utilities.path_leaf(video))))
    strip_cmd = STRIP_AUDIO_CMD.format(input_file=video, output_file=audio).split()
    p = subprocess.Popen(strip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait until the stripping is done
    return_code = p.wait()

    # Close these to avoid a resource leak that unittests complain about
    p.stdout.close()
    p.stderr.close()

    return audio, return_code


def read_audio_frames(audio, n_frames):
    """
    Reads an audio file as smaller audio segments based on the number of frames specified.
    Args:
        audio: path to the audio file to segment
        n_frames

    Yields: at most n_frames frames from the audio file as a string of bytes

    """
    with wave.open(audio, 'rb') as wave_read:
        total_frames = wave_read.getnframes()
        read_frames = 0
        while read_frames < total_frames:
            yield wave_read.readframes(n_frames)
            read_frames += n_frames


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


def get_audio_params(audio):
    with wave.open(audio, "rb") as wave_read:
        params = wave_read.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        return {"nchannels": nchannels,
                "sampwidth": sampwidth,
                "framerate": framerate,
                "nframes": nframes,
                "comptype": comptype,
                "compname": compname
                }


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
