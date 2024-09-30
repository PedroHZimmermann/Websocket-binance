import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import sys
sys.setrecursionlimit(1000000) 

from binance.client import Client
import pandas as pd
from datetime import date
from binance import Client
import ta
import pandas as pd
from time import sleep
from binance.client import Client
import numpy as np
import matplotlib.pyplot as plt
from binance.exceptions import BinanceAPIException
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import math
from sklearn.metrics import mean_squared_error
import seaborn as sn
import glob
from tkinter import *
from PIL import ImageTk
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
import PIL.Image
from tkinter import font

interval = Client.KLINE_INTERVAL_30MINUTE
api_key = "QBpyLIZT4RkhyJYR2swse1f6ynB9sWTrXjndc7gB5AliOqpIfa6B0y69YcRoyd7c"




def valida_entrada_usuario(ativo, l, api_key1, api_secret1, dias):
    ativo = ativo.get()
    api_key1 = api_key1.get()
    api_secret1 = api_secret1.get()
    ativo = ativo.upper()
    d = dias.get()
    client = Client(api_key1, api_secret1)
    client.WEBSITE_URL = "wss://fstream.binance.com:9443/ws/"
    try:
        client.get_historical_klines(ativo, Client.KLINE_INTERVAL_30MINUTE, "2 days ago UTC")
        vativo = 0
    except BinanceAPIException as e:
        vativo = 1
    except ConnectionError as c:
        vativo = 1
    l = l.get()
    try:
        float(l)
        vl = 0
    except Exception as e:
        vl = 1
    if api_key1 != api_key:
        vapi_key = 0
    else: 
        vapi_key = 0
    de = float(d)
    if de <= 10 or de >= 1200:
        vd = 1
    else:
        vd = 0
    return vativo, vl, vapi_key, ativo, l, api_key1,api_secret1,d, vd

def resposta_validacao(ativo, l, api_key1, api_secret1, dias):
    resposta = valida_entrada_usuario(ativo, l, api_key1, api_secret1, dias)
    if resposta[0] == 1 and resposta[1] == 0 and resposta[2] == 0:
        messagebox.showerror('Falha', 'Algo parece estar errado com seu ativo selecionado. ')
        #print('A algo de errado com seu ativo selecionado.')
        return False
    elif resposta[1] == 1 and resposta[0] == 0 and resposta[2] ==0:
        messagebox.showerror('Falha', 'Confirme os lotes (use ponto ao inves da virgula). ')
        #print('Confirme os lotes (use ponto ao inves da virgula).')
        return False
    elif resposta[0] == 0 and resposta[1] == 0 and resposta[2] == 0 and resposta[8] == 0:
        #print('Iniciando robo. ')
        ativo = resposta[3]
        l =  resposta[4]
        api_key1 =  resposta[5]
        api_secret1 =  resposta[6]
        d = resposta[7]
        symbol = ativo
        lote = l 
        api_key = api_key1
        api_secret = api_secret1
        di = d
        return True, ativo, l, api_key1, api_secret1, symbol, lote, api_key, api_secret, di
    elif resposta[1] == 0 and resposta[0] == 0 and resposta[2] ==0 and resposta[8] == 1:
        messagebox.showerror('Falha', 'O intervalo de dias deve ser superior a 10 e menor que 1200. ')
        return False
    else: 
        messagebox.showerror('Falha', 'Confirme os Parâmetros. ')
        return False 

def parametros(ativo, l, api_key1, api_secret1, dias):
    global symbol
    global lote
    global api_key
    global api_secret
    global diasu
    i = resposta_validacao(ativo, l, api_key1, api_secret1, dias)
    symbol = i[1]
    lote = i[2]
    api_key = i[3]
    api_secret = i[4]
    diasu = i[9]
    if i[0] == True:
        pass
    else: 
        usuariomenu()
    rootm.destroy()
    pass


