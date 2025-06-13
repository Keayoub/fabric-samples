# PowerShell script to bulk create Fabric shortcuts from a CSV file
# Place this script in the shortcuts folder and run it from the project root
# Ensure you have a CSV file named shortcuts.csv in the shortcuts folder with columns: location,subpath,connectionId,workspace,lakehouse,shortcutName

param(
    [string]$CsvPath = "shortcuts.csv",
    [string]$shortcutType = "adlsGen2"  # Default shortcut type
)

# Ensure user is connected to fab CLI
try {
    $fabStatus = fab account show 2>$null
}
catch {
    Write-Host "You are not connected to Fabric CLI. Please run 'fab auth login' and try again."
    exit 1
}


if (!(Test-Path $CsvPath)) {
    Write-Host "CSV file not found: $CsvPath"
    exit 1
}

$csvRows = Import-Csv -Path $CsvPath

foreach ($row in $csvRows) {
    $workspaceName = $row.workspace
    $lakehouseName = $row.lakehouse
    $targetName = $row.target
    $shortcutName = $row.shortcutName
    $shortcutFullPath = "$workspaceName.workspace/$lakehouseName.lakehouse/Files/$targetName/$shortcutName.Shortcut"

    # Get all workspaces
    $workspace = fab api -X get workspaces -q "text.value[?displayName=='$workspaceName'].{id:id, name:displayName}" | ConvertFrom-Json

    if (-not $workspace) {
        Write-Error "Workspace '$workspaceName' not found."
        continue
    }

    $workspaceId = $workspace.id
    Write-Host "Workspace ID for '$workspaceName': $workspaceId"

    # # Get lakehouses in the workspace
    # $lakehouse = fab api -X get "workspaces/$workspaceId/lakehouses" -q  "text.value[?displayName=='$lakehouseName'].{id:id, name:displayName, type:type}" | ConvertFrom-Json
    # if (-not $lakehouse) {
    #     Write-Error "Lakehouse '$lakehouseName' not found in workspace '$workspaceName'."
    #     continue
    # }

    # $lakehouseId = $lakehouse.id
    # Write-Host "Lakehouse ID for '$lakehouseName': $lakehouseId"

    $json = @{ location = $row.location; subpath = "/$($row.subpath)"; connectionId = $row.connectionId } | ConvertTo-Json -Compress
    Write-Host "Creating shortcut: $shortcutFullPath" -ForegroundColor Cyan
    $fablncmd = "fab ln '$shortcutFullPath' --type $shortcutType -i '$json' -f"
    Write-Host $fablncmd -ForegroundColor Yellow
    $lsResult = Invoke-Expression $fablncmd
    if ($lsResult) {
        Write-Host $lsResult
    }
    Write-Host "Shortcut created successfully: $shortcutFullPath" -ForegroundColor Green
    Write-Host "--------------------------------------------------"
}