using System;
using Newtonsoft.Json;

namespace Bots.Api.JsonConverters {
    public class YesNoToBooleanConverter : JsonConverter {
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            if (value == null) {
                writer.WriteNull();
            }

            var boolValue = (bool) value;
            writer.WriteValue(boolValue ? "yes" : "no");
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer) {
            var value = reader.Value;
            if (value == null || String.IsNullOrWhiteSpace(value.ToString()))
            {
                return null;
            }

            return value.ToString().Equals("yes", StringComparison.OrdinalIgnoreCase);
        }

        public override bool CanConvert(Type objectType)
        {
            if (objectType == typeof(String) || objectType == typeof(Boolean))
            {
                return true;
            }
            return false;
        }

        public override bool CanWrite => true;
    }
}