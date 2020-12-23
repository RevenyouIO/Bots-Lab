####################################
# Bots_api.py
# Facilitates accessing the BEM api
# Version: 0.0.1 - Incomplete
# contact: philip@revenyou.io
# (C) Bots by RevenYOU
####################################

from dataclasses import dataclass
import json
import requests

@dataclass
class CloseTarget:
    qtyPct: str = None
    limitPricePct: str = None
    limitPriceAbs: str = None

@dataclass
class SignalParameters:
    signalProvider: str = None
    signalProviderKey: str = None
    extId: str = None
    exchange: str = None
    baseAsset: str = None
    quoteAsset: str = None
    direction: str = None
    openLimitPrice: str = None
    openQtyPct: str = None
    openQtyAbs: str = None
    openTtlType: str = None
    openTtlSecs: str = None
    closeTargets: [CloseTarget] = None
    closeTtlType: str = 'gtc'
    closeTtlSecs: str = None
    slLimitPricePct: str = None
    slLimitPriceAbs: str = None
    slStopPricePct: str = None
    slStopPriceAbs: str = None
    slTtlType: str = 'gtc'
    slTtlSecs: str = None

@dataclass
class CancelSignalParameters:
    signalProvider: str = None
    signalProviderKey: str = None
    signalId: str = None
    extId: str = None

@dataclass
class OrderParameters:
    signalProvider: str = None
    signalProviderKey: str = None
    extId: str = None
    exchange: str = None
    baseAsset: str = None
    quoteAsset: str = None
    type: str = 'limit'
    side: str = None
    limitPrice: str = None
    stopPrice: str = None
    qtyPct: str = None
    qtyAbs: str = None
    ttlType: str = 'gtc'
    ttlSecs: str = None
    responseType: str = 'FULL'

@dataclass
class CancelOrderParameters:
    signalProvider: str = None
    signalProviderKey: str = None
    orderId: str = None
    extId: str = None

@dataclass
class OrderStateRequest:
    signalProvider: str = None
    signalProviderKey: str = None
    orderId: str = None
    extId: str = None

@dataclass
class OrderInfoRequest:
    signalProvider: str = None
    signalProviderKey: str = None
    orderId: str = None
    extId: str = None


class BEM_API:
    """
     : BEM api wrapper
    """
    exchanges = ['poloniex','binance']

    def __init__(self,host):
        self.host = host

    # Check the validity of the params
    def ValidateSignalParams(self, params: SignalParameters):

        if(params.openTtlType == 'secs' and params.openTtlSecs is None):
            return False  

        if(params.closeTtlType == 'secs' and params.closeTtlSecs is None):
            return False  

        if(params.slTtlType == 'secs' and params.slTtlSecs  is None):
            return False

        if(params.exchange not in self.exchanges):
            return False

        if(params.closeTargets is None):
            return False

        return True

    # Call BEM placeSignal
    def placeSignal(self, params: SignalParameters):
        
        path = self.host + 'placeSignal'
        message = ''
        
        if not self.ValidateSignalParams(params):
            message = 'Validate Signal Parameters returned false'
            return message

        closeList = []

        for i in params.closeTargets:
            ct = {'qtyPct': i.qtyPct, 'limitPricePct': i.limitPricePct}
            closeList.append(ct)

        sigData = {}

        sigData['signalProvider'] = params.signalProvider
        sigData['signalProviderKey'] = params.signalProviderKey
        sigData['closeTargets'] = closeList
        sigData['extId'] = params.extId
        sigData['exchange'] = params.exchange
        sigData['baseAsset'] = params.baseAsset
        sigData['quoteAsset'] = params.quoteAsset
        sigData['direction'] = params.direction
        sigData['openLimitPrice'] = params.openLimitPrice
        sigData['openQtyPct'] = params.openQtyPct
        sigData['openTtlType'] = params.openTtlType
        sigData['closeTtlType'] = params.closeTtlType
        sigData['slLimitPricePct'] = params.slLimitPricePct
        sigData['slStopPricePct'] = params.slStopPricePct
        sigData['slTtlType'] = params.slTtlType

        jsonData = json.dumps(sigData)

        response = requests.post(url = path, data = jsonData)

        return response.text

    # Call BEM cancelSignal
    def cancelSignal(self, params: CancelSignalParameters):

        path = self.host + 'cancelSignal'

        cancelRequest = {}
        cancelRequest['signalProvider'] = params.signalProvider
        cancelRequest['signalProviderKey'] = params.signalProviderKey
        cancelRequest['extId'] = params.extId

        jsonData =json.dumps(cancelRequest)

        response = requests.post(url=path, data=jsonData)

        return response.text
    
    # Call BEM placeOrder
    def placeOrder(self, params: OrderParameters):
        
        path = self.host + 'placeOrder'
        message = ''

        orderData = {}
        orderData['signalProvider'] = params.signalProvider
        orderData['signalProviderKey'] = params.signalProviderKey
        orderData['extId'] = params.extId
        orderData['exchange'] = params.exchange
        orderData['baseAsset'] = params.baseAsset
        orderData['quoteAsset'] = params.quoteAsset
        orderData['limitPrice'] = params.limitPrice
        orderData['qtyPct'] = params.qtyPct
        orderData['side'] = params.side
        orderData['ttlType'] = params.ttlType
        orderData['type'] = params.type

        jsonData =json.dumps(orderData)

        response = requests.post(url=path, data=jsonData)

        return response.text

    # Get all info about a specific order
    def getOrderInfo(self, params: OrderInfoRequest):

        path = self.host + 'getOrderInfo'
        message = ''

        pars = {'signalProvider': params.signalProvider, 'signalProviderKey': params.signalProviderKey}

        if(params.extId is not None):
            pars['extId'] = params.extId

        if(params.orderId is not None):
            pars['orderId'] = params.orderId

        response = requests.get(url= path, params=pars)

        return response.text

    # Get state of a specific order
    def getOrderState(self, params: OrderStateRequest):

        path = self.host + 'getOrderState'
        message = ''

        pars = {'signalProvider': params.signalProvider, 'signalProviderKey': params.signalProviderKey}

        if(params.extId is not None):
            pars['extId'] = params.extId

        if(params.orderId is not None):
            pars['orderId'] = params.orderId

        response = requests.get(url= path, params=pars)

        return response.text

    # Cancel a specific order
    def cancelOrder(self, params: CancelOrderParameters):

        path = self.host + 'cancelOrder'

        cancelRequest = {}
        cancelRequest['signalProvider'] = params.signalProvider
        cancelRequest['signalProviderKey'] = params.signalProviderKey

        if(params.extId is not None):
            cancelRequest['extId'] = params.extId

        if(params.orderId is not None):
            cancelRequest['orderId'] = params.orderId

        jsonData =json.dumps(cancelRequest)

        response = requests.post(url=path, data=jsonData)

        return response.text
        