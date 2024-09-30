import pandas as pd
from time import sleep
from binance.client import Client
import pandas as pd
from datetime import date
from binance import Client
import ta
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
import pandas as pd
from time import sleep
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from tkinter import *
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
import webbrowser
global symbol
global api_key
global lote
global api_secret
import decimal
import sys
limit = sys.getrecursionlimit()
Newlimit = 1000000000
limit = sys.setrecursionlimit(Newlimit)


#interface 
root = Tk()
root.title(f'PG')
root.iconbitmap('C:\pg\icon.ico')
root.geometry('325x150')

#validacao de entrada 
api_key = 'QBpyLIZT4RkhyJYR2swse1f6ynB9sWTrXjndc7gB5AliOqpIfa6B0y69YcRoyd7c' 


def valida_entrada_usuario(ativo, l, api_key1, api_secret1):
    ativo = ativo.get()
    api_key1 = api_key1.get()
    api_secret1 = api_secret1.get()
    ativo = ativo.upper()
    client = Client(api_key1, api_secret1)
    client.WEBSITE_URL = "wss://fstream.binance.com:9443/ws/"
    try:
        client.get_historical_klines(ativo, Client.KLINE_INTERVAL_30MINUTE, "2 days ago UTC")
        vativo = 0
    except BinanceAPIException as e:
        vativo = 1
    l = l.get()
    try:
        float(l)
        vl = 0
    except Exception as e:
        vl = 1
    if api_key1 != api_key:
        vapi_key = 1
    else: 
        vapi_key = 0
    return vativo, vl, vapi_key, ativo, l, api_key1,api_secret1

def resposta_validacao(ativo, l, api_key1, api_secret1):
    resposta = valida_entrada_usuario(ativo, l, api_key1, api_secret1)
    if resposta[0] == 1 and resposta[1] == 0 and resposta[2] == 0:
        messagebox.showerror('Falha', 'Algo parece estar errado com seu ativo selecionado. ')
        print('A algo de errado com seu ativo selecionado.')
        return False
    elif resposta[1] == 1 and resposta[0] == 0 and resposta[2] ==0:
        messagebox.showerror('Falha', 'Confirme os lotes (use ponto ao inves da virgula). ')
        print('Confirme os lotes (use ponto ao inves da virgula).')
        return False
    elif resposta[2] == 1 and resposta[1] == 1 and resposta[0] == 0:
        messagebox.showerror('Acesso Negado', 'Acesso negado - entre em contato com o suporte. ')
        return False
    elif resposta[0] == 0 and resposta[1] == 0 and resposta[2] == 0:
        print('Iniciando robo. ')
        ativo = resposta[3]
        l =  resposta[4]
        api_key1 =  resposta[5]
        api_secret1 =  resposta[6]
        symbol = ativo
        lote = l 
        api_key = api_key1
        api_secret = api_secret1
        return True, ativo, l, api_key1, api_secret1, symbol, lote, api_key, api_secret
    else: 
        messagebox.showerror('Falha', 'Confirme os Parâmetros. ')
        return False 

def parametros(ativo, l, api_key1, api_secret1):
    global symbol
    global lote
    global api_key
    global api_secret
    i = resposta_validacao(ativo, l, api_key1, api_secret1)
    symbol = i[1]
    lote = i[2]
    api_key = i[3]
    api_secret = i[4]
    if i[0] == True:
        pass
    else: 
        usuariomenu()
    root.destroy()
    pass


def usuariomenu():
    ativo = Entry(root, width=30)
    ativo.grid(row=0, column=1,padx=20, pady=(10,0))
    l = Entry(root, width=30)
    l.grid(row=1, column=1,padx=20)
    api_key1 = Entry(root, width=30)
    api_key1.grid(row=2, column=1,padx=20)
    api_secret1 = Entry(root, width=30)
    api_secret1.grid(row=3, column=1,padx=20)
    #Create text box label - descricao
    ativolb = Label(root, text= 'Ativo:')
    ativolb.grid(row=0, column=0,padx=20, pady=(10,0))
    llb = Label(root, text= 'Lote: ')
    llb.grid(row=1, column=0,padx=20)
    api_key1lb = Label(root, text= 'API Key: ')
    api_key1lb.grid(row=2, column=0,padx=20)
    api_secret1lb = Label(root, text= 'API Secret: ')
    api_secret1lb.grid(row=3, column=0,padx=20)
    #Crate button
    ligar = Button(root, text = 'Logar', command=lambda: parametros(ativo, l, api_key1, api_secret1))
    ligar.grid(row=4,column=0, columnspan=2, pady=10, padx=10, ipadx=126)
    root.mainloop()

