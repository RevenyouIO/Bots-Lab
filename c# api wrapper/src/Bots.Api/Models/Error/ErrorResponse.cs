using Newtonsoft.Json;

namespace Bots.Api.Models.Error {
    public class ErrorResponse : BaseResponseModel {
        [JsonProperty("errorMessage")]
        public string ErrorMessage { get; set; }
        
        [JsonProperty("errorCode")]
        public string ErrorCode { get; set; }
    }
}