import requests
import json
from datetime import datetime, timedelta

# NVD API endpoint for CVEs
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_recent_critical_vulnerabilities():
    # Calculate dates for the last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Parameters for the API request
    params = {
        "pubStartDate": start_date_str,
        "pubEndDate": end_date_str,
        "cvssV3Severity": "CRITICAL"  # Filter by CRITICAL severity
    }

    try:
        # Make the API request with a delay to avoid rate-limiting
        response = requests.get(NVD_API_URL, params=params, timeout=15)
        response.raise_for_status()  # Raise HTTP errors
        data = response.json()

        # Extract relevant CVE details
        vulnerabilities = []
        for cve in data.get("vulnerabilities", []):
            cve_data = cve.get("cve", {})
            metrics = cve_data.get("metrics", {}).get("cvssMetricV31", [{}])[0]
            cvss_data = metrics.get("cvssData", {})

            # Check if CVSS score is >= 6.0
            if cvss_data.get("baseScore", 0) >= 6.0:
                vulnerabilities.append({
                    "CVE ID": cve_data.get("id"),
                    "Description": cve_data.get("descriptions", [{}])[0].get("value"),
                    "CVSS Score": cvss_data.get("baseScore"),
                    "Severity": cvss_data.get("baseSeverity"),
                    "Published": cve_data.get("published")
                })

        return vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to parse API response.")
        return []

def print_results(vulnerabilities):
    if not vulnerabilities:
        print("No critical vulnerabilities found in the last 7 days.")
        return

    print(f"Found {len(vulnerabilities)} critical vulnerabilities:\n")
    for vuln in vulnerabilities:
        print(f"CVE ID: {vuln['CVE ID']}")
        print(f"Description: {vuln['Description']}")
        print(f"CVSS Score: {vuln['CVSS Score']} ({vuln['Severity']})")
        print(f"Published: {vuln['Published']}\n{'-'*50}")

if __name__ == "__main__":
    vulns = fetch_recent_critical_vulnerabilities()
    print_results(vulns)