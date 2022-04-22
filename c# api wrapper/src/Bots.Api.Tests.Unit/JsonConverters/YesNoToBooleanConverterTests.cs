using Bots.Api.JsonConverters;
using FluentAssertions;
using Newtonsoft.Json;
using Xunit;

namespace Bots.Api.Tests.Unit.JsonConverters {
    public class YesNoToBooleanConverterTests {
        public class ClassToSerialize {
            [JsonConverter(typeof(YesNoToBooleanConverter))]
            public bool? BooleanValue { get; set; }
        }
        
        [Theory]
        [InlineData("yes", true)]
        [InlineData("no", false)]
        [InlineData("", null)]
        [InlineData(null, null)]
        public void Deserialize_ConvertsToYesNo(string value, bool? expectedResult) {
            // Arrange
            var jsonToDeserialize = @$"{{""BooleanValue"":""{value}""}}";

            // Act
            var result = JsonConvert.DeserializeObject<ClassToSerialize>(jsonToDeserialize);

            // Assert
            result.BooleanValue.Should().Be(expectedResult);
        }

        [Theory]
        [InlineData(true, "\"yes\"")]
        [InlineData(false, "\"no\"")]
        [InlineData(null, "null")]
        public void Serialize_ConvertsToYesNo(bool? value, string expectedResult) {
            // Arrange
            var model = new ClassToSerialize {
                BooleanValue = value
            };

            // Act
            var result = JsonConvert.SerializeObject(model);

            // Assert
            result.Should().Be(@$"{{""BooleanValue"":{expectedResult}}}");
        }
    }
}