from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, ModelForm, Textarea, Select
from import_export.admin import ImportExportModelAdmin
from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from .models import Country, Continent, KitchenSink, Category, City, \
    Microwave, Fridge, WysiwygEditor, ReversionedItem, ImportExportItem,Invoice, Inv_Item,Product, Book, Author
from suit.admin import SortableTabularInline, SortableModelAdmin, \
    SortableStackedInline
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
    EnclosedInput, LinkedSelect, AutosizedTextarea
from mptt.admin import MPTTModelAdmin


    
# Inlines for KitchenSink
class CountryInlineForm(ModelForm):
    class Meta:
        widgets = {
            'code': TextInput(attrs={'class': 'input-mini'}),
            'population': TextInput(attrs={'class': 'input-medium'}),
            'independence_day': SuitDateWidget,
        }


class CountryInline(SortableTabularInline):
    form = CountryInlineForm
    model = Country
    fields = ('name', 'code', 'population',)
    extra = 1
    verbose_name_plural = 'Countries (Sortable example)'
    sortable = 'order'


class ContinentAdmin(SortableModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    inlines = (CountryInline,)
    sortable = 'order'

    def countries(self, obj):
        return len(obj.country_set.all())

    def suit_row_attributes(self, obj):
        class_map = {
            'Europe': 'success',
            'South America': 'warning',
            'North America': 'success',
            'Africa': 'error',
            'Australia': 'warning',
            'Asia': 'info',
            'Antarctica': 'info',
        }

        css_class = class_map.get(obj.name)
        if css_class:
            return {'class': css_class}

    def suit_cell_attributes(self, obj, column):
        if column == 'countries':
            return {'class': 'text-center'}
        elif column == 'right_aligned':
            return {'class': 'text-right muted'}


admin.site.register(Continent, ContinentAdmin)

class CityInlineForm(ModelForm):
    class Meta:
        widgets = {
            'area': EnclosedInput(prepend='icon-globe', append='km<sup>2</sup>',
                                  attrs={'class': 'input-small'}),
            'population': EnclosedInput(append='icon-user',
                                        attrs={'class': 'input-small'}),
        }


class CityInline(admin.TabularInline):
    form = CityInlineForm
    model = City
    extra = 3
    verbose_name_plural = 'Cities'
    suit_classes = 'suit-tab suit-tab-cities'


class CountryForm(ModelForm):
    class Meta:
        widgets = {
            'code': TextInput(attrs={'class': 'input-mini'}),
            'independence_day': SuitDateWidget,
            'area': EnclosedInput(prepend='icon-globe', append='km<sup>2</sup>',
                                  attrs={'class': 'input-small'}),
            'population': EnclosedInput(prepend='icon-user',
                                        append='<input type="button" '
                                               'class="btn" onclick="window'
                                               '.open(\'https://www.google'
                                               '.com/\')" value="Search">',
                                        attrs={'class': 'input-small'}),
            'description': AutosizedTextarea,
            'architecture': AutosizedTextarea(attrs={'class': 'span5'}),
        }


class CountryAdmin(ModelAdmin):
    form = CountryForm
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent',)
    date_hierarchy = 'independence_day'
    list_select_related = True

    inlines = (CityInline,)

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['name', 'continent', 'code', 'independence_day']
        }),
        ('Statistics', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'EnclosedInput widget examples',
            'fields': ['area', 'population']}),
        ('Autosized textarea', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'AutosizedTextarea widget example - adapts height '
                           'based on user input',
            'fields': ['description']}),
        ('Architecture', {
            'classes': ('suit-tab suit-tab-cities',),
            'description': 'Tabs can contain any fieldsets and inlines',
            'fields': ['architecture']}),
    ]

    suit_form_tabs = (('general', 'General'), ('cities', 'Cities'),
                      ('flag', 'Flag'), ('info', 'Info on tabs'))

    suit_form_includes = (
        ('admin/examples/country/tab_disclaimer.html', 'middle', 'cities'),
        ('admin/examples/country/tab_flag.html', '', 'flag'),
        ('admin/examples/country/tab_info.html', '', 'info'),
    )


admin.site.register(Country, CountryAdmin)

class CountryFilter(SimpleListFilter):
    """
    List filter example that shows only referenced(used) values
    """
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        # You can use also "Country" instead of "model_admin.model"
        # if this is not direct relation
        countries = set([c.country for c in model_admin.model.objects.all()])
        return [(c.id, c.name) for c in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__id__exact=self.value())
        else:
            return queryset


class KitchenSinkForm(ModelForm):
    class Meta:
        widgets = {
            'multiple2': TextInput(attrs={'class': 'input-small'}),
            'date': AdminDateWidget(attrs={'class': 'vDateField input-small'}),
            'date_widget': SuitDateWidget,
            'datetime_widget': SuitSplitDateTimeWidget,
            'textfield': AutosizedTextarea(attrs={'rows': '2'}),
            'linked_foreign_key': LinkedSelect,

            'enclosed1': EnclosedInput(append='icon-plane',
                                       attrs={'class': 'input-medium'}),
            'enclosed2': EnclosedInput(prepend='icon-envelope',
                                       append='<input type="button" '
                                              'class="btn" value="Send">',
                                       attrs={'class': 'input-medium'}),
        }


class FridgeInlineForm(ModelForm):
    class Meta:
        widgets = {
            'description': AutosizedTextarea(
                attrs={'class': 'input-medium', 'rows': 2,
                       'style': 'width:95%'}),
            'type': Select(attrs={'class': 'input-small'}),
        }

class FridgeInline(SortableTabularInline):
    model = Fridge
    form = FridgeInlineForm
    extra = 1
    verbose_name_plural = 'Fridges (Tabular inline)'


class MicrowaveInline(SortableStackedInline):
    model = Microwave
    extra = 1
    verbose_name_plural = 'Microwaves (Stacked inline)'


class KitchenSinkAdmin(admin.ModelAdmin):
    raw_id_fields = ()
    form = KitchenSinkForm
    inlines = (FridgeInline,MicrowaveInline)
    #inlines = (FridgeInline, MicrowaveInline)
    search_fields = ['name']
    radio_fields = {"horizontal_choices": admin.HORIZONTAL,'vertical_choices': admin.VERTICAL}
    #list_editable = ('boolean', )
    list_filter = ('choices', 'date', CountryFilter)
    readonly_fields = ('readonly_field',)
    raw_id_fields = ('raw_id_field',)
    
admin.site.register(KitchenSink, KitchenSinkAdmin)


class ProductAdmin(admin.ModelAdmin):
    fields = ('p_name','p_price',)
    verbose_name_plural = 'Products'
    
admin.site.register(Product)

class Inv_itemInline(admin.TabularInline):
    model = Inv_Item
    #total = lambda self: (self.price / self.quantity) 
    #readonly_fields = ('total',)
    readonly_fields = ('get_cost', )
    fields =('product','quantity','price','total',)
    template = 'admin/tabular.html'
    
    def get_cost(self, obj):
        if obj.quantity != None and  obj.price != None :
            x = float(obj.quantity)* float(obj.price)
        #obj.save()
        else :
            x = 0
        return x
    get_cost.short_description = 'Total'

    verbose_name = 'Invoice Item'
    verbose_name_plural = 'Invoice Items'
    

class InvoiceAdmin(admin.ModelAdmin):
    raw_id_fields = ()
    #form = InvoiceForm
    inlines = (Inv_itemInline,)
    verbose_name_plural = 'Invoices'

admin.site.register(Invoice, InvoiceAdmin)

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]
#admin.site.register(Author,AuthorAdmin)
