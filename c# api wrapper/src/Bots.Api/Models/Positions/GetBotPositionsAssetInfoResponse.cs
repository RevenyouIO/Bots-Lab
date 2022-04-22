using Bots.Api.JsonConverters;
using Bots.Api.Models.Enums;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Bots.Api.Models.Positions {
    public class GetBotPositionsAssetInfoResponse {
        [JsonProperty("exchange")]
        [JsonConverter(typeof(StringEnumConverter))]
        public Exchange Exchange { get; set; }
        
        [JsonProperty("asset")]
        public string Asset { get; set; }
        
        [JsonProperty("signalId")]
        public string SignalId { get; set; }
        
        [JsonProperty("orderId")]
        public string OrderId { get; set; }
        
        [JsonProperty("amount")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal Amount { get; set; }
        
        [JsonProperty("amountBase")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal AmountBase { get; set; }
    }
}