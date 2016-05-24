import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from haystack.query import SearchQuerySet
from main.models import Thumbnail
from videoapp.models import VideoPost


def index(request):

    # Get params or their defaults
    
    order = request.GET.get("order", "publish_date")
    query = request.GET.get("query", None)
    
    try:
        # These casts might throw exceptions, so put them inside the try
        page_num = int(request.GET.get("page", "1"))
        per_page = int(request.GET.get("perPage", "25"))

        if query is not None:
            # Search
            video_ids = _do_video_search(query)
            vps = VideoPost.objects.filter(id__in=video_ids, public_access=True)
        else:
            # Default retrieval
            vps = VideoPost.objects.filter(public_access=True)

        # order and paginate
        vps = vps.order_by(order)
        pages = Paginator(vps, per_page)
        page = pages.page(page_num)
        add_image_urls(page)
        page_path = ""
        for key in request.GET:
            if key != "page":
                if page_path != "":
                    page_path += "&"
                page_path += "{0}={1}".format(key, request.GET.get(key))

        context = {
            "vp": page,
            "user": request.user,
            "pages": range(1, pages.num_pages + 1) if pages.num_pages > 1 else [],
            "current_page": page_num,
            "query": query,
            "page_path": page_path
        }
    except Exception as e:
        context = {
            "vp": [],
            "user": request.user,
            "pages": [],
            "current_page": 1,
            "query": query,
            "page_path": ""
        }

        print(str(e))

    return render(request, 'main/index.html', context)


def _get_vps_publish_date():
    return VideoPost.objects.filter(public_access=True).order_by('publish_date')


def add_image_urls(video_posts):
    """
    Add the urls to the thumbnail to each VideoPost
    Args:
        video_posts: list of VideoPost objects

    Returns:

    """
    for vp in video_posts:
        thumbs = Thumbnail.objects.filter(video=vp.upload.id)
        if len(thumbs) > 0:
            vp.thumb_url = thumbs[0].image_blob.get_url()
        else:
            vp.thumb_url = "https://placeholdit.imgix.net/~text?txtsize=23&txt=250%C3%97140&w=254&h=140"


def _do_video_search(query):
    """
    Do the actual searching
    Args:
        query:

    Returns:

    """
    return set(video.video_id for video in SearchQuerySet().models(VideoPost).auto_query(query))


@csrf_protect
def search_videos(request):
    """
    Perform a search request for all matching videos
    Args:
        request:

    Returns:

    """
    if request.method == "POST":
        query = request.POST.get("query")

        return HttpResponse(
            json.dumps({"video_ids": _do_video_search(query)}), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({""}), content_type="application/json"
        )
