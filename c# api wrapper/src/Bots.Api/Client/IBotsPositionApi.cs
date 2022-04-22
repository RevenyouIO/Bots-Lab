using System.Threading.Tasks;
using Bots.Api.Models.Positions;

namespace Bots.Api.Client {
    public interface IBotsPositionApi {
        Task<GetBotPositionsResponse> GetBotPositions(GetBotPositionsRequest request);
    }
}