def usuariomenu():
    #interface 
    global rootm
    rootm = Tk() 
    rootm.title(f'PG | Backtest')
    rootm.iconbitmap('C:\pg\icon.ico')
    rootm.geometry('340x160')
    rootm.configure(bg='#FFFFFF')
    rootm.minsize(340, 170) 
    rootm.maxsize(340, 170)
    ativo = Entry(rootm, width=30)
    ativo.grid(row=0, column=1,padx=20, pady=(10,0))
    l = Entry(rootm, width=30)
    l.grid(row=1, column=1,padx=20)
    api_key1 = Entry(rootm, width=30)
    api_key1.grid(row=2, column=1,padx=20)
    api_secret1 = Entry(rootm, width=30)
    api_secret1.grid(row=3, column=1,padx=20)
    dias = Entry(rootm, width=30)
    dias.grid(row=4, column=1,padx=20)
    #Create text box label - descricao
    ativolb = Label(rootm, text= 'Ativo:', background= 'white')
    ativolb.grid(row=0, column=0,padx=20, pady=(10,0))
    llb = Label(rootm, text= 'Lote: ', background= 'white')
    llb.grid(row=1, column=0,padx=20)
    api_key1lb = Label(rootm, text= 'API Key: ', background= 'white')
    api_key1lb.grid(row=2, column=0,padx=20)
    api_secret1lb = Label(rootm, text= 'API Secret: ', background= 'white')
    api_secret1lb.grid(row=3, column=0,padx=20)
    diaslb = Label(rootm, text= 'Dias: ', background= 'white')
    diaslb.grid(row=4, column=0,padx=20)
    #Crate button
    ligar = Button(rootm, text = 'Backtest', command=lambda: parametros(ativo, l, api_key1, api_secret1, dias), background= 'white')
    ligar.grid(row=5,column=0, columnspan=2, pady=10, padx=10, ipadx=126)
    rootm.mainloop()

usuariomenu()
symbol = symbol.upper()
lote = float(lote)
shares = lote
dias = diasu
client = Client(api_key, api_secret)
client.WEBSITE_URL = "wss://fstream.binance.com:9443/ws/"

try:
    data = client.get_historical_klines(symbol, interval, f"{dias} days ago UTC")
except BinanceAPIException as e:
    #print(e)
    messagebox.showerror('Binance', f'Resposta: {e}. ')
except ConnectionError as c:
    messagebox.showerror('Conexão', f'Resposta: {c}. ')
data = pd.DataFrame(data)
data.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore' ]
data.head()
data['Open Time'] = pd.to_datetime(data['Open Time']/1000, unit='s')
data['Close Time'] = pd.to_datetime(data['Close Time']/1000, unit='s')
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, axis=1)


def round_down(x):
  return int(math.floor(x / 100.0)) * 100

def crossover_sinal(data):
    data["ema9"] = data["Close"].ewm(span=9).mean()
    data["ema34"] = data["Close"].ewm(span=34).mean()
    data["Antes"] = data["ema9"].shift(1) - data["ema34"].shift(1)
    data["Atual"] = data["ema9"] - data["ema34"]
    data.loc[(data["Antes"] < 0) & (data["Atual"] > 0), "Buy Price"] = data["Close"]
    data["Antes"] = data["ema9"].shift(1) - data["ema34"].shift(1)
    data["Atual"] = data["ema9"] - data["ema34"]
    data.loc[(data["Antes"] > 0) & (data["Atual"] < 0), 'Sell Price'] =data["Close"]
    data['ATR'] = ta.volatility.AverageTrueRange(high=data.High, low = data.Low, close = data.Close, window = 7).average_true_range()
    data['Stop Loss Venda'] = (data['Sell Price'] + (2.5 * data['ATR']))
    data['Stop Loss Compra'] = (data['Buy Price'] - (2.5 * data['ATR']))
    data['Stop Loss Venda'] = data['Stop Loss Venda'].fillna(method='ffill')
    data['Stop Loss Compra'] = data['Stop Loss Compra'].fillna(method='ffill')
    columns = ["Close", "ema9", "ema34", "Buy Price", 'Sell Price', 'Stop Loss Venda', 'Stop Loss Compra', 'High', 'Low', 'Close Time', 'ATR']
    return data[columns]

df = crossover_sinal(data)
df.head()
print(df)

all_profits = []
ongoing = False

