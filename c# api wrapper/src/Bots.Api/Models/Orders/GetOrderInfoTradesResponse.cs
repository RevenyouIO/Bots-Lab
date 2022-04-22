using System;
using Bots.Api.JsonConverters;
using Newtonsoft.Json;

namespace Bots.Api.Models.Orders {
    public class GetOrderInfoTradesResponse {
        [JsonProperty("id")]
        public string Id { get; set; }
        
        [JsonProperty("creationTs")]
        public DateTime CreationTimeUtc { get; set; }
        
        [JsonProperty("price")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal Price { get; set; }
        
        [JsonProperty("qtyPct")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal QuantityPercent { get; set; }
    }
}