Import-Module HPOneView.200
if (-not($global:ConnectedSessions))
{
	Connect-HPOVMgmt -Hostname 192.168.89.100 -UserName Administrator -Password HPEnet123
}

Get-HPOVAlert | ForEach-Object {
  Write-Host $_.created " " $_.description
  }
