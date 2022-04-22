# Bots.Api
![](https://github.com/Viincenttt/Bots.Api/workflows/Bots.Api%20-%20Build%20and%20test/badge.svg)

This project allows you to easily communicate with the bots.io API using C# and .NET. Bots.io has provided documentation for their API which I highly recommend you read before using this library. 

## Support
If you have encounter any issues while using this library or have any feature requests, feel free to open an issue on GitHub. If you need fast support or need help integrating the api client in your .NET application, feel free to contact me on [LinkedIn](https://www.linkedin.com/in/vincent-kok-4aa44211/). 

## Contributions
Have you spotted a bug or want to add a missing feature? All pull requests are welcome! Please provide a description of the bug or feature you have fixed/added.

## Getting started
The easiest way to install the Bots Api library is to use the [Nuget Package](https://www.nuget.org/packages/BotsIO.Api).
```
Install-Package BotsIO.Api
```

### Supported endpoints
This library currently supports all the Order and Position API endpoints:
- Orders API: PlaceOrder
- Orders API: CancelOrder
- Orders API: GetOrderState
- Orders API: GetOrderInfo
- Orders API: GetOrders
- Positions API: GetBotAssetsPct

At the moment the Signals API endpoints are not implemented. If you'd like to use the Signals endpoints, feel free to fork the repository and create a pull request! 

### Configuration
If you are using dependency injection in your project, the package contains a `IServiceCollection` extension method you can use to register the dependencies. For example: 

#### **`appsettings.json`**
```json
{
  "BotsConfiguration": {
    "BaseEndpoint": "https://signal.revenyou.io/paper/api/signal/",
    "SignalProvider": "<your-signal-provider>",
    "SignalProviderKey": "<your-signal-provider-key>"
  } 
}
```

#### **`Startup.cs`**
```c#
serviceCollection.AddBotsApiServices(configuration.GetSection("BotsConfiguration"));
```

You will now be able to inject the `IBotsOrderApi` and `IBotsPositionApi` classes in your application. If you do not want to use dependency injection, you can create the classes manually as follows:
```c#
var orderApi = new BotsOrderApi(Options.Create(new BotsConfiguration {
    BaseEndpoint = "https://signal.revenyou.io/paper/api/signal/",
    SignalProvider = "<your-signal-provider>",
    SignalProviderKey = "<your-signal-provider-key>"
}));

var positionApi = new BotsPositionApi(Options.Create(new BotsConfiguration {
    BaseEndpoint = "https://signal.revenyou.io/paper/api/signal/",
    SignalProvider = "<your-signal-provider>",
    SignalProviderKey = "<your-signal-provider-key>"
}));
```

### Calling API endpoints
After you have constructed or injected a `IBotsOrderApi` or `IBotsPositionApi` class, you can simply call any of the endpoints that are available in the API. For example:
```c#
var orderApi = new BotsOrderApi(options, httpClient);
var placeOrderRequest = new PlaceOrderRequest {
    ExternalId = Guid.NewGuid().ToString(),
    Exchange = Exchange.Binance,
    BaseAsset = "BTC",
    QuoteAsset = "USDT",
    LimitPrice = 40000.56m,
    QuantityPercent = 50,
    Side = OrderSide.Sell,
    TtlType = TtlType.GoodTillCanceled,
    Type = OrderType.Limit,
    ResponseType = ResponseType.Ack
};
var placeOrderResult = await orderApi.PlaceOrder(placeOrderRequest);
```

Need more examples? Take a look at the integration tests for the Order API or Position API here: 
https://github.com/Viincenttt/Bots.Api/blob/master/src/Bots.Api.Tests.Integration/Client/BotsIntegrationTestOrderApi.cs
https://github.com/Viincenttt/Bots.Api/blob/master/src/Bots.Api.Tests.Integration/Client/BotsIntegrationTestPositionApi.cs
