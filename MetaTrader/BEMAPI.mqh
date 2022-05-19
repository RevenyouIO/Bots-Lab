//+------------------------------------------------------------------+
//|                                                       BEMAPI.mq5 |
//|                                                        TradeDevs |
//|                                                                  |
//+------------------------------------------------------------------+
#property library
#property copyright "TradeDevs"
#property link      ""
#property version   "1.00"

// Manipulate Json
#include <JAson.mqh>
CJAVal json;


//+------------------------------------------------------------------+
//| BEM API functions                                                |
//+------------------------------------------------------------------+ 

// [POST] placeOrder - Place an order on the platform
string placeOrder(string signalProvider, string signalProviderKey, string extId, string baseAsset, string quoteAsset, string type_limit, string side, string limitPrice, string qtyPct, string ttlType, string responseType, string exchange = "binance", string ttlSecs = "", string stopPrice = "")
{
   string cookie = NULL;
   string headers = "{'content-type': 'application/json', 'accept': 'application/xml'}";
   
   // Serialize JSON data
   CJAVal json;
   json["signalProvider"] = signalProvider;
   json["signalProviderKey"] = signalProviderKey;
   json["extId"] = extId;
   json["exchange"] = exchange;
   json["baseAsset"] = baseAsset;
   json["quoteAsset"] = quoteAsset;
   json["type"] = type_limit;
   json["side"] = side;
   json["limitPrice"] = limitPrice;
   json["qtyPct"] = qtyPct;
   json["ttlType"] = ttlType;
   json["responseType"] = responseType;
   json["ttlSecs"] = ttlSecs;
   json["stopPrice"] = stopPrice;
   
   //string out=""; json.Serialize(out); // serializado
   //Print(out);
   
   char jsonData[];
   ArrayResize(jsonData, StringToCharArray(json.Serialize(), jsonData, 0, WHOLE_ARRAY)-1);
   
   char serverResult[];
   string serverHeaders;
   
   string url = "https://signal.revenyou.io/paper/api/signal/v2/placeOrder";
   
   int res = WebRequest("POST", url, headers, 10000, jsonData, serverResult, serverHeaders);
   
   json.Deserialize(serverResult);
   string place_order_status = json[0].ToStr();
   
   
   // Checks ttlSecs
   if (json[1].ToStr() == "BadParameterException: Cannot get int parameter ttlSecs: [json.exception.type_error.302] type must be number, but is null")
   {
      Print("Cannot get int parameter ttlSecs: type must be number, but is null");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   // Checks qty
   if (json[1].ToStr() == "ServiceException: qty must be strictly greater than 0")
   {
      Print("qty must be strictly greater than 0");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   // Checks order quote
   if (json[12].ToStr() == "error: code=[215]; msg=[ServiceException: Order quote value is too small - 0]")
   {
      Print("Order quote value is too small - 0");
      PrintFormat("Response error:  %s", json[12].ToStr());
      return(false);
   }
   
   // Checks if extId has already been used
   int check_extId = StringFind(json[1].ToStr(), "extId", 0);
   if (check_extId > 0)
   {
      Print("Parameter extId has already been used!");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   // Checks if exists base or quote asset
   int check_asset = StringFind(json[1].ToStr(), "asset", 0);
   if (check_asset > 0)
   {
      Print("Invalid base or quote asset: Unable to find information about");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   // Checks if exists stop Price
   int check_stopPrice = StringFind(json[1].ToStr(), "stopPrice", 0);
   if (check_stopPrice > 0)
   {
      Print("Cannot get parameter stopPrice");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   
   if (json[1].ToStr() == "BadParameterException: invalid type value")
   {
      Print("BadParameterException: invalid type value");
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
   
   /*
   if (json[0].ToStr() == "230" || json[0].ToStr() == "209" || json[0].ToStr() == "42")
   {
      Print("Could not send order...");
      return(false);
   }
   */
   
   
   // Success order placed
   if (json[0].ToStr() == baseAsset)
   {
      Print("Order placed with success!");
      return(true);
   }
   
   // Get general errors
   else
   {
      Print("Could not send order...");
      Print(GetLastError());
      PrintFormat("Response error:  %s", json[1].ToStr());
      return(false);
   }
   
  
}

// [POST] cancelOrder - Cancel an order managed by the bot
string cancelOrder(string signalProvider, string signalProviderKey, string orderId="", string extId="")
{
   string cookie = NULL;
   string headers = "{'content-type': 'application/json', 'accept': 'application/xml'}";
   
   // Serialize JSON data
   CJAVal json;
   json["signalProvider"] = signalProvider;
   json["signalProviderKey"] = signalProviderKey;
   json["orderID"] = orderId;
   json["extId"] = extId;
   //string out=""; json.Serialize(out); // serializado
   //Print(out);
   
   char jsonData[];
   ArrayResize(jsonData, StringToCharArray(json.Serialize(), jsonData, 0, WHOLE_ARRAY)-1);
   
   char serverResult[];
   string serverHeaders;
   
   string url = "https://signal.revenyou.io/paper/api/signal/v2/cancelOrder";
   
   int res = WebRequest("POST", url, headers, 10000, jsonData, serverResult, serverHeaders);
   
   if (res == 200)
   {
      // Checks if order was cancelled
      json.Deserialize(serverResult);
      string cancel_order_status = json[0].ToStr();
      
      // Checks if exists order
      if (cancel_order_status == "230")
      {
         Print("Unable to find the order...");
         return(false);
      }
      
      
      // If not exception return true
      if (json.Deserialize(serverResult) == "true")
      {
         Print("Order cancelled with success!");
         return(true);
      }
      
      // General errors
      else
      {
         Print("Order could not be cancelled...");
         return(false);
      }
      
   }
   
   else
   {
      Print("Could not retrieve data from BEM API cancelOrder...");
      return(false);
   }
}
// [GET] getOrderState - Retreive the current state of an order
string getOrderState(string signalProvider, string signalProviderKey, string orderId="", string extId="")
{
   string cookie = NULL;
   string headers = "{'content-type': 'application/json', 'accept': 'application/xml'}";
   uchar jsonData[];
   char serverResult[];
   string serverHeaders;
   
   // Check if there's orderId or extId
   if (orderId == "")
   {
      string url = "https://signal.revenyou.io/paper/api/signal/v2/getOrderState?signalProvider=" + signalProvider + "&signalProviderKey=" + signalProviderKey + "&extId=" + extId;
      // Make the Request
      int res = WebRequest("GET", url, headers, 10000, jsonData, serverResult, serverHeaders);
      
      if (res == 200)
      {
         json.Deserialize(serverResult);
         
         string isBeingCancelled = json[0].ToStr();
         string orderId = json[1].ToStr();
         string status = json[2].ToStr();
         
         // Checks if there's an error code
         if (json[0].ToInt() > 0)
         {
            Print("Could not retrieve data from BEM API getOrderState...");
            return(false);
         }
         
         PrintFormat("isBeingCancelled: %s; orderId: %s; status: %s.", isBeingCancelled, orderId, status);
         return(true);
      }
      
      else
      {
         Print("Could not retrieve data from BEM API getOrderState...");
         return(false);
      }
   }
   
   else
   {
      string url = "https://signal.revenyou.io/paper/api/signal/v2/getOrderState?signalProvider=" + signalProvider + "&signalProviderKey=" + signalProviderKey + "&orderId=" + orderId;
      // Make the Request
      int res = WebRequest("GET", url, headers, 10000, jsonData, serverResult, serverHeaders);
      
      if (res == 200)
      {
         json.Deserialize(serverResult);
         
         string isBeingCancelled = json[0].ToStr();
         string orderId = json[1].ToStr();
         string status = json[2].ToStr();
         
         
         // Checks if there's an error code
         if (json[0].ToInt() > 0)
         {
            Print("Could not retrieve data from BEM API getOrderState...");
            return(false);
         }
         
         PrintFormat("isBeingCancelled: %s; orderId: %s; status: %s.", isBeingCancelled, orderId, status);
         
         return(true);
      }
      
      else
      {
         Print("Could not retrieve data from BEM API getOrderState...");
         return(false);
      }
   }
   
}

// [GET] getOrderInfo - Request complete info on a specific order
string getOrderInfo(string signalProvider, string signalProviderKey, string orderId="", string extId="")
{
   string cookie = NULL;
   string headers = "{'content-type': 'application/json', 'accept': 'application/xml'}";
   uchar jsonData[];
   char serverResult[];
   string serverHeaders;
   
   // Check if there's orderId or extId
   if (orderId == "")
   {
      string url = "https://signal.revenyou.io/paper/api/signal/v2/getOrderInfo?signalProvider=" + signalProvider + "&signalProviderKey=" + signalProviderKey + "&extId=" + extId;
      // Make the Request
      int res = WebRequest("GET", url, headers, 10000, jsonData, serverResult, serverHeaders);
      
      if (res == 200)
      {
         json.Deserialize(serverResult);
         
         string baseAsset = json[0].ToStr();
         string creationTs = json[1].ToStr();
         string exchange = json[2].ToStr();
         string lastChangeTs = json[5].ToStr();
         string extId = json[3].ToStr();
         string orderId = json[7].ToStr();
         string limitPrice = json[6].ToStr();
         string priceAvgExec = json[8].ToStr();
         string qtyExecPct = json[9].ToStr();
         string qtyPct = json[10].ToStr();
         string quoteAsset = json[11].ToStr();
         string side = json[12].ToStr();
         string status = json[14].ToStr();
         string ttlSecs = json[16].ToStr();
         string ttlType = json[17].ToStr();
         string order_type = json[18].ToStr();
         
         
         // Checks if there's an error code
         if (json[0].ToInt() > 0)
         {
            Print("Could not retrieve data from BEM API getOrderInfo...");
            return(false);
         }
            
         PrintFormat("baseAsset: %s; exchange: %s; creationTs: %s; lastChangeTs: %s, extId: %s; orderId: %s; limitPrice: %s; priceAvgExec: %s; qtyExecPct: %s; qtyPct: %s; quoteAsset: %s; side: %s; status: %s, type: %s; ttlType: %s; ttlSecs: %s.", baseAsset, exchange, creationTs, lastChangeTs, extId, orderId, limitPrice, priceAvgExec, qtyExecPct, qtyPct, quoteAsset, side, status, order_type, ttlType, ttlSecs);
         return(true);
      }
      
      else
      {
         Print("Could not retrieve data from BEM API getOrderInfo...");
         return(false);
      }
   }
   
   else
   {
      string url = "https://signal.revenyou.io/paper/api/signal/v2/getOrderInfo?signalProvider=" + signalProvider + "&signalProviderKey=" + signalProviderKey + "&orderId=" + orderId;
      // Make the Request
      int res = WebRequest("GET", url, headers, 10000, jsonData, serverResult, serverHeaders);
      
      if (res == 200)
      {
         json.Deserialize(serverResult);
         
         string baseAsset = json[0].ToStr();
         string creationTs = json[1].ToStr();
         string exchange = json[2].ToStr();
         string lastChangeTs = json[5].ToStr();
         string extId = json[3].ToStr();
         string orderId = json[7].ToStr();
         string limitPrice = json[6].ToStr();
         string priceAvgExec = json[8].ToStr();
         string qtyExecPct = json[9].ToStr();
         string qtyPct = json[10].ToStr();
         string quoteAsset = json[11].ToStr();
         string side = json[12].ToStr();
         string status = json[14].ToStr();
         string ttlSecs = json[16].ToStr();
         string ttlType = json[17].ToStr();
         string order_type = json[18].ToStr();
            
         // Checks if there's an error code
         if (json[0].ToInt() > 0)
         {
            Print("Could not retrieve data from BEM API getOrderInfo...");
            return(false);
         }
         
         PrintFormat("baseAsset: %s; exchange: %s; creationTs: %s; lastChangeTs: %s, extId: %s; orderId: %s; limitPrice: %s; priceAvgExec: %s; qtyExecPct: %s; qtyPct: %s; quoteAsset: %s; side: %s; status: %s, type: %s; ttlType: %s; ttlSecs: %s.", baseAsset, exchange, creationTs, lastChangeTs, extId, orderId, limitPrice, priceAvgExec, qtyExecPct, qtyPct, quoteAsset, side, status, order_type, ttlType, ttlSecs);
         return(true);
      }
      
      else
      {
         Print("Could not retrieve data from BEM API getOrderInfo...");
         return(false);
      }
   }
   
}

// [GET] getOrders - Request complete list of orders from a bot
string getOrders(string signalProvider, string signalProviderKey)
{
   
   string url = "https://signal.revenyou.io/paper/api/signal/v2/getOrders?signalProvider=" + signalProvider + "&signalProviderKey=" + signalProviderKey;
   string cookie = NULL;
   //string headers = "Content-Type: application/json; Accept: application/xml";
   string headers = "{'content-type': 'application/json', 'accept': 'application/xml'}";
   uchar jsonData[];
   char serverResult[];
   string serverHeaders;
   
   int res = WebRequest("GET", url, headers, 10000, jsonData, serverResult, serverHeaders);
   
   if (res == 200)
   {
      json.Deserialize(serverResult);

      //Print(json["orders"].ToStr()); // None
      long qtd_orders = json[0].Size(); // Quantity of orders in response content
      
      if (qtd_orders > 0)
      {
      
         for (long i = 0; i < qtd_orders; i++)
         {
            string baseAsset = json[0][i][0].ToStr();
            string creationTs = json[0][i][1].ToStr();
            string exchange = json[0][i][2].ToStr();
            string lastChangeTs = json[0][i][5].ToStr();
            string extId = json[0][i][3].ToStr();
            string orderId = json[0][i][7].ToStr();
            string limitPrice = json[0][i][6].ToStr();
            string priceAvgExec = json[0][i][8].ToStr();
            string qtyExecPct = json[0][i][9].ToStr();
            string qtyPct = json[0][i][10].ToStr();
            string quoteAsset = json[0][i][11].ToStr();
            string side = json[0][i][12].ToStr();
            string status = json[0][i][14].ToStr();
            string ttlSecs = json[0][i][15].ToStr();
            string ttlType = json[0][i][16].ToStr();
            string order_type = json[0][i][17].ToStr();
            
            PrintFormat("baseAsset: %s; exchange: %s; creationTs: %s; lastChangeTs: %s, extId: %s; orderId: %s; limitPrice: %s; priceAvgExec: %s; qtyExecPct: %s; qtyPct: %s; quoteAsset: %s; side: %s; status: %s, type: %s; ttlType: %s; ttleSecs: %s.", baseAsset, exchange, creationTs, lastChangeTs, extId, orderId, limitPrice, priceAvgExec, qtyExecPct, qtyPct, quoteAsset, side, status, order_type, ttlType, ttlSecs);
         }
         
         string all_orders = "Qtd Orders: " + qtd_orders;
         Print(all_orders);
         return(true);
      }
      
      else
      {
         Print("List of orders is empty!");
         return(false);
      }
      
   }
   
   else
   {
      Print("Could not retrieve data from BEM API getOrders...");
      return(false);
   }
}
//+------------------------------------------------------------------+
