"""READMESection model - single entry section within README."""
from dataclasses import dataclass


@dataclass(frozen=True)
class READMESection:
    """Single entry section within the README.

    Immutable value object representing one gallery entry's documentation.
    """
    entry_name: str
    command_content: str
    plot_path: str

    def render(self) -> str:
        """Generate markdown section for this entry.

        Returns:
            Formatted markdown string for one gallery entry section
        """
        return f"""## Entry: {self.entry_name}

```bash
{self.command_content}```

![Plot]({self.plot_path})

---
"""
