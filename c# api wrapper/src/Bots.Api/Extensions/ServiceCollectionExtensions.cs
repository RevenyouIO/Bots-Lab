using System.Diagnostics.CodeAnalysis;
using Bots.Api.Client;
using Bots.Api.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Bots.Api.Extensions {
    [ExcludeFromCodeCoverage]
    public static class ServiceCollectionExtensions {
        public static void AddBotsApiServices(this IServiceCollection serviceCollection, IConfiguration configuration) {
            serviceCollection.Configure<BotsConfiguration>(configuration);
            serviceCollection.AddTransient<IBotsOrderApi, BotsOrderApi>();
            serviceCollection.AddTransient<IBotsPositionApi, BotsPositionApi>();
        }
    }
}