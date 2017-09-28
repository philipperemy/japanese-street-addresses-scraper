import requests


def get_address_by_gps(lat='136.50656688934518', lon='36.07898638675558'):
    # 'https://www.google.fr/maps/preview/reveal?authuser=0&hl=fr&pb=!2m9!1m3!1d13702.886796058505!2d139.735146!3d35.6993669!2m0!3m2!1i1166!2i812!4f13.1!3m2!2d136.50656688934518!3d36.07898638675558!4m2!1s4mXMWZsFy-rwBf2vsoAO!7e81!5m4!2m3!1i96!2i64!3i1'
    return 'https://www.google.jp/maps/preview/reveal?authuser=0&hl=fr&pb=!2m9!1m3!1d13702.886796058505!2d139.735146!3d35.6993669!2m0!3m2!1i1166!2i812!4f13.1!3m2!2d{}!3d{}!4m2!1s4mXMWZsFy-rwBf2vsoAO!7e81!5m4!2m3!1i96!2i64!3i1'.format(
        lat, lon)


r = requests.get(get_address_by_gps())
print(r.encoding)
a = r.content
b = 2
