Convert-VHD -Path OneView2.vhdx -DestinationPath OneView2.vhd

Login-AzureRmAccount
New-AzureRmResourceGroup -Name OneView -Location westeurope
New-AzureRmStorageAccount -ResourceGroupName OneView -Name oneview -Location westeurope -SkuName Standard_LRS -Kind "Storage"

Add-AzureRmVhd -ResourceGroupName OneView -Destination "http://oneview.blob.core.windows.net/images/OneView2.vhd" -LocalFilePath OneView2.vhd

$singleSubnet = New-AzureRmVirtualNetworkSubnetConfig -Name ovsubnet -AddressPrefix "10.20.1.0/24"
$vnet = New-AzureRmVirtualNetwork -Name ovnet -ResourceGroupName OneView -Location westeurope -AddressPrefix "10.20.1.0/24" -Subnet $singleSubnet
$ovip = New-AzureRmPublicIpAddress -Name ovip -ResourceGroupName OneView -Location westeurope -AllocationMethod Dynamic -DomainNameLabel oneview
$ovnic = New-AzureRmNetworkInterface -Name ovnic -ResourceGroupName OneView -Location westeurope -SubnetId $vnet.Subnets[0].Id -PublicIpAddressId $ovip.Id

$password = ConvertTo-SecureString "HPEnet123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ("oneview", $password);

$storageAcc = Get-AzureRmStorageAccount -ResourceGroupName OneView -AccountName oneview
$vmConfig = New-AzureRmVMConfig -VMName ovvm -VMSize Standard_D3_v2
$vm = Set-AzureRmVMOperatingSystem -VM $vmConfig -Linux -ComputerName ovvm -Credential $cred
$vm = Add-AzureRmVMNetworkInterface -VM $vm -Id $ovnic.Id
$osDiskUri = '{0}vhds/ovvm-OneView2.vhd' -f $storageAcc.PrimaryEndpoints.Blob.ToString()
$vm = Set-AzureRmVMOSDisk -VM $vm -Name ovvm-OneView2.vhd -VhdUri $osDiskUri -CreateOption fromImage -SourceImageUri http://oneview.blob.core.windows.net/images/OneView2.vhd -Linux

New-AzureRmVM -ResourceGroupName OneView -Location westeurope -VM $vm

Write-Host "Connect with your browser to oneview.westeurope.cloudapp.azure.com"
