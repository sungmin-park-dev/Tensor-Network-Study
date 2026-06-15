"""Tests for SpinSystem to method-form exports."""

import numpy as np

from one_dimensional_multi_solver_demo import ED, NQS, TN, QuadHam, build_xxz_chain, change_form


def test_spin_system_keeps_geometry_and_terms_method_independent():
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0, jz=0.0)

    assert system.length == 4
    assert system.bc == "periodic"
    assert system.bond_tuples() == ((0, 1), (1, 2), (2, 3), (3, 0))
    assert system.bonds[-1].boundary
    assert [term.label for term in system.terms] == [
        "xx_exchange",
        "yy_exchange",
        "xx_exchange",
        "yy_exchange",
        "xx_exchange",
        "yy_exchange",
        "xx_exchange",
        "yy_exchange",
    ]


def test_ed_form_consumes_many_body_basis_and_local_matrices():
    system = build_xxz_chain(length=4, bc="open", jxy=1.0)
    form = change_form(system, ED)

    assert form.status == "ready"
    assert form.payload["basis"]["dimension"] == 16
    assert form.payload["local_operator_matrices"]["Sx"].shape == (2, 2)
    assert len(form.payload["matrix_terms"]) == 6
    assert "local_space.operators" in form.consumed


def test_tn_form_keeps_named_operator_terms_and_bonds():
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0)
    form = change_form(system, TN)

    assert form.status == "ready"
    assert "backend_site_class" in form.required_extra
    assert form.payload["operator_names"] == ("I", "Sx", "Sy", "Sz", "Sp", "Sm")
    assert form.payload["bonds"][-1]["boundary"] is True
    assert form.payload["mpo_terms"][0]["operators"] == (
        {"name": "Sx", "site": 0},
        {"name": "Sx", "site": 1},
    )


def test_nqs_form_exposes_graph_hilbert_and_local_operator_split():
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0)
    form = change_form(system, NQS)

    assert form.status == "ready"
    assert form.payload["graph"]["edges"] == ((0, 1), (1, 2), (2, 3), (3, 0))
    assert form.payload["hilbert"]["local_states"] == ("up", "down")
    assert "random_seed" in form.required_extra


def test_quad_ham_open_xx_chain_exports_numeric_hopping_matrix():
    system = build_xxz_chain(length=4, bc="open", jxy=1.0, jz=0.0, hz=0.0, hx=0.0)
    form = change_form(system, QuadHam)
    hopping = form.payload["hopping_matrix"]

    expected = np.array(
        [
            [0.0, 0.5, 0.0, 0.0],
            [0.5, 0.0, 0.5, 0.0],
            [0.0, 0.5, 0.0, 0.5],
            [0.0, 0.0, 0.5, 0.0],
        ],
        dtype=complex,
    )

    assert form.status == "ready"
    assert not form.required_extra
    assert np.allclose(hopping, expected)


def test_quad_ham_periodic_xx_chain_surfaces_jw_boundary_sector():
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0, jz=0.0, hz=0.0, hx=0.0)
    form = change_form(system, QuadHam)
    hopping = form.payload["hopping_matrix"]

    assert form.status == "partial"
    assert "fermion_parity_sector" in form.required_extra
    assert form.payload["boundary_terms"] == (
        {
            "sites": (3, 0),
            "spin_amplitude": 0.5,
            "fermion_amplitude": "-Pi * Jxy / 2 after JW sector choice",
        },
    )
    assert hopping[3, 0] == 0.0
    assert hopping[0, 3] == 0.0


def test_quad_ham_rejects_interacting_xxz_as_non_quadratic():
    system = build_xxz_chain(length=4, bc="open", jxy=1.0, jz=1.0)
    form = change_form(system, QuadHam)

    assert form.status == "not_applicable"
    assert "jz_interaction" in form.payload["unsupported_features"]
    assert "noninteracting_or_jw_quadratic_mapping" in form.required_extra

