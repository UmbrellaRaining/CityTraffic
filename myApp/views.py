from django.shortcuts import render,HttpResponse,redirect
from myApp import models
from myApp.models import User, City, Traffic_Data, Flight_Data
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django import forms
from utils.encrypt import md5
from openpyxl import load_workbook
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponseRedirect
from json import JSONEncoder
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd
import json, requests, math, sys

# Create your views here.
# 主页
def index(request):
    info = request.session.get("info")
    userInfo = User.objects.all()
    ID = info['id']
    value = request.session.get("value")
    TrafficValue = request.session.get("TrafficValue")
    user_logo = User.objects.filter(id=ID).values().first()['logo']
    user_name = User.objects.filter(id=ID).values().first()['name']

    CA_ke = Flight_Data.objects.values_list('ke')[0][0]
    CA_correct = Flight_Data.objects.values_list('correct')[0][0]
    CA_use = Flight_Data.objects.values_list('use')[0][0]
    MU_ke = Flight_Data.objects.values_list('ke')[1][0]
    MU_correct = Flight_Data.objects.values_list('correct')[1][0]
    MU_use = Flight_Data.objects.values_list('use')[1][0]
    CZ_ke = Flight_Data.objects.values_list('ke')[2][0]
    CZ_correct = Flight_Data.objects.values_list('correct')[2][0]
    CZ_use = Flight_Data.objects.values_list('use')[2][0]
    HO_ke = Flight_Data.objects.values_list('ke')[3][0]
    HO_correct = Flight_Data.objects.values_list('correct')[3][0]
    HO_use = Flight_Data.objects.values_list('use')[3][0]
    C9_ke = Flight_Data.objects.values_list('ke')[4][0]
    C9_correct = Flight_Data.objects.values_list('correct')[4][0]
    C9_use = Flight_Data.objects.values_list('use')[4][0]
    MF_ke = Flight_Data.objects.values_list('ke')[5][0]
    MF_correct = Flight_Data.objects.values_list('correct')[5][0]
    MF_use = Flight_Data.objects.values_list('use')[5][0]
    ZH_ke = Flight_Data.objects.values_list('ke')[6][0]
    ZH_correct = Flight_Data.objects.values_list('correct')[6][0]
    ZH_use = Flight_Data.objects.values_list('use')[6][0]
    HU_ke = Flight_Data.objects.values_list('ke')[7][0]
    HU_correct = Flight_Data.objects.values_list('correct')[7][0]
    HU_use = Flight_Data.objects.values_list('use')[7][0]
    flight_data = {"CA_ke": CA_ke, "CA_correct": CA_correct, "CA_use": CA_use,
                   "MU_ke": MU_ke, "MU_correct": MU_correct, "MU_use": MU_use,
                   "CZ_ke": CZ_ke, "CZ_correct": CZ_correct, "CZ_use": CZ_use,
                   "HO_ke": HO_ke, "HO_correct": HO_correct, "HO_use": HO_use,
                   "C9_ke": C9_ke, "C9_correct": C9_correct, "C9_use": C9_use,
                   "MF_ke": MF_ke, "MF_correct": MF_correct, "MF_use": MF_use,
                   "ZH_ke": ZH_ke, "ZH_correct": ZH_correct, "ZH_use": ZH_use,
                   "HU_ke": HU_ke, "HU_correct": HU_correct, "HU_use": HU_use}

    weather_info = request.session.get('weather_info')

    return render(request, "index.html", {"info": info, "ID": ID, "value": value,
                                          "TrafficValue": TrafficValue, "flight_data": flight_data,
                                          "weather_info": weather_info, "user_logo":user_logo,
                                          "user_name": user_name})

