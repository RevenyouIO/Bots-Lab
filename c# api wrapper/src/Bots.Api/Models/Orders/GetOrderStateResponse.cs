using Bots.Api.JsonConverters;
using Bots.Api.Models.Enums;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Bots.Api.Models.Orders {
    public class GetOrderStateResponse : BaseResponseModel {
        [JsonProperty("orderId")]
        public string OrderId { get; set; }
        
        [JsonProperty("status")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public OrderStatus Status { get; set; }
        
        [JsonProperty("isBeingCanceled")]
        [JsonConverter(typeof(YesNoToBooleanConverter))] 
        public bool IsBeingCanceled { get; set; }
        
        [JsonProperty("rejReason")]
        public string RejectionReason { get; set; }
    }
}