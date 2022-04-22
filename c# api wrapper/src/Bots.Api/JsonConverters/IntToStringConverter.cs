using System;
using System.Globalization;
using Newtonsoft.Json;

namespace Bots.Api.JsonConverters {
    public class IntToStringConverter : JsonConverter {
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer) {
            if (value == null) {
                writer.WriteNull();
            }
            
            var valueInt = (int)value;
            writer.WriteValue(valueInt.ToString(CultureInfo.InvariantCulture));
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer) {
            var value = reader.Value;
            if (value == null || string.IsNullOrEmpty(value.ToString())) {
                return null;
            }

            if (int.TryParse(value.ToString(), out var result)) {
                return result;
            }
            throw new ArgumentException($"Error while converting string to int: \"{value}\" of type: {objectType}");
        }

        public override bool CanConvert(Type objectType) {
            return objectType == typeof(int);
        }

        public override bool CanWrite => true;
    }
}