def get_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if estado_id:
        municipios = Municipio.objects.filter(estado_id=estado_id)
    for municipio in municipios:
        options += '<option value="%s">%s</option>' % (
            municipio.pk,
            municipio.municipio
        )
    response = {}
    response['municipios'] = options
    return JsonResponse(response)

def get_localidades(request):
    municipio_id = request.GET.get('municipio_id')
    localidades = Localidad.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if municipio_id:
        localidades = Localidad.objects.filter(municipio_id=municipio_id)
    for localidad in localidades:
        options += '<option value="%s">%s</option>' % (
            localidad.pk,
            localidad.localidad
        )
    response = {}
    response['localidades'] = options
    return JsonResponse(response)
