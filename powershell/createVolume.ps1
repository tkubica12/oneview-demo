# PowerShell script to demonstrate OneView interaction
# Creating volumes
# Tomas Kubica

param([String[]] $Volumes, [Int64] $Size)

Import-Module HPOneView.200

# Connect, if not connected already
if (-not($global:ConnectedSessions))
{
	Connect-HPOVMgmt -Hostname 192.168.89.100 -UserName Administrator -Password HPEnet123
}

# Get Storage pool
$pool = Get-HPOVStoragePool CPG-SSD

# Create volumes for each name in input
foreach ($volume in $Volumes) {
  New-HPOVStorageVolume -Name $volume -StoragePool $pool -Capacity $Size -Description "Created with PowerShell"
}
