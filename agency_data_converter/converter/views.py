from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from vanilla import ListView, CreateView, UpdateView, DeleteView
from .forms import GilKvarForm, FlatForm
from .models import GilKvar, Flat
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import logout

import xlrd
from .formats import yandex


@sensitive_post_parameters()
@csrf_protect
@never_cache
def signin(request, template_name='signin.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           authentication_form=AuthenticationForm,
           current_app=None, extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to
    }

    return TemplateResponse(request, template_name, context)


def dologout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('converter:list'))


class GilKvarList(ListView):
    model = GilKvar

    def get_queryset(self):
        return GilKvar.objects.all().annotate(flatcount=Count('flat'))

    def get_context_data(self, **kwargs):
        context = super(GilKvarList, self).get_context_data(**kwargs)
        if self.kwargs.get('pk', None):
            context['uplpk'] = self.kwargs['pk']
            res = GilKvar.objects.filter(id=self.kwargs['pk']).annotate(flatcount=Count('flat')).first()
            context['uplflatcount'] = res.flatcount
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect_to_login(self.request.get_full_path(), reverse_lazy('converter:signin'))

        return super(GilKvarList, self).dispatch(request, *args, **kwargs)


class GilKvarCreate(CreateView):
    model = GilKvar
    form_class = GilKvarForm
    success_url = reverse_lazy('converter:list')


class GilKvarUpdate(UpdateView):
    model = GilKvar
    form_class = GilKvarForm
    success_url = reverse_lazy('converter:list')


class GilKvarDelete(DeleteView):
    model = GilKvar
    success_url = reverse_lazy('converter:list')


def uploadflats(request, pk):
    uplfile = request.FILES['file']
    with open(uplfile.name, 'wb+') as f:
        for chunk in uplfile.chunks():
            f.write(chunk)

    rb = xlrd.open_workbook(uplfile.name)
    sheet = rb.sheet_by_index(0)
    rowstruct = ('uid', 'housing', 'section', 'floor', 'num_on_floor', 'area', 'price', 'balcony')
    Flat.objects.filter(gilkvar_id=pk).delete()
    for rownum in range(1, sheet.nrows):
        row = sheet.row_values(rownum)
        vals = {'gilkvar_id': pk}
        indx = 0
        for c_el in row:
            if indx < len(rowstruct):
                val = c_el if c_el != '' else None
                if val:
                    vals[rowstruct[indx]] = val
                indx += 1
        flat = Flat(**vals)
        flat.save()

    return HttpResponseRedirect(reverse('converter:list_upl', kwargs={'pk': pk}))


def getdata(request, pk, outputformat):
    data = None
    response = HttpResponse('')
    if outputformat == 'yrl':
        data = yandex.get(Flat.objects.select_related().filter(gilkvar_id=pk))
        response = HttpResponse(data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=yandex.xml'

    return response


class FlatList(ListView):
    model = Flat

    def get_queryset(self):
        return Flat.objects.filter(gilkvar_id=self.kwargs['fk'])

    def get_context_data(self, **kwargs):
        context = super(FlatList, self).get_context_data(**kwargs)
        context['fk'] = self.kwargs['fk']
        return context


class FlatCreate(CreateView):

    model = Flat
    form_class = FlatForm

    def post(self, request, *args, **kwargs):
        post_params = request.POST.copy()

        post_params['gilkvar'] = self.kwargs['fk']

        form = self.get_form(data=post_params, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('converter:flats', kwargs=self.kwargs)


class FlatUpdate(UpdateView):
    model = Flat
    form_class = FlatForm

    def get_success_url(self):
        return reverse('converter:flats', kwargs={'fk': self.object.gilkvar.id})


class FlatDelete(DeleteView):
    model = Flat

    def get_success_url(self):
        return reverse('converter:flats', kwargs={'fk': self.object.gilkvar.id})
