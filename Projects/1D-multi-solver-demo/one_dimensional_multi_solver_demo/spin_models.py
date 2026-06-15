"""Small model builders used by the method-consumption probe."""

from __future__ import annotations

from .spin_system import (
    Bond,
    HamiltonianTerm,
    OperatorOnSite,
    Site,
    SpinSystem,
    spin_half_space,
)


def _validate_length(length: int) -> int:
    length = int(length)
    if length < 2:
        raise ValueError("length must be at least 2.")
    return length


def _validate_bc(bc: str) -> str:
    bc = str(bc).lower()
    if bc not in {"open", "periodic"}:
        raise ValueError("bc must be 'open' or 'periodic'.")
    return bc


def _chain_sites(length: int) -> tuple[Site, ...]:
    return tuple(Site(index=i, coordinate=(float(i),), label=f"s{i}") for i in range(length))


def _chain_bonds(length: int, bc: str) -> tuple[Bond, ...]:
    bonds = [Bond(i, i + 1) for i in range(length - 1)]
    if bc == "periodic":
        bonds.append(Bond(length - 1, 0, boundary=True))
    return tuple(bonds)


def build_xxz_chain(
    *,
    length: int,
    bc: str = "open",
    jxy: float = 1.0,
    jz: float = 0.0,
    hz: float = 0.0,
    hx: float = 0.0,
) -> SpinSystem:
    """Build the first-slice XXZ plus Zeeman spin system."""

    length = _validate_length(length)
    bc = _validate_bc(bc)
    sites = _chain_sites(length)
    bonds = _chain_bonds(length, bc)
    terms: list[HamiltonianTerm] = []

    for bond in bonds:
        i, j = bond.as_tuple()
        if jxy:
            terms.append(
                HamiltonianTerm(
                    label="xx_exchange",
                    coefficient=complex(jxy),
                    operators=(OperatorOnSite("Sx", i), OperatorOnSite("Sx", j)),
                )
            )
            terms.append(
                HamiltonianTerm(
                    label="yy_exchange",
                    coefficient=complex(jxy),
                    operators=(OperatorOnSite("Sy", i), OperatorOnSite("Sy", j)),
                )
            )
        if jz:
            terms.append(
                HamiltonianTerm(
                    label="zz_exchange",
                    coefficient=complex(jz),
                    operators=(OperatorOnSite("Sz", i), OperatorOnSite("Sz", j)),
                )
            )

    for site in sites:
        if hz:
            terms.append(
                HamiltonianTerm(
                    label="longitudinal_field",
                    coefficient=complex(-hz),
                    operators=(OperatorOnSite("Sz", site.index),),
                )
            )
        if hx:
            terms.append(
                HamiltonianTerm(
                    label="transverse_field",
                    coefficient=complex(-hx),
                    operators=(OperatorOnSite("Sx", site.index),),
                )
            )

    return SpinSystem(
        name="xxz_chain",
        local_space=spin_half_space(),
        sites=sites,
        bonds=bonds,
        terms=tuple(terms),
        bc=bc,
        metadata={
            "model_family": "xxz",
            "length": length,
            "jxy": float(jxy),
            "jz": float(jz),
            "hz": float(hz),
            "hx": float(hx),
            "cluster_coupling": 0.0,
        },
    )