def weather(request):
    key = "f9c96b98908401fd9e336686bb3a9f44"
    # city_code = "522622"
    # City_Value = City.objects.filter(city_name='黄平县')
    if request.method == 'GET':
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
    url_navi = 'https://restapi.amap.com/v3/geocode/regeo'
    LOCATION = "{},{}".format(longitude, latitude)
    RADIUS = 3000
    OUTPUT = 'json'
    EX = 'all'
    params = {
        "location": LOCATION,
        "output": OUTPUT,
        "key": key,
        'radius': RADIUS,
        'extensions': EX,
    }
    response_navi = requests.get(url_navi, params=params)
    answer = response_navi.json()
    city_name = answer['regeocode']['addressComponent']['city']
    City_Value = City.objects.filter(city_name=city_name)

    for item in City_Value:
        code = item.adcode

        # 构造API请求URL
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={code}&key=f9c96b98908401fd9e336686bb3a9f44"

    # 发送HTTP请求获取天气信息
    response = requests.get(url)

    # 解析JSON数据
    weather_info = response.json()
    print(weather_info)

    # 获取lives列表中的数据
    lives = weather_info['lives']
    province = lives[0]['province']
    weather = lives[0]['weather']
    city = lives[0]['city']
    adcode = lives[0]['adcode']
    temperature_float = lives[0]['temperature_float']
    winddirection = lives[0]['winddirection']
    windpower = lives[0]['windpower']
    humidity_float = lives[0]['humidity_float']
    reporttime = lives[0]['reporttime']

    info = {"province": province, "weather": weather, "city": city, "adcode": adcode,
            "temperature_float": temperature_float, "winddirection": winddirection,
            "windpower": windpower, "humidity_float": humidity_float, "reporttime": reporttime}

    request.session['weather_info'] = info

    info_display = {"省份": province, "城市": city, "天气": weather,
            "温度": temperature_float, "风向": winddirection,
            "风力": windpower, "湿度": humidity_float, "时间": reporttime}

    return JsonResponse({"info_display": info_display})

def DriverMap(request):
    begin = request.POST.get("begin")
    end = request.POST.get("end")
    city = request.session.get('weather_info')

    position = {"begin": begin, "end": end}
    return render(request, 'DriverMap.html', {"position": position, "city": city})

# 中转站
def toFileSelect(request):
    return render(request, "FileSelect.html")

# 近十年客流量文件选择
def FileSelect(request):
    file = request.FILES.get("file")
    df = pd.read_excel(file)
    year = list(df[1:]['年份'])
    data_subway = list(df[1:]['铁路客流量（亿）'])
    # data_subway = list(df[1:]['测试数据1'])
    data_airplane = list(df[1:]['航空客流量（亿）'])
    # data_airplane = list(df[1:]['测试数据2'])
    up_subway = ['{:.2f}'.format(value) for value in list(df[1:]['铁路同比'])]
    up_subway_list = [float(value) for value in up_subway]
    up_airplane = ['{:.2f}'.format(value) for value in list(df[1:]['航空同比'])]
    up_airplane_list = [float(value) for value in up_airplane]
    request.session["value"] = {"year": year, "data_subway": data_subway,"data_airplane": data_airplane,
                                "up_subway_list": up_subway_list,"up_airplane_list": up_airplane_list}

    return redirect("/index/")

# 中转站
def toTrafficToolFile(request):
    return render(request, "TrafficToolFile.html")

# 交通工具销量文件选择
def TrafficToolFile(request):
    file = request.FILES.get("file")
    df = pd.read_excel(file)
    month = list(df['月份'])
    data_1 = list(df['乘用车'])
    # data_1 = list(df['测试数据1'])
    data_2 = list(df['二手车'])
    # data_2 = list(df['测试数据2'])
    data_3 = list(df['进口车'])
    # data_3 = list(df['测试数据3'])

    request.session["TrafficValue"] = {"month": month, "data_1": data_1, "data_2": data_2,
                                "data_3": data_3}
    return redirect("/index/")

def toSubwayFile(request):
    return render(request, 'SubwayFile.html')

def SubwayFile(request):
    file = request.FILES.get("file")
    df = pd.read_excel(file)
    month = df.iloc[:, 0].tolist()
    km = df.iloc[:, 1].tolist()
    passenger = df.iloc[:, 2].tolist()
    station = df.iloc[:, 3].tolist()

    request.session["Subway"] = {"month": month, "km": km, "passenger": passenger,
                                      "station": station}
    return redirect('/index/')

def Subway(request):
    city = request.POST.get("cityName")
    CityValue = City.objects.filter(city_name=city)
    for item in CityValue:
        ID = item.id
        city_name_ = item.city_name
        adcode_ = item.adcode
    city_name = city_name_
    adcode = adcode_[:4]
    key = "f9c96b98908401fd9e336686bb3a9f44"
    SubwayValue = {"city_name": city_name, "adcode": adcode, "key": key}
    return render(request, "Subway.html", {"SubwayValue": SubwayValue})

