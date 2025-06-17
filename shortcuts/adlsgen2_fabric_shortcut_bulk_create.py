import argparse
import csv
import subprocess
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def main():
    parser = argparse.ArgumentParser(description="Bulk create Fabric shortcuts from ADLS Gen2 folders.")
    parser.add_argument('--account-url', required=True, help='ADLS Gen2 account URL (e.g. https://<account>.dfs.core.windows.net)')
    parser.add_argument('--container', required=True, help='ADLS Gen2 container name')
    parser.add_argument('--connection-id', required=True, help='Fabric connectionId')
    parser.add_argument('--workspace', required=True, help='Fabric workspace name')
    parser.add_argument('--lakehouse', required=True, help='Fabric lakehouse name')
    parser.add_argument('--shortcut-type', default='adlsGen2', help='Shortcut type (default: adlsGen2)')
    parser.add_argument('--root-path', default='', help='Root path in the container to scan (default: root)')
    args = parser.parse_args()

    credential = DefaultAzureCredential()
    service_client = BlobServiceClient(account_url=args.account_url, credential=credential)
    container_client = service_client.get_container_client(args.container)

    rows = []
    folders = set()

    # List all folders at the root (or under root_path)
    for blob in container_client.walk_blobs(name_starts_with=args.root_path, delimiter='/'):
        if hasattr(blob, 'name') and blob.name.endswith('/'):
            folder_name = blob.name.rstrip('/')
            folders.add(folder_name)

    # For each folder, create shortcut and record CSV row
    for folder_name in sorted(folders):
        shortcut_name = f"shortcut_{folder_name.replace('/', '_')}"
        target = folder_name
        subpath = folder_name
        # Build shortcut JSON
        shortcut_json = {
            "location": args.account_url,
            "subpath": f"/{subpath}",
            "connectionId": args.connection_id
        }
        # Build shortcut path for fab CLI
        shortcut_full_path = f"{args.workspace}.workspace/{args.lakehouse}.lakehouse/Files/{target}/{shortcut_name}.Shortcut"
        # Call fab CLI to create the shortcut
        fab_cmd = [
            "fab", "ln", shortcut_full_path,
            "--type", args.shortcut_type,
            "-i", str(shortcut_json).replace("'", '"'),
            "-f"
        ]
        print(f"Creating shortcut: {shortcut_full_path}")
        try:
            result = subprocess.run(fab_cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except Exception as e:
            print(f"Error running fab CLI: {e}")
        # Record for CSV
        rows.append({
            "location": args.account_url,
            "subpath": subpath,
            "connectionId": args.connection_id,
            "workspace": args.workspace,
            "lakehouse": args.lakehouse,
            "target": target,
            "shortcutName": shortcut_name
        })

    # Write shortcuts.csv for record-keeping
    with open("shortcuts.csv", "w", newline='') as csvfile:
        fieldnames = ["location", "subpath", "connectionId", "workspace", "lakehouse", "target", "shortcutName"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("All shortcuts created and shortcuts.csv written.")

if __name__ == "__main__":
    main()
