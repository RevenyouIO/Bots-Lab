using Bots.Api.JsonConverters;
using Bots.Api.Models.Enums;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Bots.Api.Models.Orders {
    public class PlaceOrderRequest : BaseRequestModel {
        [JsonProperty("extId")]
        public string ExternalId { get; set; }
        
        [JsonProperty("exchange")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public Exchange Exchange { get; set; }
        
        [JsonProperty("baseAsset")]
        public string BaseAsset { get; set; }
        
        [JsonProperty("quoteAsset")]
        public string QuoteAsset { get; set; }
        
        [JsonProperty("type")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public OrderType Type { get; set; }
        
        [JsonProperty("side")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public OrderSide Side { get; set; }
        
        [JsonProperty("limitPrice")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal LimitPrice { get; set; }
        
        [JsonProperty("stopPrice")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal StopPrice { get; set; }
        
        [JsonProperty("qtyPct")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal QuantityPercent { get; set; }
        
        [JsonProperty("ttlType")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public TtlType TtlType { get; set; }
        
        [JsonProperty("ttlSecs")]
        [JsonConverter(typeof(IntToStringConverter))]
        public int TtlSecs { get; set; }
        
        [JsonProperty("responseType")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public ResponseType ResponseType { get; set; }
    }
}