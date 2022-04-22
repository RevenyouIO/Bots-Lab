using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Configuration;
using Bots.Api.Extensions;
using Bots.Api.Models.Positions;
using Microsoft.Extensions.Options;

namespace Bots.Api.Client {
    public class BotsPositionApi : BaseHttpClient, IBotsPositionApi {
        private readonly BotsConfiguration _options;
        
        public BotsPositionApi(IOptions<BotsConfiguration> options, HttpClient httpClient = null) 
            : base(options.Value.BaseEndpoint, httpClient) {
            _options = options.Value;
        }

        public async Task<GetBotPositionsResponse> GetBotPositions(GetBotPositionsRequest request) {
            var queryParameters = new Dictionary<string, string>();
            queryParameters.AddValueIfNotNullOrEmpty("signalProvider", _options.SignalProvider);
            queryParameters.AddValueIfNotNullOrEmpty("signalProviderKey", _options.SignalProviderKey);
            queryParameters.AddValueIfNotNullOrEmpty("exchange", request.Exchange.ToString().ToLower());
            queryParameters.AddValueIfNotNullOrEmpty("baseAsset", request.BaseAsset);
            var queryString = queryParameters.ToQueryString();
            
            return await this.GetAsync<GetBotPositionsResponse>($"v2/getBotAssetsPct{queryString}");
        }
    }
}