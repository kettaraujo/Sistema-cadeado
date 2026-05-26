from django.shortcuts import render
from consulta.forms import ConsultaCadeadoForm
from consulta.services import buscar_cadeado_por_id, abrir_cadeado_por_guid


def buscar_cadeado(request):
    resultado = None
    resultado_abertura = None

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'buscar':
            form = ConsultaCadeadoForm(request.POST)

            if form.is_valid():
                id_cadeado = form.cleaned_data['id_cadeado']
                resultado = buscar_cadeado_por_id(id_cadeado)

        elif acao == 'abrir':
            form = ConsultaCadeadoForm()

            asset_guid = request.POST.get('asset_guid')

            if asset_guid:
                resultado_abertura = abrir_cadeado_por_guid(asset_guid)
            else:
                resultado_abertura = {
                    "sucesso": False,
                    "mensagem": "Não foi possível abrir: FAssetGUID não encontrado."
                }

    else:
        form = ConsultaCadeadoForm()

    return render(request, 'consulta/buscar.html', {
        'form': form,
        'resultado': resultado,
        'resultado_abertura': resultado_abertura
    })