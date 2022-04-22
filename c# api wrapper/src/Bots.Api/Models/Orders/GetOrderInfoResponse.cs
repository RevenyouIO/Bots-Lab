using System;
using System.Collections.Generic;
using Bots.Api.JsonConverters;
using Bots.Api.Models.Enums;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Bots.Api.Models.Orders {
    public class GetOrderInfoResponse : BaseResponseModel {
        [JsonProperty("orderId")]
        public string OrderId { get; set; }
        
        [JsonProperty("signaleId")]
        public string SignaleId { get; set; }
        
        [JsonProperty("extId")]
        public string ExternalId { get; set; }
        
        [JsonProperty("signalProvider")]
        public string SignalProvider { get; set; }
        
        [JsonProperty("exchange")]
        [JsonConverter(typeof(StringEnumConverter))] 
        public Exchange Exchange { get; set; }
        
        [JsonProperty("baseAsset")]
        public string BaseAsset { get; set; }
        
        [JsonProperty("quoteAsset")]
        public string QuoteAsset { get; set; }
        
        [JsonProperty("type")]
        [JsonConverter(typeof(StringEnumConverter))]
        public OrderType OrderType { get; set; }
        
        [JsonProperty("side")]
        [JsonConverter(typeof(StringEnumConverter))]
        public OrderSide OrderSide { get; set; }
        
        [JsonProperty("limitPrice")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal LimitPrice { get; set; }
        
        [JsonProperty("stopPrice")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal StopPrice { get; set; }
        
        [JsonProperty("priceAvgExec")]
        public decimal AveragePriceExecution { get; set; }
        
        [JsonProperty("qtyPct")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal QuantityPercent { get; set; }
        
        [JsonProperty("ttlType")]
        [JsonConverter(typeof(StringEnumConverter))]
        public TtlType TtlType { get; set; }
        
        [JsonProperty("ttlSecs")]
        [JsonConverter(typeof(IntToStringConverter))]
        public int TtlSecs { get; set; }
        
        [JsonProperty("status")]
        [JsonConverter(typeof(StringEnumConverter))]
        public OrderStatus Status { get; set; }
        
        [JsonProperty("isBeingCanceled")]
        [JsonConverter(typeof(YesNoToBooleanConverter))]
        public bool IsBeingCanceled { get; set; }
        
        [JsonProperty("qtyExecPct")]
        [JsonConverter(typeof(DecimalToStringConverter))]
        public decimal QuantityExecutedPercentage { get; set; }
        
        [JsonProperty("creationTs")]
        public DateTime CreationTimestampUtc { get; set; }
        
        [JsonProperty("lastChangeTs")]
        public DateTime UpdatedTimestampUtc { get; set; }
        
        [JsonProperty("rejReason")]
        public string RejectionReason { get; set; }

        [JsonProperty("trades")]
        public IEnumerable<GetOrderInfoTradesResponse> Trades { get; set; } = new List<GetOrderInfoTradesResponse>();
    }
}