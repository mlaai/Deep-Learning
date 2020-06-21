using Microsoft.WindowsAzure.Storage.Table;
using System;
using System.Collections.Generic;
using System.Text;

namespace Mlaai
{
    public class Mlaai
    {
        public string PartitionKey { get; set; }
        public string RowKey { get; set; } = Guid.NewGuid().ToString("n");
        public string Data { get; set; }
    }

    public class MlaaiCreateModel
    {
        public string PartitionKey { get; set; }
        public string Data { get; set; }
    }

    public class MlaaiUpdateModel
    {
        public string Data { get; set; }
    }

    public class MlaaiTableEntity : TableEntity
    {
        public string Data { get; set; }
    }

    public static class Mappings
    {
        public static MlaaiTableEntity ToTableEntity(this Mlaai mlaai)
        {
            return new MlaaiTableEntity()
            {
                PartitionKey = mlaai.PartitionKey,
                RowKey = mlaai.RowKey,
                Timestamp = System.DateTime.UtcNow,
                Data = mlaai.Data
            };
        }

        public static Mlaai ToMlaai(this MlaaiTableEntity mlaai)
        {
            return new Mlaai()
            {
                RowKey = mlaai.RowKey,
                Data = mlaai.Data
            };
        }
    }
}
