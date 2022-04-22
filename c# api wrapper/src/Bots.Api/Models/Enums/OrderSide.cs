using System.Runtime.Serialization;

namespace Bots.Api.Models.Enums {
    public enum OrderSide {
        [EnumMember(Value = "buy")] Buy,
        [EnumMember(Value = "sell")] Sell,
    }
}