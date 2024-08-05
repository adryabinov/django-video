from django.http import HttpResponse, FileResponse
from PIL import ImageColor
from utils import scrollvideo



def index(request):
    if request.GET.get('text'):
        if request.GET.get('color'):
            try:
                ImageColor.getrgb(request.GET.get('color'))
            except ValueError:
                return HttpResponse("wrong color")
        if request.GET.get('bg_color'):
            try:
                ImageColor.getrgb(request.GET.get('bg_color'))
            except ValueError:
                return HttpResponse("wrong bg_color")
        text = request.GET.get('text')
        color = request.GET.get('color') if request.GET.get('color') else scrollvideo.TEXT_COLOR
        bg_color = request.GET.get('bg_color') if request.GET.get('bg_color') else scrollvideo.BG_COLOR
        resolution = (100,100)
        duration = 3
        fps = 25


        scrollvideo.save_scroll_video(
            scrollvideo.clip_image(
                scrollvideo.text_image(
                        text=text,
                        color=color),
                bg_color=bg_color,
                resolution=resolution,
                duration=duration,
                fps=fps),
                    resolution=resolution,
                    duration=duration,
                    fps=fps)
        return FileResponse(open('video/video.mp4', "rb"), filename="video.mp4")
    return HttpResponse("""make scroll based video vs 'text' in reqest, 
                        change color of text and background vs 'color' and 'bg_color' 
                        (use rgb color consts)""")
