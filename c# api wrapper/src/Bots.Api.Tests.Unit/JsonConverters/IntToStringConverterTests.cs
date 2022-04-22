using Bots.Api.JsonConverters;
using FluentAssertions;
using Newtonsoft.Json;
using Xunit;

namespace Bots.Api.Tests.Unit.JsonConverters {
    public class IntToStringConverterTests {
        public class DecimalToStringConverterTests {
            private class ClassToSerialize {
                [JsonConverter(typeof(IntToStringConverter))]
                public int? IntValue { get; set; }
            }
        
            [Theory]
            [InlineData("1", 1)]
            [InlineData("-1", -1)]
            [InlineData("", null)]
            [InlineData(null, null)]
            public void Deserialize_ConvertsIntValue(string value, int? expectedResult) {
                // Arrange
                var jsonToDeserialize = @$"{{""IntValue"":""{value}""}}";

                // Act
                var result = JsonConvert.DeserializeObject<ClassToSerialize>(jsonToDeserialize);

                // Assert
                result.IntValue.Should().Be(expectedResult);
            }

            [Theory]
            [InlineData(1, "\"1\"")]
            [InlineData(-1, "\"-1\"")]
            [InlineData(null, "null")]
            public void Serialize_ConvertsToYesNo(int? value, string expectedResult) {
                // Arrange
                var model = new ClassToSerialize {
                    IntValue = value
                };

                // Act
                var result = JsonConvert.SerializeObject(model);

                // Assert
                result.Should().Be(@$"{{""IntValue"":{expectedResult}}}");
            }
        }
    }
}