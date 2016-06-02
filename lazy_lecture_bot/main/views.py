import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from haystack.query import SearchQuerySet
from main.models import Utterances, Videos
from videoapp.models import VideoPost


def index(request):
    # Get params or their defaults
    order = request.GET.get("order", "-publish_date")
    query = request.GET.get("query", None)
    
    if query is not None:
        # Search
        video_ids = _do_video_search(query)
        vps = VideoPost.objects.filter(id__in=video_ids, public_access=True)
    else:
        # Default retrieval
        vps = VideoPost.objects.filter(public_access=True)

    # Order results
    vps = vps.order_by(order)

    context = _build_index_context(request, vps, extra_context={"query": query})

    return render(request, 'main/index.html', context)


def favorites(request):
    favs = request.user.favorite_set.order_by("-video_post__publish_date").all()
    vps = [VideoPost.objects.get(pk=fav.video_post_id) for fav in favs]

    context = _build_index_context(request, vps)
    return render(request, "main/favorites.html", context)


def _build_index_context(request, vps, extra_context=None):
    try:
        # These casts might throw exceptions, so put them inside the try
        page_num = int(request.GET.get("page", "1"))
        per_page = int(request.GET.get("perPage", "25"))

        # order and paginate
        pages = Paginator(vps, per_page)
        page = pages.page(page_num)
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
            "page_path": page_path
        }
    except Exception as e:
        context = {
            "vp": [],
            "user": request.user,
            "pages": [],
            "current_page": 1,
            "page_path": ""
        }

        print(str(e))

    # Add extra context
    if extra_context is not None:
        for key, val in extra_context.items():
            context[key] = val

    return context


def _get_vps_publish_date():
    return VideoPost.objects.filter(public_access=True).order_by('publish_date')


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


@csrf_protect
def search_utterances(request):
    if request.method == "POST":
        video_id = request.POST.get("video_id")
        query = request.POST.get("query")
        videos = Videos.objects.filter(id=video_id)
        if len(videos) == 0:
            return HttpResponse()

        utterance_ids = [utterance_result.utterance_id
                         for utterance_result in SearchQuerySet().models(Utterances).filter(content__startswith=query)]

        return HttpResponse(
            json.dumps({"utterance_ids": utterance_ids}), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({""}), content_type="application/json"
        )

