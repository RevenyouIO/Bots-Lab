using System.IO;
using Bots.Api.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;

namespace Bots.Api.Tests.Integration.Client {
    public abstract class BaseBotsIntegrationTestClient {
        protected IOptions<BotsConfiguration> CreateOptions() {
            var configuration = GetConfiguration();
            var botsConfigurationSection = configuration.GetSection("BotsConfiguration");
            var botsConfiguration = botsConfigurationSection.Get<BotsConfiguration>();
            
            return Options.Create(botsConfiguration);
        }

        private IConfiguration GetConfiguration() {
            var builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("secrets.json", true)
                .AddEnvironmentVariables();

            var configuration = builder.Build();

            return configuration;
        }
    }
}