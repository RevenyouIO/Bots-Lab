using System.Runtime.Serialization;

namespace Bots.Api.Models.Enums {
    public enum OrderType {
        [EnumMember(Value = "limit")] Limit,
        [EnumMember(Value = "stopLimit")] StopLimit
    }
}