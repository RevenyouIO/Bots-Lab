using Bots.Api.Models.Enums;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Bots.Api.Models.Positions {
    public class GetBotPositionsRequest {
        [JsonProperty("exchange")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public Exchange Exchange { get; set; }
        
        [JsonProperty("baseAsset")]
        public string BaseAsset { get; set; }
    }
}