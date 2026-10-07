# Security Engineering Glossary

This glossary defines recurring terms used across the portfolio.

| Term | Meaning in this portfolio |
|---|---|
| **OBSERVED** | Directly present in collected evidence |
| **VERIFIED** | Corroborated through an independent or authoritative check |
| **INFERRED** | Supported indirectly but not directly demonstrated |
| **UNVERIFIED** | Not demonstrated with available evidence |
| **Security invariant** | A property that must remain true despite hostile or unexpected input |
| **Trust boundary** | A point where identity, authority, data or execution context changes |
| **Fail closed** | Unexpected or unsafe states do not silently produce an allow/pass decision |
| **Least privilege** | Effective capability is limited to the minimum demonstrated operational need |
| **Containment** | Action intended to limit ongoing or imminent security impact |
| **Rollback** | Defined path to safely reverse a change when validation fails |
| **Synthetic evidence** | Artificial data created specifically for a controlled exercise |
| **Production-safe** | Investigation behavior designed to minimize operational mutation and risk |

## Evidence discipline

Severity and confidence are separate dimensions. A potentially severe scenario can remain low-confidence until evidence supports it.

Documentation, source code, test behavior and production observations are also separate evidence categories; one does not automatically prove another.
