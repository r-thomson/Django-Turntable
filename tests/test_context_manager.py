from django.test import TestCase

from django_turntable import inspect_queries

from .models import Album, Artist, Song


class TestInspectQueries(TestCase):
    def test_counts_queries_and_logs_as_context_manager(self):
        with self.assertLogs('django_turntable', level='INFO') as logs:
            with inspect_queries():
                Artist.objects.create(name='Joywave')
                Album.objects.count()

        self.assertEqual(len(logs.output), 1)
        self.assertRegex(logs.output[0], r'2 queries executed \(\d+\.\d+ms\)')

    def test_counts_queries_and_logs_as_context_decorator(self):
        @inspect_queries()
        def execute_queries():
            Artist.objects.create(name='Joywave')
            Album.objects.count()

        with self.assertLogs('django_turntable', level='INFO') as logs:
            execute_queries()

        self.assertEqual(len(logs.output), 1)
        self.assertRegex(logs.output[0], r'2 queries executed \(\d+\.\d+ms\)')

    def test_does_not_log_if_no_queries(self):
        with self.assertNoLogs('django_turntable', level='INFO'):
            with inspect_queries():
                pass

    def test_warns_for_repeated_queries(self):
        with self.assertLogs('django_turntable', level='WARNING') as logs:
            with inspect_queries():
                for i in range(10):
                    list(Song.objects.filter(id=i))

        self.assertEqual(len(logs.output), 1)
        self.assertRegex(
            logs.output[0],
            r'Repeating query \(10x\): SELECT .+ FROM "tests_song" WHERE "tests_song"."id" = %s$',
        )
