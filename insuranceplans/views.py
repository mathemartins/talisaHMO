# from django.views import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from analytics.mixins import ObjectViewedMixin

from carts.models import Cart

from .models import Insuranceplan, InsuranceplanFile


class InsuranceplanFeaturedListView(ListView):
    template_name = "insuranceplans/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Insuranceplan.objects.all().featured()


class InsuranceplanFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Insuranceplan.objects.all().featured()
    template_name = "insuranceplans/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Insuranceplan.objects.featured()


class UserInsuranceplanHistoryView(LoginRequiredMixin, ListView):
    template_name = "insuranceplans/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserInsuranceplanHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Insuranceplan, model_queryset=False)
        return views


class InsuranceplanListView(ListView):
    template_name = "insuranceplans/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(InsuranceplanListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(InsuranceplanListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Insuranceplan.objects.all()


def insuranceplan_list_view(request):
    queryset = Insuranceplan.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "insuranceplans/list.html", context)


class InsuranceplanDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Insuranceplan.objects.all()
    template_name = "insuranceplans/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(InsuranceplanDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        # instance = get_object_or_404(Insuranceplan, slug=slug, active=True)
        try:
            instance = Insuranceplan.objects.get(slug=slug, active=True)
        except Insuranceplan.DoesNotExist:
            raise Http404("Not found..")
        except Insuranceplan.MultipleObjectsReturned:
            qs = Insuranceplan.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance


import os
from wsgiref.util import FileWrapper  # this used in django
from mimetypes import guess_type

from django.conf import settings
from orders.models import InsuranceplanPurchase


class InsuranceplanDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = InsuranceplanFile.objects.filter(pk=pk, insuranceplan__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        # permission checks

        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated():
                user_ready = False

        purchased_insuranceplans = Insuranceplan.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            # not free
            purchased_insuranceplans = InsuranceplanPurchase.objects.insuranceplans_by_request(request)
            if download_obj.insuranceplan in purchased_insuranceplans:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path # .url /media/
        # final_filepath = os.path.join(file_root, filepath) # where the file is stored
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/force-download'
        #     gussed_mimetype = guess_type(filepath)[0] # filename.mp4
        #     if gussed_mimetype:
        #         mimetype = gussed_mimetype
        #     response = HttpResponse(wrapper, content_type=mimetype)
        #     response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
        #     response["X-SendFile"] = str(download_obj.name)
        #     return response
        # return redirect(download_obj.get_default_url())


class InsuranceplanDetailView(ObjectViewedMixin, DetailView):
    # queryset = Insuranceplan.objects.all()
    template_name = "insuranceplans/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(InsuranceplanDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Insuranceplan.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Insuranceplan doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Insuranceplan.objects.filter(pk=pk)


def insuranceplan_detail_view(request, pk=None, *args, **kwargs):
    # instance = Insuranceplan.objects.get(pk=pk, featured=True) #id
    # instance = get_object_or_404(Insuranceplan, pk=pk, featured=True)
    # try:
    #     instance = Insuranceplan.objects.get(id=pk)
    # except Insuranceplan.DoesNotExist:
    #     print('no insuranceplan here')
    #     raise Http404("Insuranceplan doesn't exist")
    # except:
    #     print("huh?")

    instance = Insuranceplan.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Insuranceplan doesn't exist")
    # print(instance)
    # qs  = Insuranceplan.objects.filter(id=pk)

    # #print(qs)
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("Insuranceplan doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "insuranceplans/detail.html", context)