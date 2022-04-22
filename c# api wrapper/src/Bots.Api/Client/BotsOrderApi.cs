using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Bots.Api.Configuration;
using Bots.Api.Extensions;
using Bots.Api.Models.Orders;
using Microsoft.Extensions.Options;

namespace Bots.Api.Client {
    public class BotsOrderApi : BaseHttpClient, IBotsOrderApi {
        private readonly BotsConfiguration _options;
        
        public BotsOrderApi(IOptions<BotsConfiguration> options, HttpClient httpClient = null) 
            : base(options.Value.BaseEndpoint, httpClient) {
            _options = options.Value;
        }

        public async Task<PlaceOrderResponse> PlaceOrder(PlaceOrderRequest request) {
            request.SignalProvider = _options.SignalProvider;
            request.SignalProviderKey = _options.SignalProviderKey;
            return await this.PostAsync<PlaceOrderResponse>("v2/placeOrder", request);
        }

        public async Task<CancelOrderResponse> CancelOrder(CancelOrderRequest request) {
            request.SignalProvider = _options.SignalProvider;
            request.SignalProviderKey = _options.SignalProviderKey;
            return await this.PostAsync<CancelOrderResponse>("v2/cancelOrder", request);
        }

        public async Task<GetOrderStateResponse> GetOrderState(GetOrderStateRequest request) {
            var queryParameters = new Dictionary<string, string>();
            queryParameters.AddValueIfNotNullOrEmpty("signalProvider", _options.SignalProvider);
            queryParameters.AddValueIfNotNullOrEmpty("signalProviderKey", _options.SignalProviderKey);
            queryParameters.AddValueIfNotNullOrEmpty("extId", request.ExternalId);
            queryParameters.AddValueIfNotNullOrEmpty("orderId", request.OrderId);
            var queryString = queryParameters.ToQueryString();
            
            return await this.GetAsync<GetOrderStateResponse>($"v2/getOrderState{queryString}");
        }

        public async Task<GetOrderInfoResponse> GetOrderInfo(GetOrderInfoRequest request) {
            var queryParameters = new Dictionary<string, string>();
            queryParameters.AddValueIfNotNullOrEmpty("signalProvider", _options.SignalProvider);
            queryParameters.AddValueIfNotNullOrEmpty("signalProviderKey", _options.SignalProviderKey);
            queryParameters.AddValueIfNotNullOrEmpty("extId", request.ExternalId);
            queryParameters.AddValueIfNotNullOrEmpty("orderId", request.OrderId);
            var queryString = queryParameters.ToQueryString();
            
            return await this.GetAsync<GetOrderInfoResponse>($"v2/getOrderInfo{queryString}");
        }
        
        public async Task<GetOrdersResponse> GetOrders() {
            var queryParameters = new Dictionary<string, string>();
            queryParameters.AddValueIfNotNullOrEmpty("signalProvider", _options.SignalProvider);
            queryParameters.AddValueIfNotNullOrEmpty("signalProviderKey", _options.SignalProviderKey);
            var queryString = queryParameters.ToQueryString();
            
            return await this.GetAsync<GetOrdersResponse>($"v2/getOrders{queryString}");
        }
    }
}