import logging
from lazy_lecture_bot.celery import app
from main.models import BlobStorage, Videos, PipelineTypes
from modules.blob_storage import blob_settings
from modules.blob_storage.blob_storage import create_bsr_from_s3
from modules.voice_to_text import pipeline_lookup
from videoapp.models import VideoPost

logger = logging.getLogger("django")


@app.task(name="_async_vp")
def _async_vp(video_id):
    logger.info("doing async queuing for video_id: {0}".format(video_id))
    video = Videos.objects.get(pk=video_id)

    pipeline = pipeline_lookup.pipelines[video.pipeline_type.name]()
    pipeline.process_video(video)


def queue_vp_request(request, pipeline_name="watson"):
    """
    Queue a video processing request.
    Args:
        request: A request object with an authenticated user and a POST containing at least: "user_id", "title",
                 "description", and "public_access", "s3_file_key", "file_name"
        pipeline_name: The name of the pipeline type. Must be a valid pipeline type defined in PipelineTypes.

    Returns: An incomplete Videos record if the request was successful. Check the finished_processing field to check
             if it is ready to be used. None if the request failed.

    """
    s3_video_url = request.POST["video_file"]
    bucket_str = blob_settings.bucket_name + "/"
    if bucket_str not in s3_video_url:
        return None

    s3_key = s3_video_url.split(bucket_str)
    s3_key = s3_key[len(s3_key) - 1]

    # Video is uploaded and ready to process, do it
    try:
        video_blob = create_bsr_from_s3(s3_key)
    except FileNotFoundError:
        # There is no file with this file_key in the s3 bucket. Let's log this just in case we're getting spammed with
        # fake requests...
        logger.warn("Failed to find video file in s3. File key: {0}".format(s3_key))
        return None

    audio_blob = BlobStorage(file_name="")
    audio_blob.save()
    pipeline_type = PipelineTypes.objects.filter(name=pipeline_name).all()
    if len(pipeline_type) != 1:
        raise ValueError("Invalid pipeline name: {0}".format(pipeline_name))
    else:
        pipeline_type = pipeline_type[0]
    video = Videos(audio_blob=audio_blob, video_blob=video_blob, user_id=1, finished_processing=False,
                   pipeline_type=pipeline_type, processing_status="Video Queued")
    video.save()

    # Do the rest of the processing and transcribing asynchronously
    _async_vp.delay(video.id)

    return video
