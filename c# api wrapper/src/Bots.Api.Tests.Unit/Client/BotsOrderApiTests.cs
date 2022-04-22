using System;
using System.Globalization;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Client;
using Bots.Api.Configuration;
using Bots.Api.Exceptions;
using Bots.Api.Models.Enums;
using Bots.Api.Models.Orders;
using FluentAssertions;
using Microsoft.Extensions.Options;
using RichardSzalay.MockHttp;
using Xunit;

namespace Bots.Api.Tests.Unit.Client {
    public class BotsOrderApiTests {
        [Fact]
        public async Task PlaceOrder_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/placeOrder";
            var orderId = "order-id";
            var response = @$"{{
    ""isBeingCanceled"": ""no"",
    ""orderId"": ""{orderId}"",
    ""status"": ""acceptedByExch"",
    ""success"": true
}}";
            var placeOrderRequest = CreatePlaceOrderRequest(options.Value);
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Post, expectedUrl)
                .WithPartialContent(CreatePlaceOrderRequestJson(placeOrderRequest, options.Value))
                .Respond("application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await orderClient.PlaceOrder(placeOrderRequest);

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.OrderId.Should().Be(orderId);
            result.IsBeingCanceled.Should().BeFalse();
            result.Status.Should().Be(OrderStatus.AcceptedByExchange);
            result.Success.Should().BeTrue();
        }
        
        [Fact]
        public async Task CancelOrder_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/cancelOrder";
            var orderId = "order-id";
            var response = @$"{{
    ""success"": true
}}";
            var cancelOrderRequest = new CancelOrderRequest {
                ExternalOrderId = orderId
            };
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Post, expectedUrl)
                .WithPartialContent(CreateCancelOrderRequestJson(cancelOrderRequest, options.Value))
                .Respond("application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await orderClient.CancelOrder(cancelOrderRequest);

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.Success.Should().BeTrue();
        }

        [Fact]
        public async Task GetOrderState_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            var orderId = "order-id";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrderState?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}&orderId={orderId}";
            var getOrderStateRequest = CreateGetOrderStateRequest(options.Value, orderId);
            var response =  $@"{{
    ""isBeingCanceled"": ""no"",
    ""orderId"": ""{orderId}"",
    ""status"": ""acceptedByExch"",
    ""success"": true
}}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond("application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await orderClient.GetOrderState(getOrderStateRequest);

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.OrderId.Should().Be(orderId);
            result.IsBeingCanceled.Should().BeFalse();
            result.Status.Should().Be(OrderStatus.AcceptedByExchange);
            result.Success.Should().BeTrue();
        }
        
        [Fact]
        public async Task GetOrderInfo_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            var orderId = "order-id";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrderInfo?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}&orderId={orderId}";
            var getOrderInfoRequest = CreateGetOrderInfoRequest(options.Value, orderId);
            var response =  $@"{{
    ""baseAsset"": ""BTC"",
    ""creationTs"": ""2022-04-16 09:31:28"",
    ""exchange"": ""binance"",
    ""extId"": ""b1220bfa-b1ba-45e4-a768-42e3f6d43b6d"",
    ""isBeingCanceled"": ""no"",
    ""lastChangeTs"": ""2022-04-16 09:31:28"",
    ""limitPrice"": ""40000.56"",
    ""orderId"": ""{orderId}"",
    ""priceAvgExec"": ""40394.98"",
    ""qtyExecPct"": ""99.98765334644912267918333970906426534375"",
    ""qtyPct"": ""25"",
    ""quoteAsset"": ""USDT"",
    ""side"": ""sell"",
    ""signalProvider"": ""signal-provider"",
    ""status"": ""fulfilled"",
    ""success"": true,
    ""trades"": [{{
            ""creationTs"": ""2022-04-16 09:31:28"",
            ""id"": ""625a8cf0dd16297d2e2a39ec"",
            ""price"": ""40394.98"",
            ""qtyPct"": ""99.98765334644912267918333970906426534375""
        }}
    ],
    ""ttlSecs"": 30,
    ""ttlType"": ""secs"",
    ""type"": ""limit""
}}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond("application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await orderClient.GetOrderInfo(getOrderInfoRequest);

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.OrderId.Should().Be(orderId);
            result.ExternalId.Should().Be("b1220bfa-b1ba-45e4-a768-42e3f6d43b6d");
            result.IsBeingCanceled.Should().BeFalse();
            result.Status.Should().Be(OrderStatus.FulFilled);
            result.Success.Should().BeTrue();
            result.QuoteAsset.Should().Be("USDT");
            result.BaseAsset.Should().Be("BTC");
            result.LimitPrice.Should().Be(40000.56m);
            result.AveragePriceExecution.Should().Be(40394.98m);
            result.QuantityExecutedPercentage.Should().Be(99.98765334644912267918333970906426534375m);
            result.QuantityPercent.Should().Be(25m);
            result.OrderSide.Should().Be(OrderSide.Sell);
            result.OrderType.Should().Be(OrderType.Limit);
            result.SignalProvider.Should().Be("signal-provider");
            result.TtlSecs.Should().Be(30);
            result.TtlType.Should().Be(TtlType.Seconds);
            result.Trades.Should().HaveCount(1);
            var trade = result.Trades.First();
            trade.Id.Should().Be("625a8cf0dd16297d2e2a39ec");
            trade.Price.Should().Be(40394.98m);
            trade.QuantityPercent.Should().Be(99.98765334644912267918333970906426534375m);
        }
        
        [Fact]
        public async Task GetOrders_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            var orderId = "order-id";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrders?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}";
            var response =  $@"{{
    ""orders"": [{{
            ""baseAsset"": ""BTC"",
            ""creationTs"": ""2022-04-16 13:03:00"",
            ""exchange"": ""binance"",
            ""extId"": ""0354718f-6448-4226-abb4-d36bcd3632e1"",
            ""isBeingCanceled"": ""no"",
            ""lastChangeTs"": ""2022-04-16 13:03:00"",
            ""limitPrice"": ""41000.56"",
            ""orderId"": ""{orderId}"",
            ""priceAvgExec"": ""0"",
            ""qtyExecPct"": ""0"",
            ""qtyPct"": ""25"",
            ""quoteAsset"": ""USDT"",
            ""side"": ""sell"",
            ""signalProvider"": ""signal-provider"",
            ""status"": ""acceptedByExch"",
            ""ttlSecs"": 30,
            ""ttlType"": ""secs"",
            ""type"": ""limit""
        }}
    ],
    ""success"": true
}}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond("application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await orderClient.GetOrders();

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.Success.Should().BeTrue();
            result.Orders.Should().HaveCount(1);
            var order = result.Orders.First();
            order.OrderId.Should().Be(orderId);
            order.ExternalId.Should().Be("0354718f-6448-4226-abb4-d36bcd3632e1");
            order.IsBeingCanceled.Should().BeFalse();
            order.Status.Should().Be(OrderStatus.AcceptedByExchange);
            order.QuoteAsset.Should().Be("USDT");
            order.BaseAsset.Should().Be("BTC");
            order.LimitPrice.Should().Be(41000.56m);
            order.AveragePriceExecution.Should().Be(0m);
            order.QuantityExecutedPercentage.Should().Be(0m);
            order.QuantityPercent.Should().Be(25m);
            order.OrderSide.Should().Be(OrderSide.Sell);
            order.OrderType.Should().Be(OrderType.Limit);
            order.SignalProvider.Should().Be("signal-provider");
            order.TtlSecs.Should().Be(30);
            order.TtlType.Should().Be(TtlType.Seconds);
            order.Trades.Should().HaveCount(0);
        }

        [Fact]
        public async Task GetOrders_ApiExceptionCanBeParsed_BotsApiExceptionIsThrown() {
            // Arrange
            var options = CreateOptions();
            var errorCode = "301";
            var errorMessage = "Forbidden";
            var response = @$"{{
    ""errorCode"": {errorCode},
    ""errorMessage"": ""{errorMessage}"",
    ""success"": false
}}
";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrders?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond(HttpStatusCode.Forbidden, "application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());
            
            // Act
            var exception = await Assert.ThrowsAsync<BotsApiException>(() => orderClient.GetOrders());

            // Assert
            var expectedExceptionMessage = $@"Http request was not successful HttpStatusCode={(int)HttpStatusCode.Forbidden} ErrorCode={errorCode} ErrorMessage={errorMessage}";
            exception.Message.Should().Be(expectedExceptionMessage);
            exception.Response.Should().Be(response);
            exception.Error.Should().NotBeNull();
            exception.Error.ErrorCode.Should().Be(errorCode);
            exception.Error.ErrorMessage.Should().Be(errorMessage);
        }
        
        [Fact]
        public async Task GetOrders_ApiExceptionCannotBeParsed_BotsApiExceptionIsThrown() {
            // Arrange
            var options = CreateOptions();
            var response = @$"<html>Error</html>";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrders?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond(HttpStatusCode.InternalServerError, "text/html", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());
            
            // Act
            var exception = await Assert.ThrowsAsync<BotsApiException>(() => orderClient.GetOrders());

            // Assert
            var expectedExceptionMessage = $@"Http request was not successful HttpStatusCode=500";
            exception.Message.Should().Be(expectedExceptionMessage);
            exception.Response.Should().Be(response);
        }
        
        [Fact]
        public async Task GetOrders_SuccessIsFalse_BotsApiExceptionIsThrown() {
            // Arrange
            var options = CreateOptions();
            var response =  $@"{{
    ""orders"": [],
    ""success"": false
}}";
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getOrders?signalProvider={options.Value.SignalProvider}&signalProviderKey={options.Value.SignalProviderKey}";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond(HttpStatusCode.OK, "application/json", response);
            var orderClient = new BotsOrderApi(options, mockHttp.ToHttpClient());
            
            // Act
            var exception = await Assert.ThrowsAsync<BotsApiException>(() => orderClient.GetOrders());

            // Assert
            var expectedExceptionMessage = $@"Response indicates Success=false but HttpStatusCode={(int)HttpStatusCode.OK}";
            exception.Message.Should().Be(expectedExceptionMessage);
            exception.Response.Should().Be(response);
        }
        
        private string CreatePlaceOrderRequestJson(PlaceOrderRequest request, BotsConfiguration options) {
            return $@"{{
  ""extId"": ""{request.ExternalId}"",
  ""exchange"": ""{request.Exchange.ToString().ToLower()}"",
  ""baseAsset"": ""{request.BaseAsset}"",
  ""quoteAsset"": ""{request.QuoteAsset}"",
  ""type"": ""{request.Type.ToString().ToLower()}"",
  ""side"": ""{request.Side.ToString().ToLower()}"",
  ""limitPrice"": ""{request.LimitPrice.ToString(CultureInfo.InvariantCulture)}"",
  ""stopPrice"": ""{request.StopPrice.ToString(CultureInfo.InvariantCulture)}"",
  ""qtyPct"": ""{request.QuantityPercent.ToString(CultureInfo.InvariantCulture)}"",
  ""ttlType"": ""secs"",
  ""ttlSecs"": ""{request.TtlSecs.ToString(CultureInfo.InvariantCulture)}"",
  ""responseType"": ""{request.ResponseType.ToString().ToUpper()}"",
  ""signalProvider"": ""{options.SignalProvider}"",
  ""signalProviderKey"": ""{options.SignalProviderKey}""
}}";
        }

        private string CreateCancelOrderRequestJson(CancelOrderRequest request, BotsConfiguration options) {
            return $@"{{
  ""extId"": ""{request.ExternalOrderId}"",
  ""signalProvider"": ""{options.SignalProvider}"",
  ""signalProviderKey"": ""{options.SignalProviderKey}""
}}";
        }

        private PlaceOrderRequest CreatePlaceOrderRequest(BotsConfiguration options) {
            return new PlaceOrderRequest {
                ExternalId = Guid.NewGuid().ToString(),
                Exchange = Exchange.Binance,
                BaseAsset = "BTC",
                QuoteAsset = "USDT",
                LimitPrice = 40000.56m,
                QuantityPercent = 25m,
                Side = OrderSide.Sell,
                TtlType = TtlType.Seconds,
                TtlSecs = 30,
                Type = OrderType.Limit,
                ResponseType = ResponseType.Ack
            };
        }

        private GetOrderStateRequest CreateGetOrderStateRequest(BotsConfiguration options, string orderId) {
            return new GetOrderStateRequest {
                OrderId = orderId
            };
        }
        
        private GetOrderInfoRequest CreateGetOrderInfoRequest(BotsConfiguration options, string orderId) {
            return new GetOrderInfoRequest {
                OrderId = orderId
            };
        }
        
        private IOptions<BotsConfiguration> CreateOptions() {
            return Options.Create(new BotsConfiguration {
                BaseEndpoint = "https://signal.revenyou.io/paper/api/signal/",
                SignalProvider = "signal-provider",
                SignalProviderKey = "signal-provider-key"
            });
        }
    }
}