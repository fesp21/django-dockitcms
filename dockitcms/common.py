import dockit

import re

from django import forms
from django.conf.urls.defaults import patterns
from django.core.urlresolvers import RegexURLResolver

FORM_FIELD_TO_DOCKIT_FIELD = [
    (forms.BooleanField, dockit.BooleanField),
    #(forms.CharField, dockit.CharField),
    (forms.DateField, dockit.DateField),
    (forms.DateTimeField, dockit.DateTimeField),
    (forms.DecimalField, dockit.DecimalField),
    (forms.EmailField, dockit.EmailField),
    (forms.FileField, dockit.FileField),
    (forms.FloatField, dockit.FloatField),
    (forms.IntegerField, dockit.IntegerField),
    (forms.IPAddressField, dockit.IPAddressField),
    #(forms.GenericIPAddressField, dockit.GenericIPAddressField),
    (forms.SlugField, dockit.SlugField),
    (forms.TimeField, dockit.TimeField),
    (forms.ModelChoiceField, dockit.ModelReferenceField),
]

REGISTERED_VIEW_POINTS = dict()

def register_view_point_class(key, cls):
    REGISTERED_VIEW_POINTS[key] = cls()

def dockit_field_for_form_field(form_field):
    df_kwargs = {'blank': not form_field.required,
                 'help_text': form_field.help_text,}
    if isinstance(form_field, forms.CharField):
        if isinstance(form_field.widget, forms.TextInput):
            return dockit.CharField(**df_kwargs)
        return dockit.TextField(**df_kwargs)
    if isinstance(form_field, forms.ModelChoiceField):
        df_kwargs['model'] = form_field.queryset.model
    for ff, df in FORM_FIELD_TO_DOCKIT_FIELD:
        if isinstance(form_field, ff):
            return df(**df_kwargs)

class CMSURLResolver(RegexURLResolver):
    def __init__(self, regex, url_patterns, default_kwargs=None, app_name=None, namespace=None):
        # regex is a string representing a regular expression.
        # urlconf_name is a string representing the module containing URLconfs.
        self.regex = re.compile(regex, re.UNICODE)
        self._url_patterns = url_patterns
        self.callback = None
        self.default_kwargs = default_kwargs or {}
        self.namespace = namespace
        self.app_name = app_name
        self._reverse_dict = None
        self._namespace_dict = None
        self._app_dict = None
    
    def _get_url_patterns(self):
        return self._url_patterns
    url_patterns = property(_get_url_patterns)
    
    def __repr__(self):
        return '<%s (%s:%s) %s>' % (self.__class__.__name__, self.app_name, self.namespace, self.regex.pattern)

class BaseViewPointClass(object):
    form_class = None
    label = None
    
    def get_document(self, view_point_doc):
        doc_cls = view_point_doc.collection.get_document()
        return doc_cls
    
    def register_view_point(self, view_point_doc):
        pass
        #here it would ensure all neceassry indexes are created
    
    def get_urls(self, view_point_doc):
        return patterns('')
    
    def get_templated_form(self):
        return self.get_form_class()()
    
    def get_form_class(self):
        return self.form_class
    
    def get_resolver(self, view_point_doc):
        urls = self.get_urls(view_point_doc)
        return CMSURLResolver(r'^'+view_point_doc.url, urls)
    
    def dispatch(self, request, view_point_doc):
        resolver = self.get_resolver(view_point_doc)
        view_match = resolver.resolve(request.path)
        return view_match.func(request, *view_match.args, **view_match.kwargs)
    
    def reverse(self, view_point_doc, name, *args, **kwargs):
        resolver = self.get_resolver(view_point_doc)
        return resolver.reverse(name, *args, **kwargs)
