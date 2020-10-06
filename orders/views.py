from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView

from .models import Order, InsuranceplanPurchase


class OrderListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        # return Order.objects.get(id=self.kwargs.get('id'))
        # return Order.objects.get(slug=self.kwargs.get('slug'))
        qs = Order.objects.by_request(
            self.request
        ).filter(
            order_id=self.kwargs.get('order_id')
        )
        if qs.count() == 1:
            return qs.first()
        raise Http404


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'orders/library.html'

    def get_queryset(self):
        return InsuranceplanPurchase.objects.insuranceplans_by_request(self.request)  # .by_request(self.request).digital()


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            insuranceplan_id = request.GET.get('insuranceplan_id', None)
            if insuranceplan_id is not None:
                insuranceplan_id = int(insuranceplan_id)
                ownership_ids = InsuranceplanPurchase.objects.insuranceplans_by_id(request)
                if insuranceplan_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404