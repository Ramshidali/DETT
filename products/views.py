import datetime
import json

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from general.functions import get_auto_id, send_sms
from general.decorators import ajax_required
from products.forms import ProductCategoryForm, ProductForm, UomForm, UnitForm, PvForm, ProductImageForm, \
    ProductForOccassionForm, ColorForm, BrandForm, GstCodesForm
from products.models import ProductCategory, Product, UnitOfMeasurement, Unit, ProductVariant, ProductImage, \
    ProductForOccassion, ProductColor, Brand, GstCodes

AGE = (
    ("10", "0-5"),
    ("20", "5-10"),
    ("30", "10-15"),
)

GENDER = (
    ("10", "Male"),
    ("20", "Female"),
    ("30", "Other"),
)


class HsnAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return GstCodes.objects.none()

        items = GstCodes.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(code__icontains=query) | Q(type__icontains=query))

        return items


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ProductCategory.objects.none()

        items = ProductCategory.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(category_name__icontains=query))

        return items


class UomAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return UnitOfMeasurement.objects.none()

        items = UnitOfMeasurement.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(unit_of_measurement__icontains=query))

        return items


class ProductAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        items = Product.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query))

        return items


class UnitAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Unit.objects.none()

        items = Unit.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(unit__icontains=query))

        return items


class PvAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ProductVariant.objects.none()

        items = ProductVariant.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(title__icontains=query))

        return items


class ColorAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ProductColor.objects.none()

        items = ProductColor.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(color__icontains=query))

        return items


class BrandAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Brand.objects.none()

        items = Brand.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(brand__icontains=query))

        return items


