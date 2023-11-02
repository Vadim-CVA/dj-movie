from django import forms
from django.contrib import admin

from .models import Category,Actor,Genre,Movie,MovieShots,RatingStar,Rating,Reviews

from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label = "Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id","name","url")
    list_display_links = ("name",)


class ReviewInLine(admin.TabularInline):
    """Отображение комментариев в админке фильмы"""
    model = Reviews
    extra = 1
    readonly_fields = ("name","email")


class MovieShotsInLine(admin.TabularInline):
    """Отображение кадров из фильма в админке фильма"""
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="200" height="180"')
    
    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title","category","url","draft")
    list_filter = ("category","genres","year","draft",)
    search_fields = ("title","category__name","url")
    inlines = [MovieShotsInLine,ReviewInLine]
    save_on_top = True
    save_as = True
    actions = ["publish","unpublish"]
    form = MovieAdminForm
    list_editable = ("draft",)
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (
                ("title","tagline","category"),
            )
        }),
        (None, {
            "fields": (
                ("description","poster","get_image"),
            )
        }),
        (None, {
            "fields": (
                ("year","world_premiere", "country"),
            )
        }),
        ("Actors", {
            "fields": (
                ("actors","directors", "genres"),
            )
        }),
        ("Money", {
            "fields": (
                ("budget","fees_in_usa", "fess_in_world"),
            )
        }),
        ("Options", {
            "fields": (
                ("url","draft"),
            )
        }),
    )

    def unpublish(self,request,queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        self.message_user(request, f"{row_update} записей было обновлено")

    def publish(self,request,queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=False)
        self.message_user(request, f"{row_update} записей было обновлено")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )
    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change', )

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.poster.url} width="200" height="300"')
    
    get_image.short_description = " "
    

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name","email","parent","movie","id")
    readonly_fields = ("name","email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("id","name","url")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name","age","get_image")
    readonly_fields = ("get_image",)
    search_fields = ("name",)
    
    fieldsets = (
        ("БИО", {
            
            "fields": (
                ("name","age","description"),
            )
        }),
        ("Изображение", {
            "classes" : ("collapse",),
            "fields": (
                ("get_image"),
            )
        }),
    )
    
    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="90"')
    
    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title","description","movie","get_image")
    readonly_fields = ("get_image",)

    def get_image(self,obj):
        return mark_safe(f'<img src={obj.image.url} width="170" height="90"')
    
    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star","movie","ip")




admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"


admin.site.register(RatingStar)