for i in range(0,len(df)):
    if ongoing == True:
        if ~(np.isnan(df['Sell Price'][i])):
            DataHoraF = df['Close Time']
            if df['Stop Loss Compra'][i] < df['Sell Price'][i]:
                exit = df['Sell Price'][i]
            else:
                exit = df['Stop Loss Compra'][i]
            profit = shares * (exit - entry)
            all_profits += [profit]
            ongoing = False
        elif df['Low'][i] <= df['Stop Loss Compra'][i]:
            exit = df['Stop Loss Compra'][i]
            profit = shares * (entry - exit)
            all_profits += [profit]
            ongoing = False
    else:
        if ~(np.isnan(df['Buy Price'][i])):
            entry = df['Buy Price'][i]
            DataHoraI = df['Close Time']
            shares = lote
            ongoing = True


all_profitsv = []
ongoingv = False

for i in range(0,len(df)):
    if ongoing == True:
        if ~(np.isnan(df['Buy Price'][i])):
            if df['Stop Loss Venda'][i] > df['Buy Price'][i]:
                exit = df['Buy Price'][i]
            else:
                exit = df['Stop Loss Venda'][i]
            profitv = shares * (entry - exit)
            all_profitsv += [profitv]
            ongoing = False
        elif df['High'][i] >= df['Stop Loss Venda'][i]:
            exit = df['Stop Loss Venda'][i]
            profitv = shares * (entry - exit)
            all_profitsv += [profitv]
            ongoing = False
    else:
        if ~(np.isnan(df['Sell Price'][i])):
            entry = df['Sell Price'][i]
            shares = lote
            ongoing = True


def corrigitamanholista():
    if len(all_profits) > len(all_profitsv):
        del all_profits[-1]
        #print('Foi corrigido as o tamanho das ordens de Compra. ')
        return all_profits and all_profitsv
    elif len(all_profits) < len(all_profitsv):
        del all_profitsv[-1]
        #print('Foi corrigido as o tamanho das ordens de Venda. ')
        return all_profitsv and all_profits
    else:
        pass

curva_capital = []
def juntacompraevenda():
    corrigitamanholista()
    for i in range(0 , len(all_profits)):
        curva_capital.append(all_profits[i]) and curva_capital.append(all_profitsv[i])
    return curva_capital

def acumular():
    curva_capital_pronta = []
    j=0
    curva_capital = juntacompraevenda()
    for i in range(0,len(curva_capital)):
        j+=curva_capital[i]
        curva_capital_pronta.append(j)     
    return curva_capital_pronta

curva_capital_pronta = acumular()

#Retornar as medi
# as
def retornarmedias():
    #Operacoes que ganharam na parte compradora gera media de ganho
    positivas = []
    negativas = []
    Npositivas = 0
    NNegativas = 0 
    for i in all_profits:
        if i > 0: 
            positivas.append(i) 
            Npositivas = Npositivas + 1
        elif i <= 0: 
            negativas.append(i)
            NNegativas = NNegativas + 1
    for j in all_profitsv:
        if j > 0: 
            positivas.append(i) 
            Npositivas = Npositivas + 1
        elif j <= 0: 
            negativas.append(i)
            NNegativas = NNegativas + 1
    mediaG = sum(positivas)/Npositivas
    mediaL = sum(negativas)
    mediaL = abs(mediaL)/NNegativas
    payoff = mediaG/mediaL
    return payoff, mediaG, mediaL


def drawdown():
    c = all_profits + all_profitsv
    menor = 0
    maior = 0 
    for i in c:
        if i < menor:
            menor = i
        elif i > maior:
            maior = i
    draw = menor - maior/maior
    return draw

