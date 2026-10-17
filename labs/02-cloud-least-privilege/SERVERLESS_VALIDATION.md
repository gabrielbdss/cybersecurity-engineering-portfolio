# Synthetic serverless boundary validation

The existing least-privilege lab compares **declared** grants with **declared** needs. This small complementary Python check evaluates a fictional internal-only Cloud Run API declaration, without any GCP account or API call.

## Policy under test

The fixture must declare:
- a nonempty service name;
- a user-managed runtime service-account string;
- internal-only ingress;
- explicitly named service-account invokers, not `allUsers` or `allAuthenticatedUsers`;
- enabled invoker IAM check.

Run from the repository root:

```bash
python3 labs/02-cloud-least-privilege/review_serverless.py
python3 -m unittest discover -s labs/02-cloud-least-privilege -p 'test_review_serverless.py' -v
```

A valid synthetic declaration returns `PASS`, exit 0. Invalid or missing settings return `FAIL`, exit 1. The test suite includes positive, negative, malformed and CLI exit-code scenarios.

**Boundary:** Input is a manually supplied fictional JSON object. The validator does not query Google Cloud, prove effective IAM/ingress, validate workload identity federation or protect an actual deployed endpoint. Its model is intentionally narrower than a cloud security audit.
