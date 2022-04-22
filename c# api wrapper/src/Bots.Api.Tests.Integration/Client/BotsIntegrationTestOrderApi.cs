using System;
using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Client;
using Bots.Api.Models.Enums;
using Bots.Api.Models.Orders;
using FluentAssertions;
using Xunit;

namespace Bots.Api.Tests.Integration.Client {
    public class BotsIntegrationTestOrderApi : BaseBotsIntegrationTestClient {
        [Fact]
        public async Task PlaceOrder_CanPlaceOrder() {
            // Arrange
            var options = CreateOptions();
            var httpClient = new HttpClient();
            var client = new BotsOrderApi(options, httpClient);
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

            // Act
            var placeOrderResult = await client.PlaceOrder(placeOrderRequest);
            var getOrderStateRequest = new GetOrderStateRequest {
                OrderId = placeOrderResult.OrderId
            };
            var getOrderStateResult = await client.GetOrderState(getOrderStateRequest);

            // Assert
            placeOrderResult.Should().NotBeNull();
            getOrderStateResult.Should().NotBeNull();
            getOrderStateResult.OrderId.Should().Be(getOrderStateRequest.OrderId);
        }
        
        [Fact]
        public async Task GetOrdersInfo_ReturnsOrderInfo() {
            // Arrange
            var options = CreateOptions();
            var httpClient = new HttpClient();
            var client = new BotsOrderApi(options, httpClient);
            var getOrderInfoRequest = new GetOrderInfoRequest {
                OrderId = "bem-bot-5fdf0108e8f42a4ffc5fa0a1-1650101488-0001-3429175148"
            };
            
            // Act
            var order = await client.GetOrderInfo(getOrderInfoRequest);

            // Assert
            order.Should().NotBeNull();
            order.OrderId.Should().Be(getOrderInfoRequest.OrderId);
        }

        [Fact]
        public async Task GetOrders_ReturnsOrders() {
            // Arrange
            var options = CreateOptions();
            var httpClient = new HttpClient();
            var client = new BotsOrderApi(options, httpClient);
            
            // Act
            var result = await client.GetOrders();

            // Assert
            result.Should().NotBeNull();
        }

        [Fact]
        public async Task CancelAllOpenOrders() {
            // Arrange
            var options = CreateOptions();
            var httpClient = new HttpClient();
            var client = new BotsOrderApi(options, httpClient);
            
            // Act
            var result = await client.GetOrders();
            foreach (var order in result.Orders) {
                var cancelOrderResult = await client.CancelOrder(new CancelOrderRequest {
                    ExternalOrderId = order.ExternalId
                });
                cancelOrderResult.Success.Should().BeTrue();
            }

            // Assert
            result.Should().NotBeNull();
        }
    }
}