def interfacecliente():
    draw = drawdown()
    mm = retornarmedias()
    num_operations = len(all_profits) + len(all_profitsv)
    gains = sum(x >= 0 for x in all_profits) + sum(x >= 0 for x in all_profitsv)
    pct_gains = 100 * (gains / num_operations)
    losses = num_operations - gains
    pct_losses = 100 - pct_gains

    print("Número de operações = ", int(num_operations))
    print("Operações no lucro = ", gains, "or", pct_gains.round(), "%")
    print("Operaçoes no prejuízo = ", losses, "or", pct_losses.round(), "%")
    print("O resultado foi de = ", curva_capital_pronta[-1])
    print("PayOff = ", round(mm[0],3))
    print("Media de ganho = ", round(mm[1],3))
    print("Media de loss = ", round(mm[2],3))
    print('Drawdown Maximo = ', round((draw * -1),3))
    resultadoindice = ['Numero de operações', 'Operações no lucro (%)', 'Operaçoes no prejuízo (%)', 'O resultado foi de', 'PayOff', 'Media de ganho', 'Media de loss', 'Drawdown Maximo']
    resultador = [int(num_operations), pct_gains.round(), pct_losses.round(), curva_capital_pronta[-1], round(mm[0],3), round(mm[1],3), round(mm[2],3), round((draw * -1),3)]
    dicr = {}
    for i in resultadoindice:
        for j in range(0,8):
            dicr[resultadoindice[j]] = f'{resultador[j]}'
    print(dicr)
    img = Image.new('RGB', (400, 300), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    operacoslucro = int(pct_gains.round())
    operacoeprejuizo = int(pct_losses.round())
    
    #Problema na fonte nao esta carregando
    ###
    default_font = ImageFont.load_default()
    my_font = default_font
    d.multiline_text((10, 10), f"Número de operacoes = {int(num_operations)}\nResultado = {round(curva_capital_pronta[-1],2)}\nOperacoes no lucro = {operacoslucro}%\nOperaçoes no prejuizo = {operacoeprejuizo}%\nPayOff = {round(mm[0],2)}\nMedia de ganho = {round(mm[1],2)}\nMedia de loss = {round(mm[2],2)}\nDrawdown Maximo = {round((draw * -1),2)}\nLote = {lote}\nPrazo = {dias} dias", fill=(0, 0, 0), font = my_font)
    img.save('table.png')
    o = []    
    c = 1 
    for i in curva_capital_pronta:
        o = o + [c]
        c = c + 1
    root = Tk()
    root.configure(bg='#FFFFFF')
    root.geometry("1250x450")
    root.iconbitmap('c:\pg\icon.ico')
    root.title('PG | Backtest')
    root.minsize(1250, 550) 
    root.maxsize(1250, 550)  
    fig = Figure(figsize=(8, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(o, curva_capital_pronta, color="#09BF0B")
    plot.set_facecolor('#EBEBEB')
    plot.grid(which='major', color='white', linewidth=1.2)
    plot.grid(which='minor', color='white', linewidth=0.6)
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    backt = Label(background="#FFFFFF", foreground="#000000",text=f'{symbol}', font=f'raleway 20').grid(column=0, row=0)
    frame = Frame(root, width=900, height=900)
    frame.grid(column=1, row=1)

    # Create an object of tkinter ImageTk
    img = ImageTk.PhotoImage(Image.open('table.png'))

    # Create a Label Widget to display the text or Image
    label = Label(frame, image = img, anchor='center').grid(column=0, row=2)
    canvas.get_tk_widget().grid(column=0, row=1)
    arima = Button(root, text = 'Trades', command=lambda: nuvemdepontos(), bg='white')
    arima.grid(row=2,column=1, columnspan=2, pady=10, padx=10, ipadx=137)
    root.mainloop()



def nuvemdepontos():
    dic = {}
    allt = all_profits + all_profits
    o = 1
    for i in allt:
        dic[o] = i
        o = o + 1
    keys = dic.keys()
    values = dic.values()
    names = keys
    values = values
    rootn = Tk()
    rootn.configure(bg='#FFFFFF')
    rootn.geometry("800x500")
    rootn.iconbitmap('C:\pg\icon.ico')
    rootn.title('PG | Nuvem')
    rootn.minsize(800, 500) 
    rootn.maxsize(800, 500)  
    fig1= Figure(figsize=(8, 4), dpi=100)
    plot1 = fig1.add_subplot(1, 1, 1)
    plot1.scatter(names, values, color="#09BF0B")
    plot1.set_facecolor('#EBEBEB')
    plot1.grid(which='major', color='white', linewidth=1.2)
    plot1.grid(which='minor', color='white', linewidth=0.6)
    canvas1 = FigureCanvasTkAgg(fig1, master=rootn)
    canvas1.draw()
    canvas1.get_tk_widget().grid(column=0, row=1)
    trades = Label(rootn,background="#FFFFFF", foreground="#000000",text=f'Trades: {symbol}', font=f'raleway 20').grid(column=0, row=0)
    sair = Button(rootn, text = 'Sair', command=lambda: rootn.destroy(), bg='white')
    sair.grid(row=2,column=0, columnspan=2, pady=10, padx=10, ipadx=107)
    rootn.mainloop()



interfacecliente()

