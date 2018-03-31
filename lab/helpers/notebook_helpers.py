from IPython.display import HTML


def play_video(path, width=320, height=240, format='mp4'):
    html = """
        <video width="{width}" height="{height}" controls>
        <source src="{path}" type="video/{format}">
        </video>
        """.format(path=path, width=width, height=height, format=format)

    return HTML(html)
