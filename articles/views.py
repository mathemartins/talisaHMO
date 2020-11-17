from django.http import JsonResponse
from django.views import generic
from .models import Article, Comment


class ArticleList(generic.CreateView, generic.ListView):
    fields = ("title", "description", "image_url", "body", "draft")
    model = Article
    context_object_name = 'articles'
    paginate_by = 6
    template_name = "articles/article_list.html"


class ArticleDetail(generic.DetailView):
    model = Article
    template_name = "articles/article_detail.html"

    def get_object(self):
        view_count_obj = super(ArticleDetail, self).get_object()
        view_count_obj.view_count += 1
        view_count_obj.save()
        return view_count_obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article_ = self.get_queryset()  # use to generate related articles if needed
        slug = self.kwargs.get(self.slug_url_kwarg)  # use to get slug and modify slug data
        context['comments'] = Comment.objects.filter(article=self.object)
        # get the reply for a particular comment
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            print(data)
            comment_detail = data["comment_detail"]
            Comment.objects.create(article=self.get_object(), by=request.user, content=comment_detail)
            # comment.save()
            # print(comment.)
            return JsonResponse({'message': 'comment updated'}, status=200)
        return JsonResponse({'message': 'error during comment update'}, status=400)
