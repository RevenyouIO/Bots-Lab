using System.Runtime.Serialization;

namespace Bots.Api.Models.Enums {
    public enum TtlType {
        [EnumMember(Value = "secs")] Seconds,
        [EnumMember(Value = "gtc")] GoodTillCanceled
    }
}