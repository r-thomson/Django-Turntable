from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.test import Client, TestCase, override_settings
from django.urls import re_path

from .models import Album, Artist, Song


def list_albums(request: HttpRequest):
    return JsonResponse(
        [
            {
                'name': album.name,
                'artist': album.artist.name,
                'songs': [
                    {
                        'name': song.name,
                        'artist': song.artist.name,
                    }
                    for song in album.song_set.all()
                ],
            }
            for album in Album.objects.all()
        ],
        safe=False,
    )


def noop(request: HttpRequest):
    return HttpResponse()


urlpatterns = [
    re_path('^albums/$', list_albums),
    re_path('^noop/$', noop),
]


@override_settings(ROOT_URLCONF=__name__)
class TestTurntableMiddleware(TestCase):
    def setUp(self):
        self.client = Client()

        artist = Artist.objects.create(name='Slow Teeth')
        album = Album.objects.create(name='I - EP', artist=artist)
        Song.objects.bulk_create(
            [
                Song(name='Holy Death / Peace On Earth', album=album, artist=artist),
                Song(name='Sundials', album=album, artist=artist),
                Song(name='Still You Speak', album=album, artist=artist),
                Song(name='Plushy', album=album, artist=artist),
            ]
        )

    def test_counts_queries_as_middleware(self):
        with self.assertLogs('django_turntable', level='INFO') as logs:
            response = self.client.get('/albums/')
            self.assertEqual(response.status_code, 200)

        self.assertEqual(len(logs.output), 2)
        self.assertRegex(logs.output[0], r'7 queries executed \(\d+\.\d+ms\)')
        self.assertRegex(
            logs.output[1], r'Repeating query \(5x\): SELECT .+ FROM "tests_artist"'
        )

    def test_does_not_log_if_no_queries(self):
        with self.assertNoLogs('django_turntable', level='INFO'):
            response = self.client.get('/noop/')
            self.assertEqual(response.status_code, 200)
