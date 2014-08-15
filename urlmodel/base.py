from django.db import models
from django.core.urlresolvers import reverse


__all__ = ('UrlModelMixin', 'UrlModel', 'CrudUrlModelMixin', 'CrudUrlModel')


class UrlModelMixin(object):
    """
    Provides methods for the URLs of basic actions such as searching,
    creating, inspecting (detail), updating, deleting.
    
    If a model instance is identified by pk, ``slug_field_name`` should be left
    blank, otherwise, give the name of the field.
    
    # Slug field name and slug kwarg name.

    The name of the argument in the URL that identifies this slug or the
    primary key is set in ``slug_kwarg_name``. A pk specified by an anonymous
    argument is not supported.
    Usually, both variables should be set to the same value.
    E.g.
    ````
    # urls.py
    urlpatterns('',
        url(
            r'pokemons/(?P<hoenn_pokedex_number>\d+)/$'),
            views.pokemon_detail_by_pokedex_number,
            name='pokemon-hoenn'
        ),
        url(
            r'pokemons/(?<pk>\d+)/?'),  # National Pokédex number
            views.pokemon_detail_by_pk,
            name='pokemon-pk'
        )
    )

    class
    ```` 

    # Arguments

    The first argument, optional, is ``url_name``. By default this will be:
    - search: 'modelname-search'
    - create: 'modelname-create'
    - detail: 'modelname'
    - update: 'modelname-update'
    - delete: 'modelname-delete'
    
    Any extra arguments to be passed as ``*args`` and ``**kwargs``.

    The create and search urls can be called from the class instead of and
    instance.

    To make custom instance urls, use ``get_instance_url`` and to make
    custom class urls, use ``get_class_url``.
    Usage: self.get_instance_url('hide', )
    
    Note: all methods are lazily evaluated and stored. Except for
    ``get_absolute_url``, though, one usually expects the same value to be
    returned by ``get_absolute_url`` and ``detail_url``, the latter accepts
    argument lists and keyword arguements.
    """

    slug_kwarg_name = None
    slug_field_name = None
    action_url_formatter = lambda model, action: '%s-%s' % (model, action)

    # this signature will override action_url_formatter
    # @classmethod
    # def format_action(cls, modelname, action):
    #     pass

    @classmethod
    def get_action_url_formatter(cls, action):
        if hasattr(cls, 'format_action'):
            return self.format_action(cls._meta.model_name, action)
        elif cls.action_url_formatter:
            return cls.action_url_formatter(cls._meta.model_name, action)

    @classmethod
    def get_class_url(cls, url_name, *args, **kwargs):
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    @classmethod
    def get_class_action_url(cls, action, *args, **kwargs):
        url_name = cls.get_action_url_formatter(action)
        return cls.get_class_url(url_name, *args, **kwargs)

    def get_instance_url(self, url_name, *args, **kwargs):
        slug_kwarg = self.slug_kwarg_name or 'pk'
        slug_field = self.slug_field_name or 'pk'
        kwargs[slug_kwarg] = getattr(self, slug_field)
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    def get_instance_action_url(self, action, *args, **kwargs):
        url_name = self.get_action_url_formatter(action)
        return self.get_instance_url(action, *args, **kwargs)


class UrlModel(UrlModelMixin, models.Model):
    """
    A class for any basic model that will only implement the UrlModelMixin.
    """


class CrudUrlModelMixin(UrlModelMixin):
    """
    Provides implementation for a non-lazy evaluation of a five 'action' URLs:
    - list (classmethod)
    - search(classmethod)
    - create (classmethod)
    - detail (instance method)
    - update (instance method)
    - delete (instance method)
    """

    def get_absolute_url(self):
        """
        Returns the URL for the detail view assuming that it does not receive
        any other arguments or keywords. The `detail_url` could be overriden
        to make this also work.
        """
        return self.detail_url()
    
    @classmethod
    def list_url(cls, *args, **kwargs):
        return cls.get_class_action_url('list', *args, **kwargs)

    @classmethod
    def search_url(cls, *args, **kwargs):
        return cls.get_class_action_url('search', *args, **kwargs)

    @classmethod
    def create_url(cls, *args, **kwargs):
        return cls.get_class_action_url('create', *args, **kwargs)

    def detail_url(self, *args, **kwargs):
        return self.get_instance_action_url('detail', *args, **kwargs)

    def update_url(self, *args, **kwargs):
        return self.get_instance_action_url('update', *args, **kwargs)

    def delete_url(self, *args, **kwargs):
        return self.get_instance_action_url('delete', *args, **kwargs)

class CrudUrlModel(CrudUrlModelMixin, models.Model):
    """
    This class should be enough for most applications. But you might want
    evaluation of urls to be lazy. Consider using `LazyCrudUrlModel`.
    """
