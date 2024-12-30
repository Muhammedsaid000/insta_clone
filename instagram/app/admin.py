from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *


class PostImageInLine(admin.TabularInline):
    model = PostPhotos
    extra = 1


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = [PostImageInLine]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Story)
admin.site.register(SavePost)
admin.site.register(SaveItem)