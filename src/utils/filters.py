import re


def get_id_video(link_video):
    regex_id = re.compile("""^.*(youtu\\.be\\/|v\\/|u\\/\\w\\/|
                          embed\\/|watch\\?v=|\\&v=)([^#\\&\\?]*).*""")

    match = re.match(regex_id, link_video)
    if match:
        id_video = match.group(2)
    else:
        id_video = None

    return id_video