@login_required
def create_category(request):
    if request.method == "POST":
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ProductCategory)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Category Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:category', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = ProductCategoryForm()
        send_sms()
        context = {
            "form": form,
            "title": "Create Product Category",
            "redirect": True,
            "url": reverse("products:create_category"),
            "is_category": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/category/entry.html', context)


@login_required
def category(request, pk):
    instance = get_object_or_404(ProductCategory.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.category_name,
        "instance": instance,
        "is_category": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/category/category.html', context)


@login_required
def categories(request):
    instances = ProductCategory.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(category_name__icontains=query))
    context = {
        "title": "Categories",
        "instances": instances,
        "is_category": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/category/categories.html', context)


@login_required
def edit_category(request, pk):
    instance = get_object_or_404(ProductCategory.objects.filter(pk=pk))
    if request.method == "POST":
        form = ProductCategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Category Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:category', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = ProductCategoryForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Category",
            "redirect": True,
            "url": reverse("products:edit_category", kwargs={"pk": pk}),
            "pk": pk,
            "is_category": True,
            "is_product": True,
            "instance": instance,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/category/entry.html', context)


@login_required
def delete_category(request, pk):
    ProductCategory.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Category Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:categories')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_uom(request):
    if request.method == "POST":
        form = UomForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(UnitOfMeasurement)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Unit Of Measurement Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:uom', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = UomForm()
        context = {
            "form": form,
            "title": "Create Unit Of Measurement",
            "redirect": True,
            "url": reverse("products:create_uom"),
            "is_uom": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/uom/entry.html', context)


@login_required
def uom(request, pk):
    instance = get_object_or_404(UnitOfMeasurement.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.unit_of_measurement,
        "instance": instance,
        "is_uom": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/uom/uom.html', context)


@login_required
def edit_uom(request, pk):
    instance = get_object_or_404(UnitOfMeasurement.objects.filter(pk=pk))
    if request.method == "POST":
        form = UomForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Unit Of Measurement Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:uom', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = UomForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit UOM",
            "redirect": True,
            "url": reverse("products:edit_uom", kwargs={"pk": pk}),
            "pk": pk,
            "is_uom": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/uom/entry.html', context)


@login_required
def uoms(request):
    instances = UnitOfMeasurement.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(unit_of_measurement__icontains=query))
    context = {
        "title": "Unit of measurements",
        "instances": instances,
        "is_uom": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/uom/uoms.html', context)


@login_required
def delete_uom(request, pk):
    UnitOfMeasurement.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "UOM Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:uoms')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_unit(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Unit)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Unit Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:unit', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = UnitForm()
        context = {
            "form": form,
            "title": "Create Units",
            "redirect": True,
            "url": reverse("products:create_unit"),
            "is_unit": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/unit/entry.html', context)


@login_required
def unit(request, pk):
    instance = get_object_or_404(Unit.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.unit,
        "instance": instance,
        "is_unit": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/unit/unit.html', context)


@login_required
def units(request):
    instances = Unit.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(unit__icontains=query))
    context = {
        "title": "Units",
        "instances": instances,
        "is_unit": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/unit/units.html', context)


@login_required
def edit_unit(request, pk):
    instance = get_object_or_404(Unit.objects.filter(pk=pk))
    if request.method == "POST":
        form = UnitForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Unit Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:unit', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = UnitForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Unit",
            "redirect": True,
            "url": reverse("products:edit_unit", kwargs={"pk": pk}),
            "pk": pk,
            "is_uom": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/unit/entry.html', context)


@login_required
def delete_unit(request, pk):
    Unit.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "UNIT Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:units')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():

            data = form.save(commit=False)
            code_type = request.POST.get("code_type")
            code = request.POST.get("code")
            igst = request.POST.get("igst")
            cgst = request.POST.get("cgst")
            sgst = request.POST.get("sgst")

            # print("The hsn types are ==>", code_type)

            gst_code_instances = None
            if GstCodes.objects.filter(type=code_type, code=code).exists():
                gst_code_instances = GstCodes.objects.get(type=code_type, code=code)

            else:
                gst_code_instances = GstCodes.objects.create(
                    auto_id=get_auto_id(GstCodes),
                    creator=request.user,
                    updater=request.user,
                    type=code_type,
                    code=code,
                    igst_rate=igst,
                    cgst_rate=cgst,
                    sgst_rate=sgst,
                )

            data.gst_code = gst_code_instances
            data.auto_id = get_auto_id(Product)
            data.creator = request.user
            data.updater = request.user
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Product Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:product', kwargs={"pk": data.pk})
            })
        else:
            print(product_variant_formset.errors)
            return JsonResponse({'error': True,
                                 'message': product_variant_formset.errors,
                                 'title': "Error Occoured"
                                 })

    else:
        form = ProductForm()
        context = {
            "form": form,
            "title": "Create Product",
            "redirect": True,
            "url": reverse("products:create_product"),
            "is_pro": True,
            "is_product": True,
            "is_create": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
        }

        return render(request, 'products/products/entry.html', context)


@login_required
def product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    pv_items = ProductVariant.objects.filter(product=instance, is_deleted=False)[:4]
    context = {
        "title": "Product : " + instance.name,
        "pv_items": pv_items,
        "instance": instance,
        "is_pro": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/products/product.html', context)


@login_required
def products(request):
    instances = Product.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(name__icontains=query))
    context = {
        "title": "Products",
        "instances": instances,
        "is_pro": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/products/products.html', context)


@login_required
def edit_product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk, is_deleted=False))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()

            pk = data.pk
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Product Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:product', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = ProductForm(instance=instance)
        context = {
            "form": form,

            "title": "Edit Product",
            "redirect": True,
            "url": reverse("products:edit_product", kwargs={"pk": pk}),
            "pk": pk,
            "is_pro": True,
            "is_product": True,
            "instance": instance,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/products/entry.html', context)


@login_required
def delete_product(request, pk):
    Product.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:products')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_product_variant(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = PvForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ProductVariant)
            data.opening_stock = form.cleaned_data['stock']
            data.product = product
            data.save()
            return JsonResponse({
                "status": "true",
                'error': False, 'message': 'Product variant Created',
                "redirect": 'true',
                "redirect_url": reverse('products:create_product_variant', kwargs={"pk": pk})
            })
        else:
            print(form.errors)
            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = PvForm()
        context = {
            "form": form,
            "title": f"Create Product Variants of : {product.name}",
            "redirect": True,
            "url": reverse("products:create_product_variant", kwargs={"pk": pk}),
            "is_pv": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }
        # pv means product variation
        return render(request, 'products/pv/entry.html', context)


@login_required
def product_variant(request, pk):
    instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.title,
        "instance": instance,
        "is_pv": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/pv/pv.html', context)


@login_required
def product_variants(request, pk):
    product = Product.objects.get(pk=pk)

    instances = ProductVariant.objects.filter(product=product, is_deleted=False)

    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(title__icontains=query))
    context = {
        "title": "Product Variations",
        "instances": instances,
        "is_pv": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/pv/pvs.html', context)


@login_required
def edit_product_variant(request, pk):
    instance = get_object_or_404(ProductVariant.objects.filter(pk=pk))
    if request.method == "POST":
        form = PvForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'message': 'PV Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:product_variant', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = PvForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit UOM",
            "redirect": True,
            "url": reverse("products:edit_product_variant", kwargs={"pk": pk}),
            "pk": pk,
            "is_uom": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/pv/entry.html', context)


@login_required
def delete_product_variant(request, pk):
    ProductVariant.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "PV Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:product_variants')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_product_image(request, pk):
    product_variant_instances = ProductVariant.objects.get(pk=pk)
    ProductVariantImageFormset = formset_factory(ProductImageForm, extra=1)

    if request.method == "POST":
        product_image_formset = ProductVariantImageFormset(request.POST, request.FILES, prefix="product_image_formset")
        if product_image_formset.is_valid():
            creator = request.user
            updater = request.user

            for item in product_image_formset:
                print(item)
                auto_id = get_auto_id(ProductImage)

                feautured_image = item.cleaned_data['feautured_image']
                ProductImage.objects.create(
                    product_variant=product_variant_instances,
                    feautured_image=feautured_image,
                    creator=creator,
                    updater=updater,
                    auto_id=auto_id,
                )

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Product Variant Image Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:variant_images', kwargs={"pk": pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': "product_image_formset.error"})

    else:
        product_image_formset = ProductVariantImageFormset(prefix="product_image_formset")
        context = {
            "product_image_formset": product_image_formset,
            "title": "Create Product Variant Image",
            "redirect": True,
            "url": reverse("products:create_product_image", kwargs={"pk": pk}),
            "is_prod_img": True,
            "is_product": True,
            "pk": pk,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/prod_image/entry.html', context)


@login_required
def product_image(request, pk):
    instance = get_object_or_404(ProductImage.objects.filter(pk=pk))
    context = {
        "instance": instance,
        "is_prod_img": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/prod_image/prod_image.html', context)


@login_required
def product_images(request):
    instances = ProductImage.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(product_variant__title__icontains=query))
    context = {
        "title": "Product Variant Images",
        "instances": instances,
        "is_prod_img": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/prod_image/prod_images.html', context)


@login_required
def edit_product_image(request, pk):
    instance = get_object_or_404(ProductImage.objects.filter(pk=pk))

    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Product Variant Image Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:product_image', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = ProductImageForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Product Image",
            "redirect": True,
            "url": reverse("products:edit_product_image", kwargs={"pk": pk}),
            "pk": pk,
            "is_category": True,
            "is_product": True,
            "instance": instance,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/prod_image/edit.html', context)


@login_required
def delete_product_image(request, pk):
    ProductImage.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Image Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:product_images')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_pof(request):
    if request.method == "POST":
        form = UomForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(UnitOfMeasurement)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Category Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:uom', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = UomForm()
        context = {
            "form": form,
            "title": "Create Unit Of Measurement",
            "redirect": True,
            "url": reverse("products:create_uom"),
            "is_uom": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/uom/entry.html', context)


@login_required
def create_pfo(request):
    if request.method == "POST":
        form = ProductForOccassionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(ProductForOccassion)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Product For Occassion Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:pfo', kwargs={"pk": data.pk})
            })
        else:
            print(form.errors)
            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = ProductForOccassionForm()
        context = {
            "form": form,
            "title": "Create Product For Occassion",
            "redirect": True,
            "url": reverse("products:create_pfo"),
            "is_pfo": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/pfo/entry.html', context)


@login_required
def pfos(request):
    instances = ProductForOccassion.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(occassion__icontains=query))
    context = {
        "title": "Occassion",
        "instances": instances,
        "is_pfo": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/pfo/pfos.html', context)


@login_required
def pfo(request, pk):
    instance = get_object_or_404(ProductForOccassion.objects.filter(pk=pk))
    context = {
        "title": "Product For Occassion",
        "instance": instance,
        "is_pfo": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/pfo/pfo.html', context)


@login_required
def edit_pfo(request, pk):
    instance = get_object_or_404(ProductForOccassion.objects.filter(pk=pk))
    if request.method == "POST":
        form = ProductForOccassionForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Product For Occassion Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:pfo', kwargs={"pk": pk})
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = ProductForOccassionForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit UOM",
            "redirect": True,
            "url": reverse("products:edit_pfo", kwargs={"pk": pk}),
            "pk": pk,
            "is_pfo": True,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/pfo/entry.html', context)


@login_required
def delete_pfo(request, pk):
    ProductForOccassion.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "PFO Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:pfos')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_color(request):
    if request.method == "POST":
        form = ColorForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Color Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:colors')
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = ColorForm()
        context = {
            "form": form,
            "title": "Create Color",
            "redirect": True,
            "url": reverse("products:create_color"),
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/color/entry.html', context)


@login_required
def edit_color(request, pk):
    instance = get_object_or_404(ProductColor.objects.filter(pk=pk))
    if request.method == "POST":
        form = ColorForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Color Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:colors')
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = ColorForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Color",
            "redirect": True,
            "url": reverse("products:edit_color", kwargs={"pk": pk}),
            "pk": pk,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/color/entry.html', context)


@login_required
def colors(request):
    instances = ProductColor.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(color__icontains=query))
    context = {
        "title": "Colors",
        "instances": instances,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/color/colors.html', context)


@login_required
def delete_color(request, pk):
    ProductColor.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Color Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:colors')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'Brand Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:brands')
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = BrandForm()
        context = {
            "form": form,
            "title": "Create Brand",
            "redirect": True,
            "url": reverse("products:create_brand"),
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/brand/entry.html', context)


@login_required
def edit_brand(request, pk):
    instance = get_object_or_404(Brand.objects.filter(pk=pk))
    if request.method == "POST":
        form = BrandForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'Brand Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:brands')
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = BrandForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Brand",
            "redirect": True,
            "url": reverse("products:edit_brand", kwargs={"pk": pk}),
            "pk": pk,
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/brand/entry.html', context)


@login_required
def brands(request):
    instances = Brand.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(brand__icontains=query))
    context = {
        "title": "Brands",
        "instances": instances,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/brand/brands.html', context)


@login_required
def delete_brand(request, pk):
    Brand.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Brand Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:brands')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_hsn(request):
    if request.method == "POST":
        form = GstCodesForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(GstCodes)
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Created',
                'message': 'HSN Successfully Created',
                "redirect": 'true',
                "redirect_url": reverse('products:hsns')
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = GstCodesForm()
        context = {
            "form": form,
            "title": "Create HSN Code",
            "redirect": True,
            "url": reverse("products:create_hsn"),
            "is_product": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/hsn/entry.html', context)


@login_required
def hsns(request):
    instances = GstCodes.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(code__icontains=query))
    context = {
        "title": "Hsn Codes",
        "instances": instances,
        "is_hsn": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/hsn/hsns.html', context)


@login_required
def delete_hsn(request, pk):
    GstCodes.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "GstCode  Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:hsns')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_hsn(request, pk):
    instance = get_object_or_404(GstCodes.objects.filter(pk=pk))
    if request.method == "POST":
        form = GstCodesForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Sucessfully Updated',
                'message': 'GstCodes Successfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('products:hsns')
            })

        else:

            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = GstCodesForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit HSN Code " + "" + instance.code,
            "redirect": True,
            "url": reverse("products:edit_hsn", kwargs={"pk": pk}),
            "pk": pk,
            "is_product": True,
            "is_hsn": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'products/hsn/entry.html', context)


@login_required
def hsn(request, pk):
    instance = get_object_or_404(GstCodes.objects.filter(pk=pk))
    context = {
        "title": "HSN Code" + instance.code,
        "instance": instance,
        "is_pfo": True,
        "is_product": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/hsn/hsn.html', context)


def get_hsn_suggestions(request):
    code = request.GET.get('code')

    response_data = {}
    try:

        hsn_code_instance = GstCodes.objects.filter(type="hsn", code__contains=code).first()
        if hsn_code_instance:
            response_data = {
                "status": True,
                "data": "yes",
                "code": hsn_code_instance.code,
                "sgst": str(hsn_code_instance.sgst_rate),
                "cgst": str(hsn_code_instance.cgst_rate),
                "igst": str(hsn_code_instance.igst_rate)

            }
        else:
            response_data = {
                "status": True,
                "code": "No Suggestions"
            }

    except Exception as e:
        print(e)
        response_data = {
            "status": "false",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def get_asc_suggestions(request):
    code = request.GET.get('code')

    response_data = {}
    try:

        sac_code_instance = GstCodes.objects.filter(type="asc", code__contains=code).first()
        if sac_code_instance:
            response_data = {
                "status": True,
                "data": "yes",
                "code": sac_code_instance.code,
                "sgst": str(sac_code_instance.sgst_rate),
                "cgst": str(sac_code_instance.cgst_rate),
                "igst": str(sac_code_instance.igst_rate)
            }
        else:
            response_data = {
                "status": True,
                "code": "No Suggestions"
            }

    except Exception as e:
        print(e)
        response_data = {
            "status": "false",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def variant_images(request, pk):
    instances = ProductImage.objects.filter(is_deleted=False, product_variant__pk=pk)
    query = request.GET.get('q')

    context = {
        "title": "Product Variant Images",
        "instances": instances,
        "is_prod_img": True,
        "is_product": True,
        
        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'products/prod_image/prod_images.html', context)


@login_required
def set_default_product_variant(request, pk):
    product_variant_instances = ProductVariant.objects.get(pk=pk)
    product = product_variant_instances.product

    if ProductVariant.objects.filter(is_default=True, product=product).exists():
        ProductVariant.objects.filter(is_default=True, product=product).update(is_default=False)

    instances = ProductVariant.objects.get(pk=pk)
    instances.is_default = True
    instances.save()

    response_data = {
        "status": "true",
        "title": "Default Variant Updated",
        "message": "Default Variant Successfully Updated.",
        "redirect": "true",
        "redirect_url": reverse('products:product_variants', kwargs={'pk': pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