usuariomenu()
symbol = symbol.upper()

def cliente(api_key, api_secret):
    while True:
        try:
            client = Client(api_key, api_secret)
            return client
        except ConnectionError as c:
            print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
            sleep(10)
            continue
        except Exception as e:
            print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
            print(e)
            sleep(10)
            continue



client = cliente(api_key, api_secret)
client.WEBSITE_URL = "wss://fstream.binance.com:9443/ws/"

def getminutedata(symbol):
    while True:
        sleep(3)
        try:
            df = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "2 days ago UTC")
            print("dados coletados com sucesso! ")
            break
        except BinanceAPIException as e:
            print(e)
            sleep(150)
            continue
        except ConnectionError as c:
            print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
            sleep(15)
            continue
        except ReadTimeout as rt:
            print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
            sleep(15)
            continue
    global rou
    df = pd.DataFrame(df)
    df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of trades', 'TB Base Volume', 'TB Quote Volume', 'Ignoere' ]
    df.head()
    df['Open Time'] = pd.to_datetime(df['Open Time']/1000, unit='s')
    df['Close Time'] = pd.to_datetime(df['Close Time']/1000, unit='s')
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, axis=1)
    pr = str(df.Close.iloc[-1])
    dec = decimal.Decimal(pr)
    rou = abs(dec.as_tuple().exponent)
    return df



def getposição(symbol=symbol):
    while True:    
        try:
            verifica = client.futures_position_information(symbol=symbol)
            break
        except BinanceAPIException as e:
            print(e)
            sleep(5)
            continue
        except ConnectionError as c:
            print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
            sleep(15)
            continue
        except ReadTimeout as rt:
            print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
            sleep(15)
            continue
    return verifica


def getstops(symbol=symbol):
    while True:    
        try:
            stops = client.futures_get_open_orders(symbol=symbol)
            break
        except BinanceAPIException as e:
            print(e)
            sleep(5)
            continue
        except ConnectionError as c:
            print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
            sleep(15)
            continue
        except ReadTimeout as rt:
            print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
            sleep(15)
            continue
    return stops

