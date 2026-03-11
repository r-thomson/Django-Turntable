from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import ManyRelatedManager


class Artist(models.Model):
    name = models.CharField(max_length=255)

    if TYPE_CHECKING:
        album_set: ManyRelatedManager[Album]
        song_set: ManyRelatedManager[Song]


class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    if TYPE_CHECKING:
        song_set: ManyRelatedManager[Song]


class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.RESTRICT)


__all__ = ['Artist', 'Album', 'Song']
