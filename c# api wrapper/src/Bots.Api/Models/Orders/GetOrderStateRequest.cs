using Newtonsoft.Json;

namespace Bots.Api.Models.Orders {
    public class GetOrderStateRequest {
        [JsonProperty("orderId")]
        public string OrderId { get; set; }
        
        [JsonProperty("extId")]
        public string ExternalId { get; set; }
    }
}