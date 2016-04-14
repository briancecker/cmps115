import subprocess
import wave

import os
from lazy_lecture_bot.modules import file_utilities

STRIP_AUDIO_CMD = "ffmpeg -i {input_file} -y -ab 160k -ac 2 -ar 44100 -vn {output_file}"


def strip_audio(video):
    """
    Gets the audio from a video file.

    Args:
        video: The path to the video to take audio from

    Returns: The path to an audio file.

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


def read_audio_segments(audio, time):
    """
    Reads an audio file as smaller audio segments based on a time length for each segment.
    Args:
        audio: path to the audio file to segment
        time: how long each segment should be in seconds, decimals are acceptable

    Yields: An audio segment as a string of bytes

    """
    with wave.open(audio, 'rb') as wave_read:
        framerate = wave_read.getframerate()
        total_frames = wave_read.getnframes()
        frames_per_segment = int(time * framerate)
        read_frames = 0
        while read_frames < total_frames:
            yield wave_read.readframes(frames_per_segment)
            read_frames += frames_per_segment


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

