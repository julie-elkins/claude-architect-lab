"""Course Doctor -- checks training material against live documentation.

The design goal is the one that sounds backwards: it has to report what it could
NOT check. When a fetch fails or a file cannot be read, most tools return a report
that looks clean, and a clean report is indistinguishable from a healthy one. So
every result here carries what it does not cover, and `unchecked` is a state this
package is not allowed to collapse into `fine`.

Built across the five episodes of the Build to Pass course. Episode 1 is this
module plus `materials.py` and the single `read_material` tool: read a lesson,
hash it, and find out which documentation it depends on. Nothing here reaches the
network -- that arrives in episode 2, along with the error taxonomy that network
failures are the reason for.
"""

__version__ = "0.1.0"
