using System.Runtime.Serialization;

namespace Bots.Api.Models.Enums {
    public enum ResponseType {
        [EnumMember(Value = "FULL")] Full,
        [EnumMember(Value = "ACK")] Ack,
    }
}