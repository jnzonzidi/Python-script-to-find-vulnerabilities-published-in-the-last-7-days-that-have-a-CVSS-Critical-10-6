# Python-script-to-find-vulnerabilities-published-in-the-last-7-days-that-have-a-CVSS-Critical-10-6
Python script to find vulnerabilities published in the last 7 days that have a CVSS Critical score between 10 and 6


First, I need to figure out which API to use. The NVD (National Vulnerability Database) API is the standard for this. They have a REST API that allows querying vulnerabilities. I should check the latest documentation to confirm the endpoints and parameters.

The user wants vulnerabilities from the last 7 days. So, the script needs to calculate the start and end dates. Using Python's datetime module, subtracting 7 days from today for the start date, and today's date as the end date.

Next, the CVSS score. The user mentions CVSS Critical with a perfect score between 10 and 6. Wait, CVSS scores range from 0 to 10. Critical severity usually corresponds to 9.0-10.0. But the user wrote "between 10 and 6", which is a bit confusing. Maybe they meant Critical (9.0-10) and High (7.0-8.9)? Or perhaps they want scores from 6 to 10? The user clarified "Critical" but the CVSS score for Critical is 9.0-10.0. Maybe they intended to include High severity as well. I should note this ambiguity and adjust the parameters accordingly. The script can filter based on cvssV3Metrics or cvssV2Vector. The NVD API allows filtering by CVSS V3 severity. So using the 'cvssV3Severity' parameter set to 'CRITICAL' would fetch Critical vulnerabilities. But the user also mentions a score between 6 and 10. That suggests they might want High and Critical (7.0 and above). But the original question says "CVSS Critical with perfect score of CVSS between 10 and 6". Maybe they want Critical (9.0-10) but also scores down to 6.0? That seems conflicting. I should proceed with Critical (9.0-10) and note that the user might need to adjust the parameters if they want a different range.

The API endpoint for the NVD is something like https://services.nvd.nist.gov/rest/json/cves/2.0. The parameters include 'cvssV3Severity=CRITICAL' and a publish date range. Let me check the API docs. The NVD API 2.0 allows parameters like `cvssV3Severity`, `pubStartDate`, `pubEndDate`. So constructing the URL with those parameters.

The script will make a GET request to the NVD API with the appropriate parameters. Then parse the JSON response. Extract the CVE ID, description, CVSS score, severity, and publication date for each vulnerability.

Handling API rate limits is important. The NVD API has rate limits, so the script should include a delay between requests. Maybe 6 seconds as per the guidelines to avoid hitting the rate limit.

Error handling is also necessary. Check for HTTP errors, handle exceptions, and ensure the script doesn't crash on network issues.

Once the data is retrieved, the script should format and print the results in a readable way, perhaps tabulated.

Testing the script is important. The user can run it and see if it fetches the correct vulnerabilities. They might need an API key if they exceed the anonymous request limit, but for occasional use, the default should work.

Potential improvements: Adding command-line arguments for date range and CVSS score, saving results to a file, or integrating with other tools. But the basic script should cover the user's immediate needs.

Now, putting it all together: Calculate dates, construct the API URL, make the request with a delay, parse the response, and display the results. Also, handle pagination since the NVD API might return multiple pages of results. Wait, the NVD 2.0 API uses a different structure, maybe with `vulnerabilities` array. So looping through each item in the response.

I should also note that the user might need to install the requests library if they haven't already. Including exception handling for that.

Finally, advising the user on how to adjust the parameters if they want a different CVSS range or severity level.


Below is a Python script that leverages the NVD (National Vulnerability Database) API to fetch vulnerabilities published in the last 7 days with a CVSS v3 score of 6.0 or higher (Critical/Severe)
