simconfig = \
{
  "Simulator" :
  {
    "Integration" : 
    {
      "DtFrac" : 0.5
    },
    "StopCondition" : 
    {
      "StopConditionFormula" :
      {
        "mtSUB" :
        {
          "mtVAR" : "t",
          "mtCONST" : 3
        }
      }
    },
    "RecordHistory" :
    {
      "RecordStepSize" : 100,
      "RecordVoxel" : 1,
      "RecordLink" : 0
    }
  }
}

envconfig = \
{
  "Environment" :
  {
    "Thermal" :
    {
      "TempEnabled" : 1,
      "VaryTempEnabled" : 1,
      "TempBase" : 25,
      "TempAmplitude" : 5, #14.4714
      "TempPeriod" : 0.2
    }
  } 
}
