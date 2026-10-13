"""The output models -- what a caller is promised, as a published schema.

Returning `dict[str, Any]` publishes an EMPTY output schema, which means an agent
has to call the tool once to find out what comes back. These models exist so the
shape is readable before the first call.

Every optional field below is explicitly nullable with an explicit default. That
is not style: under the MCP SDK a field that is merely "sometimes absent" can be
published as non-nullable while the server then serialises `None` into it, and the
served path rejects the server's own output. The in-process tests stay green
throughout, because only the served path validates.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Provenance(BaseModel):
    """Where an answer came from. Travels with the result, never in a docstring."""

    source: str = Field(
        description="What produced this answer -- here, always a local file read.",
    )
    read_at: str = Field(
        description="UTC ISO-8601 timestamp of the read, to the second.",
    )


class Diagnostics(BaseModel):
    """Caveats attached to the payload rather than left for the caller to infer.

    `what_it_does_not_show` is the field that carries this project's whole design
    goal. It is required and non-empty on every result, including successful ones,
    because the failure this package exists to prevent is a clean-looking answer
    being read as a complete one.
    """

    warnings: list[str] = Field(
        default_factory=list,
        description=(
            "Things the caller should relay to the user. An empty list means no "
            "warning was raised, NOT that the result is unqualified -- read "
            "what_it_does_not_show for that."
        ),
    )
    what_it_does_not_show: str = Field(
        description=(
            "What this result is silent about. Always populated, including on "
            "success. Do not report the result without reading it."
        ),
    )
    provenance: Provenance


class MaterialReadingResult(BaseModel):
    """A material file, read. Facts only -- no staleness verdict lives here."""

    path: str = Field(description="The path as it was passed in.")
    resolved_path: str = Field(
        description="The absolute path actually read, after root confinement.",
    )
    sha256: str = Field(
        description=(
            "SHA-256 of the file's raw bytes. This is the change detector: store it "
            "and compare on a later run. It says nothing about whether the content "
            "is correct, only whether it is the same bytes."
        ),
    )
    byte_count: int = Field(description="Size of the file in bytes.")
    line_count: int = Field(
        description=(
            "Lines in the decoded text, counted with splitlines -- so a file with no "
            "trailing newline counts its last line."
        ),
    )
    cited_urls: list[str] = Field(
        default_factory=list,
        description=(
            "Every http(s) URL the material cites, deduplicated, in order of first "
            "appearance. AN EMPTY LIST MEANS THE FILE CITED NOTHING, which is a "
            "finding about the material and not an error. It does NOT mean the URLs "
            "were checked -- none of them were fetched."
        ),
    )
    diagnostics: Diagnostics


class Refusal(BaseModel):
    """A refusal arrives as a normal result with an `error` field, not as an error.

    Point 6 of the house standard: an agent formats whatever it is handed, so a
    refusal that arrives as a transport-level exception gets summarised as "the
    tool failed" and the remedy is lost. This shape keeps the remedy in the payload.
    """

    error: Literal[
        "invalid_input",
        "outside_root",
        "not_found",
        "not_a_file",
        "too_large",
        "undecodable",
    ] = Field(description="Which refusal this is. Branch on it rather than on prose.")
    message: str = Field(description="What went wrong, in one sentence.")
    guidance: str = Field(
        description=(
            "What to do next. Follow this instead of retrying the same call -- every "
            "refusal here is deterministic, so an identical retry refuses identically."
        ),
    )
    diagnostics: Diagnostics
