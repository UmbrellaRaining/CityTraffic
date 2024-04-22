from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    logo = models.ImageField(max_length=90,default='')
    image = models.ImageField(max_length=90,default='')
    email = models.CharField(max_length=16,default='')
    say = models.CharField(max_length=100,default='')

class City(models.Model):
    city_name = models.CharField(max_length=32, default="黄平")
    adcode = models.CharField(max_length=32, default='')
    city_code = models.CharField(max_length=32, default="")

class Flight_Data(models.Model):
    flight_code = models.CharField(max_length=11)
    airline = models.CharField(max_length=32)
    ke = models.DecimalField(max_digits=5, decimal_places=2)
    correct = models.DecimalField(max_digits=5, decimal_places=2)
    use = models.DecimalField(max_digits=5, decimal_places=2)

class Traffic_Data(models.Model):
    city = models.CharField(max_length=11, default='')
    yearQ1 = models.DecimalField(max_digits=5, decimal_places=3, default='')
    yearQuarter = models.CharField(max_length=11, default='')
    before_congestion = models.DecimalField(max_digits=5, decimal_places=3, default='')
    svm_linear = models.DecimalField(max_digits=5, decimal_places=2, default='')
    svm_ploy = models.DecimalField(max_digits=5, decimal_places=2, default='')
    svm_rbf = models.DecimalField(max_digits=5, decimal_places=3, default='')
    lstm = models.DecimalField(max_digits=5, decimal_places=3, default='')
    lstm_pred = models.DecimalField(max_digits=5, decimal_places=3, default='')
    yearQ3_city = models.CharField(max_length=11, default='')
    Q3congestion = models.DecimalField(max_digits=5, decimal_places=3, default='')
    Q3congestion_speed = models.DecimalField(max_digits=5, decimal_places=2, default='')
    Q3congestion_delay = models.DecimalField(max_digits=5, decimal_places=2, default='')
    yearQ3_weekend_city = models.CharField(max_length=11, default='')
    Q3congestion_weekend = models.DecimalField(max_digits=5, decimal_places=3, default='')
    Q3congestion_weekend_speed = models.DecimalField(max_digits=5, decimal_places=2, default='')
    year = models.CharField(max_length=11, default='')
    congestion = models.DecimalField(max_digits=5, decimal_places=3, default='')
    speed = models.DecimalField(max_digits=5, decimal_places=2, default='')
    congestion_weekend = models.DecimalField(max_digits=5, decimal_places=3, default='')
    speed_weekend = models.DecimalField(max_digits=5, decimal_places=2, default='')
    time = models.DecimalField(max_digits=5, decimal_places=2, default='')
    out = models.DecimalField(max_digits=5, decimal_places=3, default='')