def jaabertap(symbol=symbol):
    verifica = getposição(symbol=symbol)
    posicaoaberta = [i['symbol'] for i in verifica]
    verificalote = [i['positionAmt'] for i in verifica]
    preco_de_entrada = [i['entryPrice'] for i in verifica]
    preco_de_entrada = float(preco_de_entrada[0])
    if posicaoaberta == [f"{symbol}"] and float(verificalote[0]) == float(lote):
        print(f'Posição Aberta no ativo: {symbol}, lote: {verificalote[0]} e preco de entrada: {preco_de_entrada}')
        stoploss = getstops(symbol=symbol)
        sl = [i['stopPrice'] for i in stoploss]
        side = [i['side'] for i in stoploss]
        if stoploss == 0 or stoploss == []:
            df = getminutedata(symbol=symbol)
            atr = ta.volatility.AverageTrueRange(high=df.High, low = df.Low, close = df.Close, window = 14).average_true_range()
            sl = round(preco_de_entrada - (atr.iloc[-1] * 2), rou)
            while True:    
                try:
                    stoploss = client.futures_create_order(symbol=symbol, side='SELL',                                            
                                                    type='STOP_MARKET', quantity=lote, closePosition = 'true', stopprice=sl)
                    print('Stop Loss nao econtrado. Foi realizado uma operacao de ajuste.')
                    pos = 1
                    break
                    #open_position == True
                except BinanceAPIException as e:
                    print(e)
                    sleep(5)
                    continue
                except ConnectionError as c:
                    print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                    sleep(15)
                    continue
                except ReadTimeout as rt:
                    print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                    sleep(15)
                    continue
            return pos
        elif side[0] == 'BUY':
            while True:    
                try:
                    client.futures_cancel_all_open_orders(symbol=symbol)
                    print('Foi encontrado uma ordem de compra. Sua posicao esta comprada, cancelando ordem.')
                    pos = 1
                    break
                except BinanceAPIException as e:
                    print(e)
                except ConnectionError as c:
                    print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                    sleep(15)
                    continue
                except ReadTimeout as rt:
                    print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                    sleep(15)
                    continue
            return pos        
        else:
            pos = 1
            sl = float(sl[0])
            return pos
    elif posicaoaberta == [f"{symbol}"] and float(verificalote[0]) == - float(lote):
        print(f'Posição Aberta no ativo: {symbol}, lote: {verificalote[0]} e preco de entrada: {preco_de_entrada}')
        stoploss = getstops(symbol=symbol)
        sl = [i['stopPrice'] for i in stoploss]
        side = [i['side'] for i in stoploss]
        if stoploss == 0 or stoploss == []:
            df = getminutedata(symbol=symbol)
            atr = ta.volatility.AverageTrueRange(high=df.High, low = df.Low, close = df.Close, window = 14).average_true_range()
            sl = round(df.Close.iloc[-1] + (atr.iloc[-1] * 2), rou)
            while True:    
                try:
                    stoploss = client.futures_create_order(symbol=symbol, side='BUY',                                            
                                                    type='STOP_MARKET', quantity=lote, closePosition = 'true', stopprice=sl)
                    print('Stop Loss nao econtrado. Foi realizado uma operacao de ajuste.')
                    pos = 2
                    break
                    #open_position == True
                except BinanceAPIException as e:
                    print(e)
                    sleep(30)
                    continue
                except ConnectionError as c:
                    print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                    sleep(15)
                    continue
                except ReadTimeout as rt:
                    print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                    sleep(15)
                    continue
            return pos        
        elif side[0] == 'SELL':
            while True:    
                try:
                    client.futures_cancel_all_open_orders(symbol=symbol)
                    print('Foi encontrado uma ordem de venda. Sua posicao esta vendida, cancelando ordem.')
                    pos = 2
                    break
                except BinanceAPIException as e:
                    print(e)
                    sleep(15)
                    continue
                except ConnectionError as c:
                    print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                    sleep(15)
                    continue
                except ReadTimeout as rt:
                    print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                    sleep(15)
                    continue
            return pos
        else:
            pos = 2
            sl = float(sl[0])
            return pos
            #open_position == True
    else:
        print(f'Não há posição aberta no ativo: {symbol}')
        ##open_position =False
        return False



def cruzamentoc(symbol, qty):
    #Verifica se esta em posicao antes do robo entrar no caso comprado
    aberta = jaabertap(symbol=symbol)
    if aberta == False:
        open_position = False
        while True:
            df = getminutedata(symbol)
            if ta.trend._ema(df.Close, 9).iloc[-2] <= ta.trend._ema(df.Close,34).iloc[-2] \
            and ta.trend._ema(df.Close,9).iloc[-1] >= ta.trend._ema(df.Close,34).iloc[-1]:
                atr = ta.volatility.AverageTrueRange(high=df.High, low = df.Low, close = df.Close, window = 14).average_true_range()
                sl = round(df.Close.iloc[-1] - (atr.iloc[-1] * 2), rou)
                while True:    
                    try:
                        order = client.futures_create_order(symbol=symbol, side='BUY',
                                                            type='MARKET', quantity=lote)
                        stoploss = client.futures_create_order(symbol=symbol, side='SELL',                                            
                                                            type='STOP_MARKET', quantity=lote, closePosition = 'true', stopprice=sl)
                        print(order)
                        print(stoploss)
                        open_position=True
                        print(f'Foi executado uma compra de {lote} lotes no ativo {symbol}.')
                        break
                    except BinanceAPIException as e:
                        print(e)
                        sleep(5)
                        continue
                    except ConnectionError as c:
                        print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                        sleep(15)
                        continue
                    except ReadTimeout as rt:
                        print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                        sleep(15)
                        continue
                break    
            else:
                print("Ticks validados, sem operação comprada no momento.")
                sleep(2)
                break
    elif aberta == 1:
        open_position=True
        while True:
            sleep(2)
            df = getminutedata(symbol)
            print("Em posição comprada verifica sinal contrario")
            #Valida sinal contrario
            if ta.trend._ema(df.Close, 9).iloc[-2] >= ta.trend._ema(df.Close, 34).iloc[-2] \
            and ta.trend._ema(df.Close, 9).iloc[-1] <= ta.trend._ema(df.Close, 34).iloc[-1]:
                while True:    
                    try:
                        order = client.futures_create_order(symbol=symbol, side='SELL',                                            
                                                    type='MARKET', quantity=qty, RedunceOnly='true')
                        print(order)
                        print(f'Foi executado uma venda de {lote} lotes no ativo {symbol} - Operação finalizada')
                        open_position = False
                        break
                    except BinanceAPIException as e:
                        print(e)
                        sleep(15)
                        continue
                    except ConnectionError as c:
                        print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                        sleep(15)
                        continue
                    except ReadTimeout as rt:
                        print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                        sleep(15)
                        continue
                break
            else:
                sleep(5)
                cruzamentoc(symbol=symbol, qty=lote)
                cgraficoligado(symbol = symbol)
    elif aberta == 2: pass


