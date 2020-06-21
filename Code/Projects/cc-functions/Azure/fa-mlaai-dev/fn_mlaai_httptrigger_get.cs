using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Linq;
using Microsoft.Azure.Cosmos.Table;

namespace Mlaai
{
    public static class fn_mlaai_httptrigger_get
    {
        [FunctionName("fn_mlaai_httptrigger_get")]
        public static async Task<IActionResult> GetMlaai(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "mlaai")] HttpRequest req,
            [Table("mlaai", Connection = "AzureWebJobsStorage")] CloudTable mlaaiTable,
            ILogger log)
        {
            log.LogInformation("Get Mlaai information");
            var query = new TableQuery<MlaaiTableEntity>();
            var segment = await mlaaiTable.ExecuteQuerySegmentedAsync(query, null);
            return new OkObjectResult(segment.Select(Mappings.ToMlaai));
        }
    }
}
