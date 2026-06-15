"""Print the first method-consumption probe for one shared SpinSystem."""

from one_dimensional_multi_solver_demo import ED, NQS, TN, QuadHam, build_xxz_chain, change_form


def main() -> None:
    system = build_xxz_chain(length=4, bc="periodic", jxy=1.0, jz=0.0)

    print(f"system: {system.name}, L={system.length}, bc={system.bc}")
    print(f"bonds: {system.bond_tuples()}")
    print()

    for method in (ED, TN, NQS, QuadHam):
        form = change_form(system, method)
        print(f"{method.label}: {form.status}")
        print(f"  consumed: {', '.join(form.consumed)}")
        if form.required_extra:
            print(f"  required_extra: {', '.join(form.required_extra)}")
        if form.dropped:
            print(f"  dropped: {', '.join(form.dropped)}")
        print(f"  payload_keys: {', '.join(form.payload.keys())}")
        for note in form.notes:
            print(f"  note: {note}")
        print()


if __name__ == "__main__":
    main()

