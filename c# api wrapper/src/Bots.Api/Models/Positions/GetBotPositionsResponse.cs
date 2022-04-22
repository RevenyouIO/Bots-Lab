using System.Collections.Generic;
using Bots.Api.JsonConverters;
using Bots.Api.Models.Enums;
using Newtonsoft.Json;

namespace Bots.Api.Models.Positions {
    public class GetBotPositionsResponse : BaseResponseModel {
        [JsonProperty("signalProvider")]
        public string SignalProvider { get; set; }
        
        [JsonProperty("exchange")]
        public Exchange Exchange { get; set; }
        
        [JsonProperty("baseAsset")]
        public string BaseAsset { get; set; }
        
        [JsonProperty("baseTotal")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal BaseTotal { get; set; }
        
        [JsonProperty("amounts")]
        public IEnumerable<GetBotPositionsAssetInfoResponse> Amounts { get; set; }
    }
}