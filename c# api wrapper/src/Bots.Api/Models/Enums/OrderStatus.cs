using System.Runtime.Serialization;

namespace Bots.Api.Models.Enums {
    public enum OrderStatus {
        [EnumMember(Value = "acceptedByBEM")] AcceptedByBem,
        [EnumMember(Value = "acceptedByExch")] AcceptedByExchange,
        [EnumMember(Value = "partiallyExecuted")] PartiallyExecuted,
        [EnumMember(Value = "rejectedByBEM")] RejectedByBem,
        [EnumMember(Value = "rejectedByExch")] RejectedByExchange,
        [EnumMember(Value = "partiallyExecutedAndCanceled")] PartiallyExecutedAndCanceled,
        [EnumMember(Value = "fullyCanceled")] FullyCanceled,
        [EnumMember(Value = "fulfilled")] FulFilled,
    }
}