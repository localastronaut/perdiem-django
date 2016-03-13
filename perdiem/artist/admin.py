"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from django.contrib import admin

from artist.models import Genre, Artist, Bio, Photo, SoundCloudPlaylist, \
    Social, Update


class BioInline(admin.StackedInline):

    model = Bio


class PhotoInline(admin.TabularInline):

    model = Photo


class SoundCloudPlaylistInline(admin.TabularInline):

    model = SoundCloudPlaylist
    extra = 1


class SocialInline(admin.TabularInline):

    model = Social


class ArtistAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    inlines = (BioInline, PhotoInline, SoundCloudPlaylistInline, SocialInline,)


admin.site.register(Genre)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Update)
