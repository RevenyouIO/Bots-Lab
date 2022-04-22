using Newtonsoft.Json;

namespace Bots.Api.Models.Orders {
    public class CancelOrderRequest : BaseRequestModel {
        [JsonProperty("orderID")]
        public string OrderId { get; set; }
        
        [JsonProperty("extId")]
        public string ExternalOrderId { get; set; }
    }
}