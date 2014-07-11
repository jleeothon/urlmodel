# urlmodel

Creating rich and dry URLs for a Django model.

## Introduction

As I started using class-based views for Django, I understood what the `get_absolute_url` method was about. Then I encountered the problem of using URLs that required more than once piece of information from a model instance, let's say, not a single primary key or slug. That's a bit abstract, take:

- `/regions/cat-cat-province/towns/mieaou/`

This identifies Mieaou town within Cat-Cat Province (there's another Mieaou town within Copy-Cat Province). Now let's say the usual list of things you'll do with a model is listing, reading detail, creating, updating, deleting (roughly, [CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)). Roughly, you'll have this URLs:

- `/regions/cat-cat-province/towns/list`
- `/regions/cat-cat-province/towns/create`
- `/regions/cat-cat-province/towns/mieaou/edit`
- `/regions/cat-cat-province/towns/mieaou/delete`

An important part to notice is that we're using *more than one piece of information per instance*, which makes things a bit more messy than just a pk. Why not just use a pk? First, I *think* there are security implications. Second, nobody wants to remember a pk. Third, programmers respect well-formed URLs and look down to senseless sequences of numbers with unfathomable disdain.

What if you provide a link to the edit and delete sections? You'll probably go for

```Python
# urls.py

urlpatterns = patterns('',
    # ...
    url(
        '^regions/(?P<region_slug>[a-zA-Z0-9-]+)/towns/(?P<town_slug>[a-zA-Z0-9-]+)/edit/?$',
        name='town-update'
    ),
    # ...
)
```

```Django
# html
{% url 'town-update' region_slug=town.region.name_slug town_slug=town.name_slug %}
```

> Note: I mostly use "update" for internal stuff for convention and readability ("update" has the length as "create" and "delete" and "detail" and "search"), but I use "edit" for usability when it'll be read by the end-user.

The latter one is not very [DRY](https://docs.djangoproject.com/en/dev/misc/design-philosophies/#don-t-repeat-yourself-dry). So I thought I could start writing a `get_update_url` method, and so on. Then every model class definition would have a set of `get_detail_url`, `get_update_url`, `get_delete_url` methods, plus `get_create_url` and `get_list_url` methods (in the original project, it was "search" instead of "list"). Now, given that my URLs have roughly the same naming format for every model (`town-list`, `town-create`, `town-detail`, `town-update`, `town-delete`), that is not very DRY either!

I decided to write a smart and flexible URL system so that the next time I would need a list-create-detail-update-delete set of URLs, things would be as easy as adding a mixin to the inheritance tree of the model.

## Requirements

I know, my requirements suck.

- Python 3
- Django 1.6

I'm not sure if this app will not work on previous versions of Django, but I think I will not with Python 2.

## Getting started

I don't know yet how to publish this project. Just copy & paste as needed.

## How to use

Using the default CRUD urls is as easy as extending funcionality as a mixin.

```Python
# models.py

from django.db import models

class Town(CrudUrlModelMixin, models.Model):
    pass
    
# or, if you're only going to extend the urlmodel functionality...

class Town(CrudUrlModel):
    pass
```

The former example will create a set of five methods (class-level: list, create; instance-level: detail, update, delete) that expect an URL based on the model name and the name of the "action". Also, these expect an URL keyword argument called "pk".

In order to use a slug field, you should override `slug_kwarg_name` (to match the URL kwarg) and `slug_field_name` (to match the model slug).

```Python

# urls.py

urlpatterns = patterns('',
    # ...
    url(
        '^digimons/(?P<name>[a-zA-Z0-9-]+)/?$',
        name='digimon-detail'
    ),
    # ...
)

# models.py

class Digimon(UrlModelMixin, models.Model):
    name = CharField(max_length=100)
    sluggified_name = SlugField(max_length=100)
    
    slug_kwarg_name = 'name'
    slug_field_name = 'sluggified_name'

```

> Try out the lazy counterparts, `LazyCrudUrlModelMixin` and `LazyCrudUrlModel`!

## Advanced stuff

If the default "CRUD" system —which is actually "list, create, detail, update, delete"— do not work for you, you can try out `UrlModel` and `UrlModelMixin` (plus their lazy counterparts).

**Note: CruddUrlModel provides implementation for `get_absolute_url` too, and defaults to `get_detail_url`.**

### Action URLs

These are URLs based on "action names", such as "detail", "create", etc. For convention, ease and readability, you should try to stick to these methods.

```Python

class TownPerson(UrlModelMixin, Model):

    def get_defenestrate_url(self):
        self.get_instance_action_url("defenestrate")
        # expects townperson-defenestrate to exist.

    @classmethod
    def get_last_defenestrated(cls):
        cls.get_class_action_url("last-defenestrated")
        # expects townperson-last-defenestrated to exist.
```

### Extra information for URL

If you need to rely on more information than a single pk or slug, use `*args` and `**kwargs` to pass on this information to the `urlresolvers.reverse` method.

```Python
class Town(CrudUrlModelMixin, Model):
    
    def get_detail_url(self):
        super().get_detail_url(region_slug=self.region.sluggified_name)
```

The above example does also work similarly for the simpler `UrlModelMixin` class.

Be careful!,

> Instance url methods (`get_instance_url` and `get_instance_action_url`) always pass the pk or slug argument to `urlresolvers.reverse`.

### Custom URL names

If you want to provide a custom URL instead of an automatic `modelname-action`, use `@classmethod get_class_url(cls, url_name, *args, **kwargs)` and `get_instance_url(self, url_name, *args, **kwargs)`.

### Format for action URLs

**Note: this section is subject to change in upcoming versions.**

Action URLs are formatted `modelname-action` by default. To change this format, override the `action_url_formatter` object or provide a `format_action` class method. If you provide the latter method, the former object will be ignored.

```Python
action_url_formatter = lambda model, action: '%s-%s' % (model, action)
# this signature will override action_url_formatter
# @classmethod
# def format_action(cls, modelname, action):
#     pass
```

## Proposals

- Provide support for Python 2, probably trough [six](https://pypi.python.org/pypi/six/1.7.3).
- Make this project available through [PyPI](https://pypi.python.org/pypi).

## Resources

- [url template tag](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#url)
- [Reversing URLs](https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse)
- [Slug fields](https://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield)
- [Class-based views](https://docs.djangoproject.com/en/dev/topics/class-based-views/)
