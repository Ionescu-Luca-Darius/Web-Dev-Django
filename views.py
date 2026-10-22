from django.shortcuts import render
from django.http import HttpResponse
from .middleware import ACCESARILE_TOTALE, Accesare


def index(request):
    return render(request, 'index.html')

def info(request):
    acc = request.accesare
    param_data = request.GET.get('data', '')
    rezultat_data = acc.calculeaza_data(param_data)
    return render(request, 'info.html', {'rezultat_data':rezultat_data})

def istoric(request):
    return render(request, 'istoric.html')

def despre(request):
    return render(request, 'despre.html')

def produse(request):
    return render(request, 'in_lucru.html')

def contact(request):
    return render(request, 'in_lucru.html')

def cos_virtual(request):
    return render(request, 'in_lucru.html')

def log(request):
    continut_html = "<h2>Jurnal Accesări (/log)</h2>"
    
    params_log = request.GET
    continut_html += "<section>"
    continut_html += "<h3>Parametri Primiți</h3>"
    continut_html += f"<p><strong>Număr total parametri:</strong> {len(params_log)}</p>"
    if params_log:
        continut_html += "<ul style='list-style-type: square; padding-left: 20px;'>"
        for k, v in params_log.items():
            continut_html += f"<li><strong>{k}</strong>: {v}</li>"
        continut_html += "</ul>"
    else:
        continut_html += "<p><em>Niciun parametru transmis în URL pentru această pagină.</em></p>"
    continut_html += "</section>"

    accesari_copie = list(ACCESARILE_TOTALE)

    ultimele_n = request.GET.get('ultimele')
    if ultimele_n:
        try:
            n = int(ultimele_n)
            accesari_copie = accesari_copie[-n:]
        except ValueError:
            pass
    
    tabel_param = request.GET.get('tabel')
    
    continut_html += "<section>"
    continut_html += "<h3>Lista Accesărilor Înregistrate</h3>"
    if not accesari_copie:
        continut_html += "<p>Nu există accesări înregistrate în sesiune.</p>"
    elif tabel_param:
        if tabel_param.lower() == 'tot':
            coloane = ['id', 'ip_client', 'url', 'pagina', 'data', 'lista_parametri']
        else:
            coloane = [c.strip() for c in tabel_param.split(',')]
            
        continut_html += "<div style='overflow-x: auto;'>"
        continut_html += "<table style='width: 100%; border-collapse: collapse; background-color: #1a1a1a; color: #e0e0e0; margin-top: 15px; border: 1px solid #d4af37;'>"
        continut_html += "<thead><tr style='background-color: #990000; color: #d4af37;'>"
        for col in coloane:
            continut_html += f"<th style='padding: 12px; border: 1px solid #333; text-align: left;'>{col.upper()}</th>"
        continut_html += "</tr></thead><tbody>"
        
        for acc in accesari_copie:
            continut_html += "<tr style='border-bottom: 1px solid #333;'>"
            for col in coloane:
                val = "-"
                if col == 'id':
                    val = acc.id
                elif col == 'ip_client':
                    val = acc.ip_client
                elif col == 'url':
                    val = acc.string_url()
                elif col == 'pagina':
                    val = acc.pagina()
                elif col == 'data':
                    val = acc.data.strftime('%d-%m-%Y %H:%M:%S')
                elif col == 'lista_parametri':
                    val = str(acc.lista_parametri())
                else:
                    val = getattr(acc, col, '-')
                continut_html += f"<td style='padding: 10px; border: 1px solid #333;'>{val}</td>"
            continut_html += "</tr>"
        continut_html += "</tbody></table></div>"
    else:
        continut_html += "<ul style='list-style-type: none; padding: 0;'>"
        for acc in accesari_copie:
            params_str = str(acc.lista_parametri()) if acc.lista_parametri() else "Niciunul"
            continut_html += f"""
            <li style='background-color: #1a1a1a; border: 1px solid #333; border-left: 3px solid #d4af37; margin-bottom: 10px; padding: 12px; border-radius: 4px;'>
                <strong>ID:</strong> {acc.id} | 
                <strong>Pagină:</strong> <span style='color: #d4af37;'>{acc.pagina()}</span><br>
                <strong>URL:</strong> {acc.url}<br>
                <strong>IP Client:</strong> {acc.ip_client} | 
                <strong>Parametri:</strong> {params_str}<br>
                <strong>Data:</strong> {acc.data.strftime('%d-%m-%Y %H:%M:%S')}
            </li>
            """
        continut_html += "</ul>"
    continut_html += "</section>"

    if ACCESARILE_TOTALE:
        frecvente = {}
        for acc in ACCESARILE_TOTALE:
            pag = acc.pagina()
            frecvente[pag] = frecvente.get(pag, 0) + 1
        
        max_accesari = max(frecvente.values())
        min_accesari = min(frecvente.values())
        
        cele_mai_multe = [p for p, c in frecvente.items() if c == max_accesari]
        cele_mai_putine = [p for p, c in frecvente.items() if c == min_accesari]
        
        continut_html += "<section>"
        continut_html += "<h3>Statistici Trafic</h3>"
        continut_html += f"<p><strong>Cea mai puțin accesată pagină:</strong> <span style='color: #d4af37;'>{', '.join(cele_mai_putine)}</span> ({min_accesari} accesări)</p>"
        continut_html += f"<p><strong>Cea mai mult accesată pagină:</strong> <span style='color: #d4af37;'>{', '.join(cele_mai_multe)}</span> ({max_accesari} accesări)</p>"
        continut_html += "</section>"

    return render(request, 'log.html', {'continut_html': continut_html})

def accesare_detalii(request, id):
    try:
        id_int = int(id)
        acc = next((a for a in ACCESARILE_TOTALE if a.id == id_int), None)
    except ValueError:
        acc = None
        
    if not acc:
        return HttpResponse(f"<h1>Accesarea cu ID-ul {id} nu a fost găsită.</h1>", status=404)
        
    html = f"""
    <!DOCTYPE html>
    <html lang="ro">
    <head><meta charset="UTF-8"><title>Detalii Accesare #{acc.id}</title></head>
    <body>
        <h1>Detalii Accesare #{acc.id}</h1>
        <ul>
            <li><strong>ID:</strong> {acc.id}</li>
            <li><strong>IP Client:</strong> {acc.ip_client}</li>
            <li><strong>URL complet:</strong> {acc.string_url()}</li>
            <li><strong>Pagină:</strong> {acc.pagina()}</li>
            <li><strong>Data și ora:</strong> {acc.data.strftime('%d-%m-%Y %H:%M:%S')}</li>
            <li><strong>Parametri:</strong> {acc.lista_parametri()}</li>
        </ul>
        <p><a href="/log">Înapoi la Jurnal</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

