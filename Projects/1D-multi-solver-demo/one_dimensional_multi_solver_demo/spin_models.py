"""Small model builders used by the method-consumption probe and ED app."""

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


def _cluster_supports(length: int, bc: str) -> tuple[tuple[int, int, int], ...]:
    if bc == "periodic":
        return tuple(((center - 1) % length, center, (center + 1) % length) for center in range(length))
    return tuple((center - 1, center, center + 1) for center in range(1, length - 1))


def _model_family(*, jxy: float, jz: float, k: float, hz: float, hx: float) -> str:
    tol = 1e-15
    has_xxz_or_field = any(abs(value) > tol for value in (jxy, jz, hz, hx))
    has_cluster = abs(k) > tol
    if has_cluster and not has_xxz_or_field:
        return "cluster_ising"
    if not has_cluster:
        return "xxz"
    return "general"


def build_spin_chain(
    *,
    length: int,
    bc: str = "open",
    jxy: float = 1.0,
    jz: float = 0.0,
    k: float = 0.0,
    hz: float = 0.0,
    hx: float = 0.0,
) -> SpinSystem:
    """Build the XXZ + cluster + Zeeman 1D spin-chain family.

    The cluster term follows the project convention
    ``-K Sx_{i-1} Sz_i Sx_{i+1}``. Under open boundary conditions only bulk
    centers ``i=1..L-2`` are included; under periodic boundary conditions site
    indices are read modulo ``L``.
    """

    length = _validate_length(length)
    bc = _validate_bc(bc)
    if k and length < 3:
        raise ValueError("cluster coupling requires length at least 3.")
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

    if k:
        for left, center, right in _cluster_supports(length, bc):
            terms.append(
                HamiltonianTerm(
                    label="cluster",
                    coefficient=complex(-k),
                    operators=(
                        OperatorOnSite("Sx", left),
                        OperatorOnSite("Sz", center),
                        OperatorOnSite("Sx", right),
                    ),
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

    family = _model_family(jxy=jxy, jz=jz, k=k, hz=hz, hx=hx)
    return SpinSystem(
        name=f"{family}_chain",
        local_space=spin_half_space(),
        sites=sites,
        bonds=bonds,
        terms=tuple(terms),
        bc=bc,
        metadata={
            "model_family": family,
            "length": length,
            "jxy": float(jxy),
            "jz": float(jz),
            "hz": float(hz),
            "hx": float(hx),
            "cluster_coupling": float(k),
            "k": float(k),
            "cluster_obc_rule": "bulk_only" if bc == "open" else "modulo_periodic",
        },
    )


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

    system = build_spin_chain(length=length, bc=bc, jxy=jxy, jz=jz, k=0.0, hz=hz, hx=hx)
    return SpinSystem(
        name="xxz_chain",
        local_space=system.local_space,
        sites=system.sites,
        bonds=system.bonds,
        terms=system.terms,
        bc=system.bc,
        metadata=system.metadata,
    )
