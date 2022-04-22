using Newtonsoft.Json;

namespace Bots.Api.Models {
    public class BaseResponseModel {
        [JsonProperty("success")]
        public bool Success { get; set; }
    }
}