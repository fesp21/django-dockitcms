from dockitcms.mixins import AdminInlineMixin
from dockitcms.models import BaseViewPoint, Collection

from dockit import schema

from exceptions import HttpForbidden

class AuthConfiguration(schema.Schema):
    authenticated_users_only = schema.BooleanField(default=False)
    staff_only = schema.BooleanField(default=False)
    required_permissions = schema.ListField(schema.CharField(), blank=True) #object or app permissions required for the user

class AuthMixinSchema(schema.Schema):
    _auth = schema.SchemaField(AuthConfiguration)

class AuthMixin(AdminInlineMixin):
    schema_class = AuthMixinSchema
    label = 'Auth Mixin'
    
    def on_dispatch(self, event, view, **kwargs):
        user = kwargs['request'].user
        if self._auth.authenticated_users_only and not user.is_authenticated():
            raise HttpForbidden()
        if self._auth.staff_only and not user.is_staff:
            raise HttpForbidden()
        for perm in self._auth.required_permissions:
            if not user.has_perm(perm):
                raise HttpForbidden()
    
    def on_object(self, event, view, **kwargs):
        obj = kwargs['object']
        user = view.request.user
        auth_info = getattr(obj, '_auth', None)
        required_perms = set(self._auth.required_permissions)
        
        if auth_info:
            if auth_info.authenticated_users_only and not user.is_authenticated():
                raise HttpForbidden()
            if auth_info.staff_only and not user.is_staff:
                raise HttpForbidden()
            required_perms.update(auth_info.required_permissions)
        for perm in required_perms:
            if not user.has_perm(perm, obj):
                raise HttpForbidden()
    
    def on_context(self, event, view, **kwargs):
        context = kwargs['context']
        user = view.request.user
        obj = getattr(view, 'object', None)
        context['object_user_perms'] = user.get_all_permissions(obj)

Collection.register_mixin('dockitcms.auth', AuthMixin)
BaseViewPoint.register_mixin('dockitcms.auth', AuthMixin)