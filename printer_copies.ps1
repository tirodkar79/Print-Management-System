
$mainList =@()
$log805 = Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-PrintService/Operational"; ID=805;}
ForEach($log805 in $log805){
  $event805 = [xml]$log805.ToXml()
 
  $h1ItemDetails = New-Object -TypeName psobject -Property @{
   Copies = $event805.Event.UserData.RenderJobDiag.Copies
   }
  $mainList += ,(@($h1ItemDetails))

 }

Write-Host $mainList