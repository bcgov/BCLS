import argparse
import json
import sys
import urllib.request

import msal


def main():
    ap = argparse.ArgumentParser(description="Simple Microsoft Graph device-login test")
    ap.add_argument("--client-id", required=True, help="Azure App Registration client ID")
    ap.add_argument("--tenant-id", required=True, help="Tenant ID or 'organizations'")
    args = ap.parse_args()

    scopes = ["Files.Read", "Sites.Read.All"]
    authority = f"https://login.microsoftonline.com/{args.tenant_id}"

    print(f"[INFO] Authority: {authority}")
    print(f"[INFO] Client ID: {args.client_id}")
    print(f"[INFO] Scopes: {scopes}")

    app = msal.PublicClientApplication(client_id=args.client_id, authority=authority)
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        print("[ERROR] Failed to start device flow.")
        print(json.dumps(flow, indent=2, ensure_ascii=False))
        return 1

    print("\n[AUTH] Complete sign-in:")
    print(flow.get("message", "Open https://microsoft.com/devicelogin and enter code"))
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        print("[ERROR] Login failed.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2

    token = result["access_token"]
    print("[OK] Access token acquired.")

    req = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/me/drive/root",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        print("[OK] Graph call succeeded: /me/drive/root")
        print(raw[:500])
        return 0
    except Exception as e:
        print(f"[ERROR] Token obtained but Graph call failed: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())

