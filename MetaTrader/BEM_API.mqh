//+------------------------------------------------------------------+
//|                                                      BEM_API.mqh |
//|                                                             BOTS |
//|                                        https://docs.revenyou.io/ |
//+------------------------------------------------------------------+
#property copyright "RevenYou BOTS"
#property link      "https://docs.revenyou.io/"
#property version   "1.00"
#property strict

struct OrderId
{
   string signalProvider;
   string signalProviderKey;
   string orderId;
   string extId;
};

struct AssetsRequest
{
   string signalProvider;
   string signalProviderKey;
   string exchange;
   string baseAsset;
};

struct OrderParameters
{
   string signalProvider;
   string signalProviderKey;
   string extId;
   string exchange;
   string baseAsset;
   string quoteAsset;
   string type;
   string side;
   string limitPrice;
   string stopPrice;
   string qtyPct;
   string ttlType;
   string ttlSecs;
   string responseType;
   
   OrderParameters()
   {
      signalProvider = "";
      signalProviderKey = "";
      extId = "";
      exchange = "binance";
      baseAsset = "";
      quoteAsset = "";
      type = "limit";
      side = "";
      limitPrice = "";
      stopPrice = "";
      qtyPct = "";
      ttlType = "gtc";
      ttlSecs = "";
      responseType = "ACK";
   }
};

