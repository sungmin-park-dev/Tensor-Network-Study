"""Tests for the generalized 1D spin-chain builder."""

from one_dimensional_multi_solver_demo import build_spin_chain, build_xxz_chain


def test_build_xxz_chain_stays_as_legacy_wrapper():
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0, jz=0.5)

    assert system.name == "xxz_chain"
    assert system.metadata["model_family"] == "xxz"
    assert system.metadata["cluster_coupling"] == 0.0


def test_cluster_obc_uses_bulk_centers_only():
    system = build_spin_chain(length=6, bc="open", jxy=0.0, jz=0.0, k=2.0)
    cluster_terms = [term for term in system.terms if term.label == "cluster"]

    assert len(cluster_terms) == 4
    assert [term.support() for term in cluster_terms] == [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
    assert system.metadata["cluster_obc_rule"] == "bulk_only"


def test_cluster_pbc_uses_modulo_centers():
    system = build_spin_chain(length=4, bc="periodic", jxy=0.0, jz=0.0, k=2.0)
    cluster_terms = [term for term in system.terms if term.label == "cluster"]

    assert len(cluster_terms) == 4
    assert [term.support() for term in cluster_terms] == [(3, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, 0)]
    assert system.metadata["cluster_obc_rule"] == "modulo_periodic"
