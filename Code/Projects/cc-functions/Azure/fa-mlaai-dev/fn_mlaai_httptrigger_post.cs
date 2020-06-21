using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.WindowsAzure.Storage.Table;
using System.Linq;

namespace Mlaai
{
    public static class fn_mlaai_httptrigger_post
    {
        [FunctionName("fn_mlaai_httptrigger_post")]
        public static async Task<IActionResult> CreateMlaai(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "mlaai")] HttpRequest req,
            [Table("mlaai", Connection = "AzureWebJobsStorage")] IAsyncCollector<MlaaiTableEntity> mlaaiTable,
            ILogger log)
        {
            log.LogInformation("Creating a new Mlaai item");

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            var input = JsonConvert.DeserializeObject<MlaaiCreateModel>(requestBody);

            var mlaai = new Mlaai() 
            {
                PartitionKey = input.PartitionKey,
                Data = input.Data
            };
            await mlaaiTable.AddAsync(mlaai.ToTableEntity());

            return new OkObjectResult(mlaai);
        }
    }
}