def cruzamentov(symbol, qty):
    #Verifica se esta em posicao antes do robo entrar no caso vendido
    aberta = jaabertap(symbol=symbol)
    if aberta == False:
        open_position = False
        while True:
            df = getminutedata(symbol)
            #Cancela ordens caso usuario tem ordens abertas no ativo - Segurança
            print("Verifica sinal de venda.")
            if ta.trend._ema(df.Close, 9).iloc[-2] >= ta.trend._ema(df.Close,34).iloc[-2] \
            and ta.trend._ema(df.Close,9).iloc[-1] <= ta.trend._ema(df.Close,34).iloc[-1]:
                atr = ta.volatility.AverageTrueRange(high=df.High, low = df.Low, close = df.Close, window = 14).average_true_range()
                sl = round(df.Close.iloc[-1] + (atr.iloc[-1] * 2), rou)
                while True:    
                    try:
                        order = client.futures_create_order(symbol=symbol, side="SELL",
                                            type='MARKET', quantity=lote, stoploss=sl)
                        stoploss = client.futures_create_order(symbol=symbol, side='BUY',                                            
                                                    type='STOP_MARKET', quantity=lote, closePosition = 'true', stopprice=sl)
                        print(order)
                        print(stoploss)
                        open_position = True
                        print(f'Foi executado uma compra de {lote} lotes no ativo {symbol}.')
                        break
                    except BinanceAPIException as e:
                        print(e)
                        sleep(5)
                        continue
                    except ConnectionError as c:
                        print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                        sleep(15)
                        continue
                    except ReadTimeout as rt:
                        print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                        sleep(15)
                        continue
                break
            else:
                print("Ticks validados com sucesso, sem operação vendida no momento.")
                sleep(2)
                break
    if aberta == 2:
        while True:
            sleep(2)
            df = getminutedata(symbol)
            print("Em posição vendida, verifica sinal contrario")
            if ta.trend._ema(df.Close, 9).iloc[-2] <= ta.trend._ema(df.Close, 34).iloc[-2] \
            and ta.trend._ema(df.Close, 9).iloc[-1] >= ta.trend._ema(df.Close, 34).iloc[-1]:
                while True:    
                    try:
                        order = client.futures_create_order(symbol=symbol, side='BUY',                                            
                                                    type='MARKET', quantity=qty, RedunceOnly='true')

                        print(order)
                        print(f'Foi executado uma venda de {lote} lotes no ativo {symbol}. - Operação finalizada')
                        open_position = False
                        break
                    except BinanceAPIException as e:
                        print(e)
                        sleep(5)
                        continue
                    except ConnectionError as c:
                        print('ERRO NA CONEXAO, TENTA RECONECTAR. ')
                        sleep(15)
                        continue
                    except ReadTimeout as rt:
                        print('TEMPO DE LEITURA MAXIMA ATINGIDA PARECE QUE HA UM PROBLEMA NA CONEXAO')
                        sleep(15)
                        continue
                break
            else:
                sleep(5)
                cruzamentov(symbol=symbol, qty=lote)  
                cgraficoligado(symbol = symbol)      
    elif aberta == 1: pass

def passa_informacoes(symbol=symbol):
    verifica = getposição(symbol=symbol)   
    stoploss = getstops(symbol=symbol)
    posicaoaberta = [i['symbol'] for i in verifica]
    verificalote = [i['positionAmt'] for i in verifica]
    preco_de_entrada = [i['entryPrice'] for i in verifica]
    preco_de_entrada = float(preco_de_entrada[0])
    sl = [i['stopPrice'] for i in stoploss]
    side = [i['side'] for i in stoploss]
    return verificalote, preco_de_entrada, sl, side, posicaoaberta 

