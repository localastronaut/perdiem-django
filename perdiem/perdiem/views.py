"""
:Created: 11 May 2016
:Author: Lucas Connors

"""

from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView


class MultipleFormView(TemplateView):

    def get_form_classes(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(MultipleFormView, self).get_context_data(**kwargs)

        for form_name, attrs in self.get_form_classes().iteritems():
            form_context_name = "{form_name}_form".format(form_name=form_name)
            if form_context_name not in context:
                form_kwargs = {
                    'initial': attrs['get_initial'](),
                }
                if self.request.method == 'POST' and self.request.POST.get('action') == form_name:
                    form_kwargs['data'] = self.request.POST
                context[form_context_name] = attrs['class'](self.request.user, **form_kwargs)

        return context

    def post(self, request, *args, **kwargs):
        try:
            form_name = request.POST['action']
            form_attrs = self.get_form_classes()[form_name]
        except KeyError:
            return HttpResponseBadRequest("Form action unrecognized or unspecified.")

        form = form_attrs['class'](self.request.user, request.POST)
        form_context_name = "{form_name}_form".format(form_name=form_name)
        if form.is_valid():
            form_attrs['form_valid'](form)
        else:
            kwargs.update({form_context_name: form,})
        return self.render_to_response(self.get_context_data(**kwargs))