class BEM_API
  {
private:

   string m_url;
   
private:
   string GetStringPair(string key, string value);
   string ReplaceSpace(string in);
   
public:

   BEM_API(string url);
   ~BEM_API();
   
   string PlaceOrder(OrderParameters &params);
   string CancelOrder(OrderId &id);
   string GetOrderInfo(OrderId &id);
   string GetOrderState(OrderId &id);
   string GetOrders(string signalProvider, string signalProviderKey);
   string GetBotAssetsPct(AssetsRequest &request);
   
  };
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
BEM_API::BEM_API(string url)
  {
   m_url = url;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
BEM_API::~BEM_API()
  {
  }
//+------------------------------------------------------------------+
string BEM_API::PlaceOrder(OrderParameters &params)
{
   string url = m_url + "/placeOrder";
   
   string body = "{";
   body += GetStringPair("signalProvider",params.signalProvider) + ",";
   body += GetStringPair("signalProviderKey",params.signalProviderKey) + ",";
   body += GetStringPair("extId",params.extId) + ",";
   body += GetStringPair("exchange",params.exchange) + ",";
   body += GetStringPair("baseAsset",params.baseAsset) + ",";
   body += GetStringPair("quoteAsset",params.quoteAsset) + ",";
   body += GetStringPair("limitPrice",params.limitPrice) + ",";
   body += GetStringPair("stopPrice",params.stopPrice) + ",";
   body += GetStringPair("qtyPct",params.qtyPct) + ",";
   body += GetStringPair("side",params.side) + ",";
   body += GetStringPair("ttlType",params.ttlType) + ",";
   body += GetStringPair("ttlSecs",params.ttlSecs) + ",";
   body += GetStringPair("type",params.type) + ",";
   body += GetStringPair("responseType",params.responseType);
   body += "}";

   uchar outbuffer[];
   uchar inbuffer[];
   string headers = "application/json";
   string resultHeader;

   ArrayResize(outbuffer, StringToCharArray(body, outbuffer)-1);

   ResetLastError();
   int response = WebRequest("POST", url, headers, 5000, outbuffer, inbuffer, resultHeader);

   string result = CharArrayToString(inbuffer); 

   return result;
}
//+------------------------------------------------------------------+
string BEM_API::CancelOrder(OrderId &id)
{
   ResetLastError();
   
   string url = m_url + "/cancelOrder";

   string body = "{";
   body += GetStringPair("signalProvider",id.signalProvider) + ",";
   body += GetStringPair("signalProviderKey",id.signalProviderKey) + ",";
   body += GetStringPair("orderId",id.orderId) + ",";
   body += GetStringPair("extId",id.extId);
   body += "}";

   uchar outbuffer[];
   uchar inbuffer[];
   string headers = "application/json";
   string resultHeader;

   ArrayResize(outbuffer, StringToCharArray(body, outbuffer)-1);

   ResetLastError();
   int response = WebRequest("POST", url, headers, 5000, outbuffer, inbuffer, resultHeader);

   string result = CharArrayToString(inbuffer); 
   
   return result;

}
//+------------------------------------------------------------------+
string BEM_API::GetOrderInfo(OrderId &id)
{
   ResetLastError();

   string url = m_url + "/getOrderInfo?";
   url += ("signalProvider=" + ReplaceSpace(id.signalProvider));
   url += ("&signalProviderKey=" + ReplaceSpace(id.signalProviderKey));
   url += ("&orderId=" + ReplaceSpace(id.orderId));
   url += ("&extId=" + ReplaceSpace(id.extId));
   
   uchar outBuffer[];
   uchar inBuffer[];
   string headers = "application/json";
   string resultHeader;

   int response = WebRequest("GET", url, headers, 5000, outBuffer, inBuffer, resultHeader);
   
   string result = CharArrayToString(inBuffer);
   
   return result;
}
//+------------------------------------------------------------------+
string BEM_API::GetOrderState(OrderId &id)
{
   ResetLastError();

   string url = m_url + "/getOrderState?";
   url += ("signalProvider=" + ReplaceSpace(id.signalProvider));
   url += ("&signalProviderKey=" + ReplaceSpace(id.signalProviderKey));
   url += ("&orderId=" + ReplaceSpace(id.orderId));
   url += ("&extId=" + ReplaceSpace(id.extId));
   
   uchar outBuffer[];
   uchar inBuffer[];
   string headers = "application/json";
   string resultHeader;

   int response = WebRequest("GET", url, headers, 5000, outBuffer, inBuffer, resultHeader);
   
   string result = CharArrayToString(inBuffer);
   
   return result;
}

//+------------------------------------------------------------------+
string BEM_API::GetOrders(string signalProvider,string signalProviderKey)
{
   ResetLastError();

   string url = m_url + "/getOrders?";
   url += ("signalProvider=" + ReplaceSpace(signalProvider));
   url += ("&signalProviderKey=" + ReplaceSpace(signalProviderKey));
   
   uchar outBuffer[];
   uchar inBuffer[];
   string headers = "application/json";
   string resultHeader;

   int response = WebRequest("GET", url, headers, 5000, outBuffer, inBuffer, resultHeader);
   
   string result = CharArrayToString(inBuffer);
   
   return result;
}
//+------------------------------------------------------------------+

string BEM_API::GetBotAssetsPct(AssetsRequest &request)
{
   ResetLastError();

   string url = m_url + "/getBotAssetsPct?";
   url += ("signalProvider=" + ReplaceSpace(request.signalProvider));
   url += ("&signalProviderKey=" + ReplaceSpace(request.signalProviderKey));
   url += ("&exchange=" + ReplaceSpace(request.exchange));
   url += ("&baseAsset=" + ReplaceSpace(request.baseAsset));
   
   uchar outBuffer[];
   uchar inBuffer[];
   string headers = "application/json";
   string resultHeader;

   int response = WebRequest("GET", url, headers, 5000, outBuffer, inBuffer, resultHeader);
   
   string result = CharArrayToString(inBuffer);
   
   return result;
}

//+------------------------------------------------------------------+
string BEM_API::GetStringPair(string key, string value)
{
   string pair = StringConcatenate("\"",key,"\"",":","\"",value,"\"");
   return pair;
}
//+------------------------------------------------------------------+
string BEM_API::ReplaceSpace(string in)
{
   string replaced = in;
   StringReplace(replaced," ","+");
   return replaced;
}
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+