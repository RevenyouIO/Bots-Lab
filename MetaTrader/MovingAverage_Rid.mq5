//+------------------------------------------------------------------+
//|                                            MovingAverage_Rid.mq5 |
//|                                                         Rid      |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Rid"
#property link      "https://www.mql5.com"
#property version   "1.00"

#include <BEMAPI.mqh>


input group "BEM API Configuration";
input string signalProvider = "SignalProvider";// Name of the Bot
input string signalProviderKey = "SignalProviderKey";// Secret key
input string baseAsset = "BTC";// Base asset of the order. Side of the order pertains to this asset
input string quoteAsset = "USDT";// Quote asset of the order
input double Lot = "0.1";

input group "Fast Moving Average Settings";
input int period = 3;// Period
input int shift = 0;// Shift
input ENUM_MA_METHOD method = MODE_EMA;// Method
input ENUM_APPLIED_PRICE price = PRICE_CLOSE;//Price

input group "Slow Moving Average Settings";
input int period_slow = 9;// Period
input int shift_slow = 0;// Shift
input ENUM_MA_METHOD method_slow = MODE_EMA;// Method
input ENUM_APPLIED_PRICE price_slow = PRICE_CLOSE;//Price


// Variables
int handle_moving_average, handle_moving_average_slow;
MqlRates rates[];
datetime candle_verification;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

int OnInit()
  {
//--- create timer
   EventSetTimer(60);
   
   // Moving Average Handler
   handle_moving_average = iMA(_Symbol, _Period, period, shift, method, price);
   
   if(handle_moving_average == INVALID_HANDLE)
   {       
      Comment("Moving Average Handler Error");      
   }     
   
   if(!ChartIndicatorAdd(0,0,handle_moving_average))      
   {       
      //Print("Erro ao inserir indicador Média Curta no gáfico");      
   }    
   else      
   {       
      Comment("Moving Average Indicator Successfully Added");   
   }
   
   
   handle_moving_average_slow = iMA(_Symbol, _Period, period_slow, shift_slow, method_slow, price_slow);
   
   if(handle_moving_average_slow == INVALID_HANDLE)
   {       
      Comment("Moving Average Handler Error");      
   }     
   
   if(!ChartIndicatorAdd(0,0,handle_moving_average_slow))      
   {       
      //Print("Erro ao inserir indicador Média Curta no gáfico");      
   }    
   else      
   {       
      Comment("Moving Average Indicator Successfully Added");   
   }
   
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
   Analysis();
   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//---
   
  }
//+------------------------------------------------------------------+
int Analysis()
{
   double fast_moving_average[];
   double slow_moving_average[];
   ArraySetAsSeries(fast_moving_average, true);
   ArraySetAsSeries(slow_moving_average, true);
   
   // Copy Candle
   ArraySetAsSeries(rates,true);    
   if(CopyRates(_Symbol,_Period,0,5,rates) < 0)      
   {       
      Alert("Rates Error");
      return 0;      
   }
   
   // Candle Verification
   if(candle_verification == rates[0].time)
   {
      return 0;
   }
   else
   {
      candle_verification = rates[0].time;
   }
   
   // Buffers
   if(CopyBuffer(handle_moving_average, 0, 0, 5, fast_moving_average) < 0)
   {         
      PrintFormat("Moving Average Indicator Error: %d",GetLastError());
      return 0;
   }
   
   if(CopyBuffer(handle_moving_average_slow, 0, 0, 5, slow_moving_average) < 0)
   {         
      PrintFormat("Moving Average Indicator Error: %d",GetLastError());
      return 0;
   }
   
   
   // Buy
   if(fast_moving_average[1] >= slow_moving_average[1] && fast_moving_average[2] < slow_moving_average[2])
   {
      int rand_int = rand() * rand();
      string side = "buy";
      //ArrowBuy(rates[0].close);
      if(placeOrder(signalProvider, signalProviderKey, rand_int, baseAsset, quoteAsset, "limit", side, DoubleToString(rates[0].close), Lot, "gtc", "FULL", "binance", "", "") == true)
      {
         Comment("Buy order placed with success!");
         return 1;
      }     
      
   }
   
   // Sell
   if(fast_moving_average[1] <= slow_moving_average[1] && fast_moving_average[2] > slow_moving_average[2])
   {
      int rand_int = rand() * rand();
      string side = "sell";
      //ArrowSell(rates[0].close);
      if(placeOrder(signalProvider, signalProviderKey, rand_int, baseAsset, quoteAsset, "limit", side, DoubleToString(rates[0].close), Lot, "gtc", "FULL", "binance", "", "") == true)
      {
         Comment("Sell order placed with success!");
         return -1;
      }
      
   }
   
   
   return(0);
}


//+------------------------------------------------------------------+ 
//|     
//+------------------------------------------------------------------+ 
void ArrowBuy(double entry_price)
{
   ObjectCreate(0,"Buy " + DoubleToString(entry_price, 1),OBJ_ARROW_BUY,0,0,entry_price);
   ObjectSetInteger(0,"Buy " + DoubleToString(entry_price, 1),OBJPROP_WIDTH,2);
   ObjectSetInteger(0,"Buy " + DoubleToString(entry_price, 1),OBJPROP_COLOR,clrIndigo);
}


void ArrowSell(double entry_price)
{
   ObjectCreate(0,"SELL " + DoubleToString(entry_price, 1),OBJ_ARROW_SELL,0,0,entry_price);
   ObjectSetInteger(0,"SELL " + DoubleToString(entry_price, 1),OBJPROP_WIDTH,2);
   ObjectSetInteger(0,"SELL " + DoubleToString(entry_price, 1),OBJPROP_COLOR,clrRed);
}
