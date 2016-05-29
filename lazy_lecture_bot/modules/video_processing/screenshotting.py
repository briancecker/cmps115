import logging
import subprocess

import io
import os
from PIL import Image

PROBE_SIZE = os.environ.get("PROBE_SIZE", "5000000")
ANALYZE_DURATION = os.environ.get("ANALYZE_DURATION", "200000000")
SCREENSHOT_CMD = "ffmpeg -analyzeduration {analyze_duration} " \
                 "-probesize {probe_size} " \
                 "-i - " \
                 "-ss {time} " \
                 "-vframes 1 " \
                 "-q:v 2 " \
                 "-f image2pipe " \
                 "-".format(analyze_duration=ANALYZE_DURATION, probe_size=PROBE_SIZE, time="{time}")

logger = logging.Logger("django")


def take_screenshot(video_bytes: bytes, time: tuple, width: int, height: int):
    """
    Take a screenshot at the specified time.
    Args:
        video_bytes: Video as bytes
        time: The time to screenshot at. A tuple of integers representing (hours, mins, seconds)
        width: Width of the screenshot in pixels
        height: Height of the screenshot in pixels

    Returns: The screenshot as bytes, loaded with Image

    """
    if time[1] > 59:
        raise ValueError("More than 59 minutes is an incorrect time specification")
    if time[2] > 59:
        raise ValueError("More than 59 seconds is an incorrect time specification")

    time_str = "{0}:{1:02d}:{2:02d}".format(time[0], time[1], time[2])
    p = subprocess.Popen(SCREENSHOT_CMD.format(time=time_str).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    screenshot, err = p.communicate(input=video_bytes)
    logger.warning(err.decode("utf-8"))
    return_code = p.returncode
    if return_code != 0:
        logger.warning("non-zero return code when screenshotting video")

    # Resize to specified dimensions
    im = Image.open(io.BytesIO(screenshot))
    im.thumbnail((width, height), Image.ANTIALIAS)
    resized = io.BytesIO()
    im.save(resized, "JPEG")
    im.close()

    resized.seek(0)
    resized_bytes = resized.read()

    return resized_bytes, return_code
