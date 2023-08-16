from dal import autocomplete

from authApp.models.clientes import Cliente


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cliente.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs
