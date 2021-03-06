# PowerShell script to demonstrate OneView interaction
# Deleting volumes
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

# Delete volume for each name in input
foreach ($volume in $Volumes) {
  Get-HPOVStorageVolume $volume | Remove-HPOVStorageVolume -Confirm
}
