# A lesson that cites documentation

This fixture exists to pin URL extraction. It cites the Claude docs twice, which
must deduplicate to one entry, and one other host.

First citation: https://docs.claude.com/en/docs/claude-code/overview

A sentence ending in a URL, so the full stop must be stripped rather than kept as
part of the address: https://modelcontextprotocol.io/specification.

The same Claude docs page again, which must NOT produce a second entry:
https://docs.claude.com/en/docs/claude-code/overview

A markdown link, whose closing bracket must not be swallowed:
[the spec](https://modelcontextprotocol.io/specification)

Not a URL and must not match: docs.claude.com without a scheme, and ftp://example.org.
