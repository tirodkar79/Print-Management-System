
$mainList =@()


$log307 = Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-PrintService/Operational"; ID=307;}




ForEach($log307 in $log307){
  $ProperyData = [xml]$log307.ToXml()
 
  $h2ItemDetails = New-Object -TypeName psobject -Property @{
   DocName = $ProperyData.Event.UserData.DocumentPrinted.Param2
   UserName = $ProperyData.Event.UserData.DocumentPrinted.Param3
   MachineName = $ProperyData.Event.UserData.DocumentPrinted.Param4
   PrinterName = $ProperyData.Event.UserData.DocumentPrinted.Param5
   PageCount = $ProperyData.Event.UserData.DocumentPrinted.Param8
   TimeCreated = $log307.TimeCreated
   }
  $mainList += ,(@($h2ItemDetails))
 }




Write-Host $mainList