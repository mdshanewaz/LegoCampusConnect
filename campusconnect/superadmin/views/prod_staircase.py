from zzz_lib.zzz_log import zzz_print
from django.contrib import admin
from django import forms

from resumeweb.models import (
    mprod_exp180,
    mprod_exp180_serviceoption,

)


from resumeweb.models import (
    mprod_intprep,
    mprod_intprep_catlist,
    mprod_intprep_serviceoption,

)


from resumeweb.models import (
    mprod_proflevel,
    mprod_proflevel_list,
    mprod_proflevel_serviceoption,
)


from resumeweb.models import (
    mprod_proglang,
    mprod_proglang_list,
    mprod_proglang_serviceoption,

)


from resumeweb.models import (
    mprod_rolebased,
    mprod_rolebased_list,
    mprod_rolebased_serviceoption,

)



from resumeweb.models import (
    mprod_strategy,
    mprod_strategy_taglist,
    mprod_strategy_serviceoption,    

)



from resumeweb.models import (
    mprod_visabased,
    mprod_visabased_list,
    mprod_visabased_serviceoption,


)

from resumeweb.models import (

    mprod_exp180_deliveryoption,
    mprod_intprep_deliveryoption,
    mprod_proflevel_deliveryoption,
    mprod_proglang_deliveryoption,
    mprod_rolebased_deliveryoption,
    mprod_strategy_deliveryoption,
    mprod_visabased_deliveryoption,


)




# Prof Level cat list
###################################
@admin.register(mprod_proflevel_list)
class admin_mprod_proflevel_catlist(admin.ModelAdmin):
    list_display = (
        "id",
        "levelname"
    )




# Prof Level or mprod_proflevel_list
########################################################################################
@admin.register(mprod_proflevel)
class AdminProflevelServlist(admin.ModelAdmin):
    list_display = (
        "sku",
        'title',
        "category",
        "deliverables",
        "golivestatus",
        "trending",
        "homepage_showup"
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)

    fieldsets = (
        ('General', {
            'fields': ('title', 
                'description',
                "trending",
                "homepage_showup",
                "category",
                )
        }),
        ('Pricing', {
            'fields': ('listprice', 'saleprice')
        }),
    )


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(AdminProflevelServlist, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description' or db_field.name == 'title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield




## service options
## *****************************************************************************************
@admin.register(mprod_proflevel_serviceoption)
class AdminProflevelServiceoption(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "listprice",
        "price",
        'products'
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(AdminProflevelServiceoption, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description' or db_field.name == 'name':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield






## delivery options
## *****************************************************************************************
@admin.register(mprod_proflevel_deliveryoption)
class admin_mprod_proflevel_deliveryoption(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "listprice",
        "price",
        "hours_to_cancel_after_payment",
        "hours_to_deliver_after_payment",
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)



