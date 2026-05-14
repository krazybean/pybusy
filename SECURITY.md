# Security Policy

## Reporting a Vulnerability

Please report suspected vulnerabilities privately by opening a GitHub security advisory for this repository, if available, or by contacting the maintainer directly before publishing details.

Include:

- The affected `pybusy` version
- A minimal reproduction or proof of concept
- Any relevant environment details
- Whether the issue appears exploitable only in terminals, CI logs, package installation, or another context

The maintainer will acknowledge reports as soon as practical and coordinate a fix, release, and disclosure timeline based on severity.

## Release Integrity

Official releases are expected to be built from repository tags and published to PyPI by GitHub Actions using PyPI Trusted Publishing. Release artifacts are accompanied by SHA256 checksums generated during the build workflow. PyPI publish attestations, when present, provide provenance for the publishing workflow identity; they do not prove that the source code is bug-free, reviewed, or non-malicious.
