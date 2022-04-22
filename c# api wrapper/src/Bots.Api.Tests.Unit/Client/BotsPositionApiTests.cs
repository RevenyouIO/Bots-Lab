using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Client;
using Bots.Api.Configuration;
using Bots.Api.Models.Enums;
using Bots.Api.Models.Positions;
using FluentAssertions;
using Microsoft.Extensions.Options;
using RichardSzalay.MockHttp;
using Xunit;

namespace Bots.Api.Tests.Unit.Client {
    public class BotsPositionApiTests {
        [Fact]
        public async Task PlaceOrder_DefaultBehaviour_ResponseIsParsed() {
            // Arrange
            var options = CreateOptions();
            var request = new GetBotPositionsRequest {
                Exchange = Exchange.Binance,
                BaseAsset = "USDT"
            };
            string expectedUrl = $"{options.Value.BaseEndpoint}v2/getBotAssetsPct?signalProvider={options.Value.SignalProvider}" +
                                 $"&signalProviderKey={options.Value.SignalProviderKey}" +
                                 $"&exchange={request.Exchange.ToString().ToLower()}" +
                                 $"&baseAsset={request.BaseAsset}";
            var response = @$"{{
    ""amounts"": [{{
            ""amount"": ""17.64304360309354798982589552101697873053"",
            ""asset"": ""BTC"",
            ""exchange"": ""binance"",
            ""orderId"": """",
            ""signalId"": """"
        }}, {{
            ""amount"": ""82.35695639690645201017410447898302126946"",
            ""asset"": ""USDT"",
            ""exchange"": ""binance"",
            ""orderId"": """",
            ""signalId"": """"
        }}
    ],
    ""baseAsset"": ""USDT"",
    ""baseTotal"": ""100"",
    ""exchange"": ""binance"",
    ""signalProvider"": ""signal-provider"",
    ""success"": true
}}
";
            var mockHttp = new MockHttpMessageHandler();
            mockHttp.Expect(HttpMethod.Get, expectedUrl)
                .Respond("application/json", response);
            var positionClient = new BotsPositionApi(options, mockHttp.ToHttpClient());

            // Act
            var result = await positionClient.GetBotPositions(request);

            // Assert
            mockHttp.VerifyNoOutstandingExpectation();
            result.Should().NotBeNull();
            result.Success.Should().BeTrue();
            result.SignalProvider.Should().Be("signal-provider");
            result.Exchange.Should().Be(Exchange.Binance);
            result.BaseAsset.Should().Be("USDT");
            result.BaseTotal.Should().Be(100m);
            result.Amounts.Should().HaveCount(2);
            var btcAmount = result.Amounts.First(x => x.Asset == "BTC");
            btcAmount.Amount.Should().Be(17.64304360309354798982589552101697873053m);
            btcAmount.Exchange.Should().Be(Exchange.Binance);
            btcAmount.OrderId.Should().BeEmpty();
            btcAmount.SignalId.Should().BeEmpty();
            var usdtAmount = result.Amounts.First(x => x.Asset == "USDT");
            usdtAmount.Amount.Should().Be(82.35695639690645201017410447898302126946m);
            usdtAmount.Asset.Should().Be("USDT");
            usdtAmount.Exchange.Should().Be(Exchange.Binance);
            usdtAmount.OrderId.Should().BeEmpty();
            usdtAmount.SignalId.Should().BeEmpty();
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