param([String[]] $Volumes, [Int64] $Size)

Import-Module HPOneView.200

if (-not($global:ConnectedSessions))
{
	Connect-HPOVMgmt -Hostname 192.168.89.100 -UserName Administrator -Password HPEnet123
}

$pool = Get-HPOVStoragePool CPG-SSD

foreach ($volume in $Volumes) {
  New-HPOVStorageVolume -Name $volume -StoragePool $pool -Capacity $Size -Description "Created with PowerShell"
}
