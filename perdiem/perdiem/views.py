"""
:Created: 11 May 2016
:Author: Lucas Connors

"""

from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView


class ConstituentFormView(object):

    def __init__(self, request):
        self.request = request

    def get_initial(self):
        return {}

    def form_valid(self):
        pass


class MultipleFormView(TemplateView):

    constituent_form_views = {}

    def get_context_data(self, **kwargs):
        context = super(MultipleFormView, self).get_context_data(**kwargs)

        context['forms_with_errors'] = []
        for form_name, form_view_class in self.constituent_form_views.iteritems():
            form_view = form_view_class(self.request)
            form_context_name = "{form_name}_form".format(form_name=form_name)
            if form_context_name not in context:
                form_kwargs = {
                    'initial': form_view.get_initial(),
                }
                if self.request.method == 'POST' and self.request.POST.get('action') == form_name:
                    form_kwargs['data'] = self.request.POST
                context[form_context_name] = form_view.form_class(self.request.user, **form_kwargs)
            elif context[form_context_name].errors:
                context['forms_with_errors'].append(form_context_name)

        return context

    def post(self, request, *args, **kwargs):
        try:
            form_name = request.POST['action']
            form_view_class = self.constituent_form_views[form_name]
        except KeyError:
            return HttpResponseBadRequest("Form action unrecognized or unspecified.")

        form_view = form_view_class(request)
        form = form_view.form_class(request.user, request.POST)
        if form.is_valid():
            form_view.form_valid(form)
        else:
            form_context_name = "{form_name}_form".format(form_name=form_name)
            kwargs.update({form_context_name: form,})
        return self.render_to_response(self.get_context_data(**kwargs))
