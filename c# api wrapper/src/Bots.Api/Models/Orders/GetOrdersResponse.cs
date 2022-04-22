using System.Collections.Generic;
using Newtonsoft.Json;

namespace Bots.Api.Models.Orders {
    public class GetOrdersResponse : BaseResponseModel{
        [JsonProperty("orders")]
        public IEnumerable<GetOrderInfoResponse> Orders { get; set; }
    }
}