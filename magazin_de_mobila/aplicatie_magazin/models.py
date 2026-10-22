from django.db import models

class Ambalaj(models.Model):
    class Meta:
        verbose_name_plural = "Ambalaje"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nivel_rezistenta__lte=10) & models.Q(nivel_rezistenta__gte=1),
                name='limite_rezista_ambalaj',
                violation_error_message="Nivelul de rezistență trebuie să fie între 1 și 10 inclusiv!"
            )
        ]
    nume=models.CharField(max_length=200, unique=True)
    culoare=models.CharField(max_length=100, null=True)
    nivel_rezistenta=models.PositiveIntegerField(
        help_text="Valori între 1 și 10. Un număr mai mare indică rezistență mai mare",
        null=True
    )
    descriere = models.TextField(null=True)
   
    def __str__(self):
        return f"{self.nume}: {self.culoare}"

class Categorie(models.Model):
    class Meta:
        verbose_name_plural = "Categorii"
        
    nume = models.CharField(max_length=100)
    descriere = models.TextField()
    culoare = models.CharField(max_length=7, help_text="Cod Hex (ex: #3498db)")
    sigla = models.CharField(max_length=100, help_text="Calea catre imagine sau clasa FontAwsome")
    nivel_prioritate = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nume
    
class Brand(models.Model):
    class Meta:
        verbose_name_plural = "Branduri"
        
    nume_brand = models.CharField(max_length=100)
    tara_origine = models.CharField(max_length=100)
    rating_calitate = models.FloatField()
    
    def __str__(self):
        return self.nume_brand
    
class SediuCompanie(models.Model):
    class Meta:
        verbose_name_plural = "Sedii Companie"
            
    nume_sediu = models.CharField(max_length=100)
    oras = models.CharField(max_length=100)
    suprafata_mp = models.FloatField()

    def __str__(self):
        return f"{self.nume_sediu} ({self.oras})"
    
class DepozitSediu(models.Model):
    class Meta:
        verbose_name_plural = "Depozite Sedii"
        
    sediu = models.ForeignKey(SediuCompanie, on_delete=models.CASCADE, related_name="depozite")
    cod_depozit = models.CharField(max_length=20)
    capacitate_paleti = models.IntegerField()
    temperatura_controlata = models.BooleanField(default=False)


    def __str__(self):
        return f"Depozit {self.cod_depozit} - {self.sediu.nume_sediu}"
    
class ServiciuAditional(models.Model):
    class Meta:
        verbose_name_plural = "Servicii Adiționale"
    
    nume_serviciu = models.CharField(max_length=100)
    pret_standard = models.DecimalField(max_digits=10, decimal_places=2)
    disponibil_national = models.BooleanField(default=True)

    def __str__(self):
        return self.nume_serviciu
    
class CompaniePartenera(models.Model):
    class Meta:
            verbose_name_plural = "Companii Partenere"
        
    nume_companie = models.CharField(max_length=100)
    comision_procentual = models.FloatField()
    contract_activ = models.BooleanField(default=True)

    def __str__(self):
        return self.nume_companie
    
class Produs(models.Model):
    class Meta:
        verbose_name_plural = "Produse"
        
    MATERIAL_CHOICES = [
        ('LEMN', 'Lemn Masiv'),
        ('PAL', 'PAL'),
        ('MDF', 'MDF'),
        ('METAL', 'Metal'),
        ('STICLA', 'Sticlă'),
    ]

    nume = models.CharField(max_length=200)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    greutate = models.FloatField(help_text="Greutatea în kg")
    in_stoc = models.BooleanField(default=True)
    data_adaugare = models.DateField(auto_now_add=True)
    material_principal = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    culori_disponibile = models.JSONField(help_text="Lista de culori disponibile (ex: [\"Alb\", \"Stejar\"])")

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produse")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="produse")
    servicii_aditionale = models.ManyToManyField(ServiciuAditional, blank=True, related_name="produse")
    parteneri_distributie = models.ManyToManyField(CompaniePartenera, blank=True, related_name="produse")

    def __str__(self):
        return self.nume
# Create your models here.
