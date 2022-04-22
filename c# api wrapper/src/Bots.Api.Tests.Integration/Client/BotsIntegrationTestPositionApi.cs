using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Client;
using Bots.Api.Models.Enums;
using Bots.Api.Models.Positions;
using FluentAssertions;
using Xunit;

namespace Bots.Api.Tests.Integration.Client {
    public class BotsIntegrationTestPositionApi : BaseBotsIntegrationTestClient {
        [Fact]
        public async Task PlaceOrder_CanPlaceOrder() {
            // Arrange
            var options = CreateOptions();
            var httpClient = new HttpClient();
            var client = new BotsPositionApi(options, httpClient);
            var request = new GetBotPositionsRequest {
                Exchange = Exchange.Binance,
                BaseAsset = "USDT"
            };
            
            // Act
            var positions = await client.GetBotPositions(request);

            // Assert
            positions.Should().NotBeNull();
        }
    }
}