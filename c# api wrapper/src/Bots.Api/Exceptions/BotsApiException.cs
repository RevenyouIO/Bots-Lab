using System;
using Bots.Api.Models.Error;

namespace Bots.Api.Exceptions {
    public class BotsApiException : Exception {
        public string Response { get; private set; }
        public ErrorResponse Error { get; private set; }
        
        public BotsApiException(string message, string json) : base(message) {
            Response = json;
        }
        
        public BotsApiException(string message, string json, ErrorResponse error) : base(message) {
            Response = json;
            Error = error;
        }
    }
}