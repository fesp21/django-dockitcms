import hyperadmin


#from django.conf.urls.defaults import patterns, url
#from django.utils.functional import update_wrapper

from dockitcms.models import Collection, SubsiteResourceDefinition, DocumentDesign, Subsite, Application, Index, BaseRecipe
from dockitcms.resources.common import ReloadCMSSiteMixin, CMSDocumentResource

#from views import ManageCollectionView

#from common import CMSDocumentResource, AdminAwareSchemaAdmin

app_name = 'dockitcms'

class ApplicationResource(CMSDocumentResource):
    pass

hyperadmin.site.register(Application, ApplicationResource, app_name=app_name)

class DocumentDesignResource(CMSDocumentResource):
    pass

hyperadmin.site.register(DocumentDesign, DocumentDesignResource, app_name=app_name)

class CollectionResource(ReloadCMSSiteMixin, CMSDocumentResource):
    list_display = ['title', 'application']#, 'admin_manage_link']
    
    def get_manage_collection_resource_kwargs(self, item, **kwargs):
        document_class = item.instance.get_document()
        params = {'resource_adaptor':document_class,
                  'site':self.site,
                  'parent_resource':self,
                  'collection':item,}
        params.update(kwargs)
        return params
    
    def get_manage_collection_resource(self, item, **kwargs):
        kwargs = self.get_manage_collection_resource_kwargs(item, **kwargs)
        klass = item.get_resource_class()
        return klass(**kwargs)

hyperadmin.site.register(Collection, CollectionResource, app_name=app_name)

class IndexResource(ReloadCMSSiteMixin, CMSDocumentResource):
    pass

hyperadmin.site.register(Index, IndexResource, app_name=app_name)

class SubsiteResource(ReloadCMSSiteMixin, CMSDocumentResource):
    list_display = ['name', 'url']

hyperadmin.site.register(Subsite, SubsiteResource, app_name=app_name)

class SubsiteResourceDefinitionResource(ReloadCMSSiteMixin, CMSDocumentResource):
    list_display = ['name', 'subsite', 'collection', 'url']

hyperadmin.site.register(SubsiteResourceDefinition, SubsiteResourceDefinitionResource, app_name=app_name)

class RecipeResource(CMSDocumentResource):
    pass

hyperadmin.site.register(BaseRecipe, RecipeResource, app_name=app_name)