def cgrafico(symbol):
    # to open/create a new html file in the write mode
    f = open('PG.html', 'w')
    # the html code which will go in the file GFG.html
    html_template = """<p style="text-align:center"><span style="font-size:16px"><strong>&nbsp;<img alt="" src="https://ckeditor.com/apps/ckfinder/userfiles/files/Design%20sem%20nome(3).jpg" style="height:50px; width:50px" />&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</strong></span><span style="font-size:16px"><strong>Ativo: """f'{symbol}'"""</strong></span><span style="font-size:16px"><strong>&nbsp; |&nbsp; Posi&ccedil;&atilde;o: ----&nbsp; |&nbsp; Lote: ----&nbsp; |&nbsp; Pre&ccedil;o de Entrada: ---- |&nbsp; Stop:&nbsp; ----&nbsp; &nbsp; &nbsp;</strong></span><span style="font-size:16px"><strong>&nbsp;</strong></span></p>
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div id="technical-analysis-chart-demo"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget(
    {
    "container_id": "technical-analysis-chart-demo",
    "width": "100%",
    "height": "100%",
    "autosize": true,
    "symbol": "BINANCE:"""f'{symbol}'"""",
    "interval": "1H",
    "timezone": "exchange",
    "theme": "dark",
    "style": "1",
    "withdateranges": true,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "save_image": false,
    "studies": [
    "ROC@tv-basicstudies",
    "StochasticRSI@tv-basicstudies",
    "MASimple@tv-basicstudies"
     ],
    "show_popup_button": true,
    "popup_width": "1000",
    "popup_height": "650",
    "locale": "en"
    }
    );
    </script>
    </div>
    <!-- TradingView Widget END -->
    """
    # writing the code into the file
    f.write(html_template)   
    # close the file
    f.close()

def cgraficoligado(symbol):
    pos = jaabertap(symbol=symbol)
    if pos == False:
        posi = '----'
        lote1 = '----'
        stop = '----'
        lado = '----'
        p_e = '----'
    elif pos == 1:
        posi = 'Comprado'
        p = passa_informacoes(symbol=symbol)
        lote1 = p[0]
        p_e = p[1]
        stop = p[2]
        stop = stop[0]
        lado = 'Comprado'
        lote1 = lote1[0]
    else: 
        posi = 'Vendido'
        p = passa_informacoes(symbol=symbol)
        lote1 = p[0]
        p_e = p[1]
        stop = p[2]
        stop = stop[0]
        lado = 'Vendido'
        lote1 = lote1[0]
    # to open/create a new html file in the write mode
    f = open('PG.html', 'w')
    # the html code which will go in the file GFG.html
    html_template = """<p style="text-align:center"><span style="font-size:16px"><strong>&nbsp;<img alt="" src="https://ckeditor.com/apps/ckfinder/userfiles/files/Design%20sem%20nome(3).jpg" style="height:50px; width:50px" />&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</strong></span><span style="font-size:16px"><strong>Ativo: """f'{symbol}'"""</strong></span><span style="font-size:16px"><strong>&nbsp; |&nbsp; Posi&ccedil;&atilde;o: """f'{posi}'"""&nbsp; |&nbsp; Lote: """f'{lote1}'"""&nbsp; |&nbsp; Pre&ccedil;o de Entrada: """f'{p_e}'""" |&nbsp; Stop:&nbsp; """f'{stop}'"""&nbsp; &nbsp; &nbsp;</strong></span><span style="font-size:16px"><strong>&nbsp;</strong></span></p>
    <!--TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div id="technical-analysis-chart-demo"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget(
    {
    "container_id": "technical-analysis-chart-demo",
    "width": "100%",
    "height": "100%",
    "autosize": true,
    "symbol": "BINANCE:"""f'{symbol}'"""",
    "interval": "1H",
    "timezone": "exchange",
    "theme": "dark",
    "style": "1",
    "withdateranges": true,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "save_image": false,
    "studies": [
    "ROC@tv-basicstudies",
    "StochasticRSI@tv-basicstudies",
    "MASimple@tv-basicstudies"
     ],
    "show_popup_button": true,
    "popup_width": "1000",
    "popup_height": "650",
    "locale": "en"
    }
    );
    </script>
    </div>
    <!-- TradingView Widget END -->
    """
    # writing the code into the file
    f.write(html_template)   
    # close the file
    f.close()


cgrafico(symbol=symbol)
webbrowser.open('PG.html') 
while True:
    cgraficoligado(symbol)
    cruzamentoc(symbol=symbol, qty=lote)
    cruzamentov(symbol=symbol, qty=lote)