def TrafficCongestion1(request):
    df = pd.read_excel(r"D:\Python\pycharmProfessional\pycharmProject\CityTraffic\spiderMan\城市交通指数.xlsx")
    city = list(df[:10]['2023Q3城市排名'])
    weekend_city = list(df[:10]['2023Q3周末城市排名'])
    title_city1 = df[:0]['2023Q3高峰拥堵指数'].name
    title_city2 = df[:0]['2023Q3高峰平均速度(km/h)'].name
    title_city3 = df[:0]['2023Q3周末拥堵指数'].name
    title_city4 = df[:0]['2023Q3周末实际速度'].name
    congestion = list(df['2023Q3高峰拥堵指数'][:10])
    weekend_congestion = list(df['2023Q3周末拥堵指数'][:10])
    speed = list(df['2023Q3高峰平均速度(km/h)'][:10])
    weekend_speed = list(df['2023Q3周末实际速度'][:10])
    delay = list(df['2023Q3高峰信控路口延误(s)'][:10])
    Congestion1 = {"city": city, "congestion": congestion, "title_city1": title_city1,
                   "title_city2": title_city2, "title_city3": title_city3, "title_city4": title_city4,
                   "speed": speed, "delay": delay, "weekend_city": weekend_city,
                   "weekend_congestion": weekend_congestion, "weekend_speed": weekend_speed}
    return render(request, "TrafficCongestion1.html", {"Congestion1": Congestion1})

def TrafficCongestion2(request):
    df = pd.read_excel(r"D:\Python\pycharmProfessional\pycharmProject\CityTraffic\spiderMan\城市交通指数.xlsx")
    year = list(df['年份'][:8])
    congestion = list(df['重庆高峰拥堵指数'][:8])
    weekend_congestion = list(df['重庆周末拥堵指数'][:8])
    speed = list(df['重庆高峰实际速度'][:8])
    weekend_speed = list(df['重庆周末实际速度'][:8])
    time = list(df['重庆平均耗时(min)'][:8])
    out = list(df['重庆出行强度'][2:8])

    # //预测部分
    quarter = list(df['年份/季度'])
    before_congestion = list(df['重庆历年交通拥堵指数'][:12])
    svm_linear = list(df['SVM-线性核函数'][:12])
    svm_poly = list(df['SVM-多项式核函数'][:12])
    svm_rbf = list(df['SVM模型-高斯'][:15])
    lstm = list(df['LSTM模型'][:12])
    lstm_pred = list(df['LSTM模型-预测'][:15])
    Congestion2 = {"year": year, "congestion": congestion, "weekend_congestion":weekend_congestion,
                   "speed": speed, "weekend_speed": weekend_speed, "time": time,
                   "out": out, "quarter": quarter, "before_congestion": before_congestion,
                   "svm_linear": svm_linear, "svm_poly": svm_poly, "svm_rbf": svm_rbf,
                   "lstm": lstm, "lstm_pred": lstm_pred}
    return render(request, "TrafficCongestion2.html", {"Congestion2": Congestion2})

# 登录页
# 1/这是ModelForm方法
class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["name", "password"]
        # No1
        widgets = {
            "name": forms.TextInput(attrs={"class":"input-material", "name": "userName", "id":"login-username", "data-msg":"请输入用户名", "placeholder":"用户名"}),
            "password": forms.PasswordInput(attrs={"class":"input-material", "name": "passWord", "id":"login-password", "data-msg":"请输入密码", "placeholder":"密码", "style": "margin-top: 30px"})
        }
        # 在字段定义中设置required属性
        form_class = forms.Form
        labels = {
            "name": False,
            "password": False
        }
    # 功能同上(No1),但是出了点小问题,嘿嘿嘿
    # def __int__(self, *args, **kwargs):
    #     super.__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "input-material, form-control"}

# 2/这是Form方法
class LoginForm1(forms.Form):
    name = forms.CharField(
        label=False,
        widget = forms.TextInput(attrs={"class":"input-material", "name": "userName", "id":"login-username", "data-msg":"请输入用户名", "placeholder":"用户名", "style": "margin-bottom: 30px"}),
        required=True,
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={"class":"input-material","name": "passWord",
                                          "id":"login-password", "data-msg":"请输入密码",
                                          "placeholder":"密码"}),
        required=True,
    )

    # 加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def Login(request):
    if request.method == "GET":
        form = LoginForm1()
        return render(request, "Login.html", {"form": form})

    form = LoginForm1(data=request.POST)
    username = request.POST.get("name")
    password = request.POST.get("password")
    # 验证成功
    if form.is_valid():
        print(form.cleaned_data)
        # user_obj = models.User.objects.filter(**form.cleaned_data).first()
        user_obj = models.User.objects.filter(name=username, password=password).first()
        if not user_obj:
            form.add_error("password", "用户名或密码错误")
            return render(request, "Login.html", {"form": form})

        request.session["info"] = {"id": user_obj.id, "name": user_obj.name}
        # request.session["info"] = user_obj.name
        return  redirect("/index/")
        # return render(request, "index.html", {"name": name})
    return render(request, "Login.html", {"form": form})

