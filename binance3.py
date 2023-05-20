from binance.client import Client
import csv
import time
from binance.enums import *

user_key = '57730420ff758f4b3efa3f0d5b86a2083103816eb5982808e32f0c1f2663bf5f'
secret_key = '5270cea3b14bd90260a46ed726e061fae1dfcc677d75bbfa1a79f4d8ab6aefea'
interval = 1
symbol = "BTCUSDT"
binance_client = Client(user_key, secret_key,base_endpoint='https://testnet.binancefuture.com/fapi/v1/order',tld='com',testnet=True)



csv_file = open("BTCtrade_futures_log.csv", "a", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Action", "orderId", "symbol", "status", "clientOrderId", "price", "avgPrice", "origQty", "executedQty", "cumQuote", "timeInForce", "type", "reduceOnly", "closePosition", "side", "positionSide", "stopPrice", "workingType", "priceProtect", "origType", "time", "updateTime"])


print('i am here')
count = 5

while count>0:
    try:

        binance_client.futures_symbol_ticker(symbol='BTCUSDT')

        binance_client.futures_change_leverage(symbol='BTCUSDT', leverage=1)

        buy_order =binance_client.futures_create_order(
            symbol='BTCUSDT',
            type='MARKET',
            side='BUY',
            quantity=0.001
        )

        #waiting for order book to fill
        while True:

            order_info = binance_client.futures_get_order(
                symbol=symbol,
                orderId=buy_order['orderId']
            )

            status = order_info['status']

            if status == 'FILLED':

                print(order_info)
                buy_order_id = order_info['orderId']
                buy_price = float(order_info['avgPrice'])
                buy_quantity = float(order_info['executedQty'])
                buy_total = float(order_info['cumQuote'])

                
                csv_writer.writerow([time.time(), "BUY", order_info["orderId"], order_info["symbol"], order_info["status"], order_info["clientOrderId"], order_info["price"], order_info["avgPrice"], order_info["origQty"], order_info["executedQty"], order_info["cumQuote"], order_info["timeInForce"], order_info["type"], order_info["reduceOnly"], order_info["closePosition"], order_info["side"], order_info["positionSide"], order_info["stopPrice"], order_info["workingType"], order_info["priceProtect"], order_info["origType"], order_info["time"], order_info["updateTime"]])
                csv_file.flush()

                break

            time.sleep(1)

    except Exception as e:
        print(f"Error placing buy order: {e}")
            

        
    time.sleep( 1 * 60)    

    try:

        sell_order = binance_client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=0.001
        )

        
        while True:

            order_info = binance_client.futures_get_order(
                symbol=symbol,
                orderId=sell_order['orderId']
            )

            status = order_info['status']

            if status == 'FILLED':

                print(order_info)
                
                sell_order_id = order_info['orderId']
                sell_price = float(order_info['avgPrice'])
                sell_quantity = float(order_info['executedQty'])
                sell_total = float(order_info['cumQuote'])

                
                csv_writer.writerow([time.time(), "SELL", order_info["orderId"], order_info["symbol"], order_info["status"], order_info["clientOrderId"], order_info["price"], order_info["avgPrice"], order_info["origQty"], order_info["executedQty"], order_info["cumQuote"], order_info["timeInForce"], order_info["type"], order_info["reduceOnly"], order_info["closePosition"], order_info["side"], order_info["positionSide"], order_info["stopPrice"], order_info["workingType"], order_info["priceProtect"], order_info["origType"], order_info["time"], order_info["updateTime"]])
                csv_file.flush()

                break

            time.sleep(1)


    except Exception as e:
            print(f"Error placing buy order: {e}")    

        
    time.sleep(interval * 60)

    count=count-1    




