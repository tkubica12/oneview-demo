# PowerShell script to demonstrate OneView interaction
# Creating and booting one or more servers
# Tomas Kubica

param(
  [String[]] $Servers,
  [String] $Hardware = "BL460c Gen9 1",
  [String] $Connection,
  [ValidateSet('NONE','RAID0','RAID1')]
  [String] $Raid,
  [Int32] $Drives = 2
  )


Import-Module HPOneView.200

# Connect, if not connected already
if (-not($global:ConnectedSessions))
{
	Connect-HPOVMgmt -Hostname 192.168.89.100 -UserName Administrator -Password HPEnet123
}

foreach ($Server in $Servers) {

  Write-Host "Creating server $Server"

  # Get list of unassigned servers and select first available
  $selectedServer = ""
  $unassignedServers = Get-HPOVServer -NoProfile
  foreach ($unassignedServer in $unassignedServers) {
    $hardwareUri = Get-HPOVServerHardwareType -Name $Hardware
    if ($unassignedServer.serverHardwareTypeUri -eq $hardwareUri.uri) {
      $selectedServer = $unassignedServer
      break
    }
  }

  # Check whether server is power on and if yes, power off
  if ($selectedServer -ne "Off") {
    Write-Host "Turning server power off"
    Stop-HPOVServer -Server $selectedServer -Force -Confirm
  }

  # Create connection  profile
  if ($Connection) {
    $connectivity = Get-HPOVNetwork $Connection | New-HPOVServerProfileConnection -Name My_connection -ConnectionID 1
    }

  # Create logical disk
  if ($Raid) {
    $logicalDisk = New-HPOVServerProfileLogicalDisk -RAID $Raid -NumberofDrives $Drives -Name My_drive -Bootable $True
    }


  # Create server profile
  if ($Raid -And $Connection) {
    New-HPOVServerProfile -Name $Server -Server $selectedServer -AssignmentType server -LocalStorage  -LogicalDisk $logicalDisk -Initialize -ManageBoot -Connections @($connectivity)
    }
  elseif ($Connection) {
    New-HPOVServerProfile -Name $Server -Server $selectedServer -AssignmentType server -Connections @($connectivity)
    }
  elseif ($Raid) {
    New-HPOVServerProfile -Name $Server -Server $selectedServer -AssignmentType server -LocalStorage  -LogicalDisk $logicalDisk -Initialize -ManageBoot
    }
  else {
    New-HPOVServerProfile -Name $Server -Server $selectedServer -AssignmentType server
  }
}