# 注册页(固定,别动)
def Register(request):
    if request.method == "GET":
        user = request.GET.get("registerUsername")
        pwd = request.GET.get("registerPassword")
        return render(request, "Register.html")
        User.objects.create(name=user, password=pwd)

    if request.method == "POST":
        user = request.POST.get("registerUsername")
        pwd = request.POST.get("registerPassword")
        User.objects.create(name=user, password=pwd)
        return redirect("/Login/")

# 用户信息
def UserInfo(request):
    userInfo = User.objects.all()
    return render(request, 'UserInfo.html',
                  {"name": userInfo})

def DetailInfo(request):
    # userInfo = User.objects.all().first()
    info = request.session.get("info")
    ID = info['id']
    # userInfo = User.objects.all().values()
    userInfo = User.objects.filter(id=ID).values().first()
    user_name = userInfo['name']
    user_pwd = userInfo['password']
    user_email = userInfo['email']
    user_image = userInfo['image']
    user_say = userInfo['say']
    user = {"user_pwd": user_pwd, "user_email": user_email, "user_image":user_image, "user_say": user_say, "user_name": user_name}
    return render(request, "DetailInfo.html", {"info": info, "user": user})

# 删除用户
def Delete(request):
    nid = request.GET.get("nid")
    User.objects.filter(id=nid).delete()
    return HttpResponse("删除成功")

# 编辑信息
def Edit(request, nid):
    row = models.User.objects.filter(id=nid).first()

    if not row:
        return HttpResponse("User not found", status=404)

        # 获取表单提交的新用户信息
    new_user = request.POST.get('user')
    new_password = request.POST.get('password')
    new_email = request.POST.get('email')

    # 检查新值是否存在，如果存在则更新
    if new_user is not None:
        row.name = new_user
    if new_password is not None:
        row.password = new_password
    if new_email is not None:
        row.email = new_email

    row.save()

    if new_user is not None and new_password is not None and new_email is not None:
        messages = 'true'
    else:
        messages = 'false'

    return render(request, 'Edit.html', {"row": row, "messages": messages})

def toImageFile(request):
    return render(request, "ImageFile.html")

def ImageFile(request):
    logo = request.FILES.get("logo")
    image = request.FILES.get("image")
    id = request.session.get('info')['id']
    error_message = None

    #头像部分
    if request.method == 'POST' and 'logo' in request.FILES:
        file = request.FILES['logo']
        if file.content_type.startswith('image/'):
            try:
                instance = User.objects.get(id=id)
                # 删除原有图片
                if instance.logo:
                    default_storage.delete(instance.logo.path)
                instance.logo = file # 更新 logo 字段
                instance.save() # 保存模型实例

                return redirect(f'/Edit/{id}/')
            except User.DoesNotExist:
                error_message = "User with given ID does not exist."
        else:
            error_message = "Invalid file type. Please upload an image."

    #图片部分
    if request.method == 'POST' and 'image' in request.FILES:
        file2 = request.FILES['image']
        if file2.content_type.startswith('image/'):
            try:
                instance2 = User.objects.get(id=id)
                # 删除原有图片
                if instance2.image:
                    default_storage.delete(instance2.image.path)
                instance2.image = file2  # 更新 logo 字段
                instance2.save()  # 保存模型实例

                return redirect(f'/Edit/{id}/')
            except User.DoesNotExist:
                error_message = "User with given ID does not exist."
        else:
            error_message = "Invalid file type. Please upload an image."
    return render(request, "ImageFile.html")

def turn(request):
    return render(request, "turn.html", {'redirect': True})

def test(request):
    userInfo = User.objects.all().first()
    info = request.session.get("info")
    return render(request, "test.html", {"info": info, "userInfo": userInfo})