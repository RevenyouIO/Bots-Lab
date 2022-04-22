using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Bots.Api.Exceptions;
using Bots.Api.Models;
using Bots.Api.Models.Error;
using Newtonsoft.Json;

namespace Bots.Api.Client {
    public abstract class BaseHttpClient {
        private readonly string _baseUrl;
        private readonly HttpClient _httpClient;
        
        protected BaseHttpClient(string baseUrl, HttpClient httpClient = null) {
            this._baseUrl = baseUrl;
            this._httpClient = httpClient ?? new HttpClient();
        }
        
        protected async Task<T> GetAsync<T>(string relativeUri) where T : BaseResponseModel {
            return await this.SendHttpRequest<T>(HttpMethod.Get, relativeUri).ConfigureAwait(false);
        }
        
        protected async Task<T> PostAsync<T>(string relativeUri, object data) where T : BaseResponseModel {
            return await this.SendHttpRequest<T>(HttpMethod.Post, relativeUri, data).ConfigureAwait(false); ;
        }
        
        private async Task<T> SendHttpRequest<T>(HttpMethod httpMethod, string relativeUri, object data = null) where T : BaseResponseModel {
            HttpRequestMessage httpRequest = this.CreateHttpRequest(httpMethod, relativeUri);
            if (data != null) {
                var jsonData = JsonConvert.SerializeObject(data, CreateSerializerSettings());
                var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
                httpRequest.Content = content;
            }

            var response = await this._httpClient.SendAsync(httpRequest).ConfigureAwait(false);
            return await this.ProcessHttpResponseMessage<T>(response).ConfigureAwait(false);
        }
        
        private async Task<T> ProcessHttpResponseMessage<T>(HttpResponseMessage response) where T : BaseResponseModel {
            var resultContent = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

            if (response.IsSuccessStatusCode) {
                var result = JsonConvert.DeserializeObject<T>(resultContent);
                if (result?.Success == true) {
                    return result;
                }
                
                throw new BotsApiException($"Response indicates Success=false but HttpStatusCode={(int)response.StatusCode}", resultContent);
            }

            try {
                var error = JsonConvert.DeserializeObject<ErrorResponse>(resultContent);
                throw new BotsApiException($"Http request was not successful " +
                                           $"HttpStatusCode={(int) response.StatusCode} " +
                                           $"ErrorCode={error?.ErrorCode} " +
                                           $"ErrorMessage={error?.ErrorMessage}", resultContent, error);
            }
            catch (JsonReaderException) {
                throw new BotsApiException($"Http request was not successful HttpStatusCode={(int)response.StatusCode}",resultContent);
            }
        }
        
        protected virtual HttpRequestMessage CreateHttpRequest(HttpMethod method, string relativeUri, HttpContent content = null) {
            HttpRequestMessage httpRequest = new HttpRequestMessage(method, new Uri(new Uri(this._baseUrl), relativeUri));
            httpRequest.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            httpRequest.Content = content;

            return httpRequest;
        }

        private JsonSerializerSettings CreateSerializerSettings() {
            return new JsonSerializerSettings {
                NullValueHandling = NullValueHandling.Ignore,
                Formatting = Formatting.Indented
            };
        }
    }
}