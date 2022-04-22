using System;
using System.Globalization;
using Newtonsoft.Json;

namespace Bots.Api.JsonConverters {
    public class DecimalToStringConverter : JsonConverter {
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer) {
            if (value == null) {
                writer.WriteNull();
            }
            
            var valueDecimal = (decimal)value;
            writer.WriteValue(valueDecimal.ToString(CultureInfo.InvariantCulture));
;        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer) {
            var value = reader.Value;
            if (value == null || string.IsNullOrEmpty(value.ToString())) {
                return null;
            }

            if (decimal.TryParse(value.ToString(), out var result)) {
                return result;
            }
            throw new ArgumentException($"Error while converting string to decimal: \"{value}\" of type: {objectType}");
        }

        public override bool CanConvert(Type objectType) {
            return objectType == typeof(decimal);
        }

        public override bool CanWrite => true;
    }
}