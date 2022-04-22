using Bots.Api.JsonConverters;
using FluentAssertions;
using Newtonsoft.Json;
using Xunit;

namespace Bots.Api.Tests.Unit.JsonConverters {
    public class DecimalToStringConverterTests {
        private class ClassToSerialize {
            [JsonConverter(typeof(DecimalToStringConverter))]
            public decimal? DecimalValue { get; set; }
        }
        
        [Theory]
        [InlineData("1.04", 1.04f)]
        [InlineData("-1.035", -1.035f)]
        [InlineData("", null)]
        [InlineData(null, null)]
        public void Deserialize_ConvertsDecimalValue(string value, float? expectedResult) {
            // Arrange
            var jsonToDeserialize = @$"{{""DecimalValue"":""{value}""}}";

            // Act
            var result = JsonConvert.DeserializeObject<ClassToSerialize>(jsonToDeserialize);

            // Assert
            result.DecimalValue.Should().Be((decimal?)expectedResult);
        }

        [Theory]
        [InlineData(1.04f, "\"1.04\"")]
        [InlineData(-1.035f, "\"-1.035\"")]
        [InlineData(null, "null")]
        public void Serialize_ConvertsToYesNo(float? value, string expectedResult) {
            // Arrange
            var model = new ClassToSerialize {
                DecimalValue = (decimal?)value
            };

            // Act
            var result = JsonConvert.SerializeObject(model);

            // Assert
            result.Should().Be(@$"{{""DecimalValue"":{expectedResult}}}");
        }
    }
}