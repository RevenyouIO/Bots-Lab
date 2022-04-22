using Newtonsoft.Json;

namespace Bots.Api.Models {
    public abstract class BaseRequestModel {
        [JsonProperty("signalProvider")]
        public string SignalProvider { get; set; }
        
        [JsonProperty("signalProviderKey")]
        public string SignalProviderKey { get; set; }
    }
}