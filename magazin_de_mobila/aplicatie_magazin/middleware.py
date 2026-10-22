from datetime import datetime

ZILE_RO ={
    'Monday': 'Luni', 'Tuesday': 'Marți', 'Wednesday': 'Miercuri',
    'Thursday': 'Joi', 'Friday': 'Vineri', 'Saturday': 'Sâmbătă', 'Sunday': 'Duminică'
}

LUNI_RO = {
    'January': 'Ianuarie', 'February': 'Februarie', 'March': 'Martie',
    'April': 'Aprilie', 'May': 'Mai', 'June': 'Iunie',
    'July': 'Iulie', 'August': 'August', 'September': 'Septembrie',
    'October': 'Octombrie', 'November': 'Noiembrie', 'December': 'Decembrie'
}

ACCESARILE_TOTALE = []

class Accesare:
    contor = 0
    
    def __init__(self, request):
        Accesare.contor += 1
        self.id = Accesare.contor
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.ip_client = x_forwarded_for.split(',')[0].strip()
        else:
            self.ip_client = request.META.get('REMOTE_ADDR', 'Necunoscut')
        self.request = request
        self.url = request.get_full_path()
        self.parametri = dict(request.GET.lists()) if request.GET else{}
        self.data = datetime.now() 
        
        ACCESARILE_TOTALE.append(self)
        
    def lista_parametri(self):
        if not self.parametri:
            return []
        rezultat = []
        for k, v in self.parametri.items():
            valoare = v[0] if len(v) == 1 else v
            rezultat.append((k, valoare if valoare else None))
        return rezultat  
    
    def string_url(self):
        return self.url  
    
    def pagina(self):
        return self.request.path
    
    def calculeaza_data(self, format=""):
        zi_sapt = ZILE_RO.get(self.data.strftime('%A'), self.data.strftime('%A'))
        luna = LUNI_RO.get(self.data.strftime('%B'), self.data.strftime('%B'))
        zi_luna = self.data.strftime('%d').lstrip('0')
        an = self.data.strftime('%Y')
        
        if format == "zi":
            continut = f"{zi_luna} {luna} {an}"
        elif format == "timp":
            continut = self.data.strftime('%H:%M:%S')
        else:
            continut = f"{zi_sapt}, {zi_luna} {luna} {an}"
        
        return f"<section><h2>Data si ora</h2><p>{continut}</p></section>"
        
    def __str__(self):
        zi_sapt = ZILE_RO.get(self.data.strftime('%A'), self.data.strftime('%A'))
        luna = LUNI_RO.get(self.data.strftime('%B'), self.data.strftime('%B'))
        zi_luna = self.data.strftime('%d').lstrip('0')
        an = self.data.strftime('%Y')
        data_formatata = f"{zi_sapt}, {zi_luna} {luna} {an}"
        
        return (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"data: {data_formatata}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )

class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):    
        accesare = Accesare(request)
        request.accesare = accesare
        request.client_ip = accesare.ip_client
        print(accesare)
        response = self.get_response(request)
        return response
