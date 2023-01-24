from django.urls import path, re_path, include

from products import views
from products.views import CategoryAutoComplete, UomAutoComplete, ProductAutoComplete, UnitAutoComplete, PvAutoComplete, \
    ColorAutoComplete,BrandAutoComplete, HsnAutoComplete

app_name = "products"

urlpatterns = [
    re_path(r'^create-category/$', views.create_category, name='create_category'),
    re_path(r'^category/(?P<pk>.*)$', views.category, name='category'),
    re_path(r'^categories/$', views.categories, name='categories'),
    re_path(r'^edit-category/(?P<pk>.*)$', views.edit_category, name='edit_category'),
    re_path(r'^delete/(?P<pk>.*)$', views.delete_category, name='delete_category'),

    re_path(r'^create-product/$', views.create_product, name='create_product'),
    re_path(r'^product/(?P<pk>.*)$', views.product, name='product'),
    re_path(r'^products/$', views.products, name='products'),
    re_path(r'^edit-product/(?P<pk>.*)$', views.edit_product, name='edit_product'),
    re_path(r'^delete-product/(?P<pk>.*)$', views.delete_product, name='delete_product'),

    re_path(r'^create-uom/$', views.create_uom, name='create_uom'),
    re_path(r'^uom/(?P<pk>.*)$', views.uom, name='uom'),
    re_path(r'^uoms/$', views.uoms, name='uoms'),
    re_path(r'^edit-uom/(?P<pk>.*)$', views.edit_uom, name='edit_uom'),
    re_path(r'^delete-uom/(?P<pk>.*)$', views.delete_uom, name='delete_uom'),

    re_path(r'^create-unit/$', views.create_unit, name='create_unit'),
    re_path(r'^unit/(?P<pk>.*)$', views.unit, name='unit'),
    re_path(r'^units/$', views.units, name='units'),
    re_path(r'^edit-unit/(?P<pk>.*)$', views.edit_unit, name='edit_unit'),
    re_path(r'^delete-unit/(?P<pk>.*)$', views.delete_unit, name='delete_unit'),

    re_path(r'^create-product-variant/(?P<pk>.*)$', views.create_product_variant, name='create_product_variant'),
    re_path(r'^product-variant/(?P<pk>.*)$', views.product_variant, name='product_variant'),
    re_path(r'^product-variants/(?P<pk>.*)$', views.product_variants, name='product_variants'),
    re_path(r'^edit-product-variant/(?P<pk>.*)$', views.edit_product_variant, name='edit_product_variant'),
    re_path(r'^delete-product-variant/(?P<pk>.*)$', views.delete_product_variant, name='delete_product_variant'),
    re_path(r'^set-default-product-variant/(?P<pk>.*)$', views.set_default_product_variant, name='set_default_product_variant'),

    re_path(r'^create-product-image/(?P<pk>.*)$', views.create_product_image, name='create_product_image'),
    re_path(r'^product-image/(?P<pk>.*)$', views.product_image, name='product_image'),
    re_path(r'^product-images/$', views.product_images, name='product_images'),
    re_path(r'^variant-images/(?P<pk>.*)$', views.variant_images, name='variant_images'),
    re_path(r'^edit-product-image/(?P<pk>.*)$', views.edit_product_image, name='edit_product_image'),
    re_path(r'^delete-product-image/(?P<pk>.*)$', views.delete_product_image, name='delete_product_image'),

    # pfc means Product For Occassion
    re_path(r'^create-pfo/$', views.create_pfo, name='create_pfo'),
    re_path(r'^pfo/(?P<pk>.*)$', views.pfo, name='pfo'),
    re_path(r'^pfos/$', views.pfos, name='pfos'),
    re_path(r'^edit-pfo/(?P<pk>.*)$', views.edit_pfo, name='edit_pfo'),
    re_path(r'^delete-pfo/(?P<pk>.*)$', views.delete_pfo, name='delete_pfo'),

    re_path(r'^create-color/$', views.create_color, name='create_color'),
    re_path(r'^colors/$', views.colors, name='colors'),
    re_path(r'^edit-color/(?P<pk>.*)$', views.edit_color, name='edit_color'),
    re_path(r'^delete-color/(?P<pk>.*)$', views.delete_color, name='delete_color'),

    re_path(r'^create-brand/$', views.create_brand, name='create_brand'),
    re_path(r'^brands/$', views.brands, name='brands'),
    re_path(r'^edit-brand/(?P<pk>.*)$', views.edit_brand, name='edit_brand'),
    re_path(r'^delete-brand/(?P<pk>.*)$', views.delete_brand, name='delete_brand'),

    re_path(r'^create-hsn/$', views.create_hsn, name='create_hsn'),
    re_path(r'^hsns/$', views.hsns, name='hsns'),
    re_path(r'^edit-hsn/(?P<pk>.*)$', views.edit_hsn, name='edit_hsn'),
    re_path(r'^hsn/(?P<pk>.*)$', views.hsn, name='hsn'),
    re_path(r'^delete-hsn/(?P<pk>.*)$', views.delete_hsn, name='delete_hsn'),

    re_path(r'^get-hsn-suggestions/$', views.get_hsn_suggestions, name='get_hsn_suggestions'),
    re_path(r'^get-asc-suggestions/$', views.get_asc_suggestions, name='get_asc_suggestions'),

    re_path(r'^category-autocomplete/$', CategoryAutoComplete.as_view(), name='category_autocomplete', ),
    re_path(r'^uom-autocomplete/$', UomAutoComplete.as_view(), name='uom_autocomplete', ),
    re_path(r'^product-autocomplete/$', ProductAutoComplete.as_view(), name='product_autocomplete', ),
    re_path(r'^unit-autocomplete/$', UnitAutoComplete.as_view(), name='unit_autocomplete', ),
    re_path(r'^unit-prod-variant-autocomplete/$', PvAutoComplete.as_view(), name='pv_autocomplete', ),
    re_path(r'^color-autocomplete/$', ColorAutoComplete.as_view(), name='color_autocomplete', ),
    re_path(r'^brand-autocomplete/$', BrandAutoComplete.as_view(), name='brand_autocomplete', ),
    re_path(r'^hsn-autocomplete/$', HsnAutoComplete.as_view(), name='hsn_autocomplete', ),

]
