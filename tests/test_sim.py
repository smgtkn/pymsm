def test_msm_sim():
    # Load Rotterdam data and fit a model
    from pymsm.datasets import prep_rotterdam

    dataset, states_labels = prep_rotterdam()
    terminal_states = [3]
    from pymsm.multi_state_competing_risks_model import (
        MultiStateModel,
        default_update_covariates_function,
    )

    multi_state_model = MultiStateModel(
        dataset, terminal_states, default_update_covariates_function
    )
    multi_state_model.fit()

    # Extract the model parameters
    from pymsm.simulation import extract_competing_risks_models_list_from_msm

    competing_risks_models_list = extract_competing_risks_models_list_from_msm(
        multi_state_model, verbose=True
    )

    from pymsm.simulation import MultiStateSimulator

    # Configure the simulator
    mssim = MultiStateSimulator(
        competing_risks_models_list,
        terminal_states=terminal_states,
        update_covariates_fn=default_update_covariates_function,
        covariate_names=[
            "year",
            "age",
            "meno",
            "grade",
            "nodes",
            "pgr",
            "er",
            "hormon",
            "chemo",
        ],
    )

    # Run MC for a sample single patient
    sim_paths = mssim.run_monte_carlo_simulation(
        sample_covariates=dataset[0].covariates.values,
        origin_state=1,
        current_time=2,
        n_random_samples=3,
        max_transitions=10,
        print_paths=True,
        n_jobs=1,
    )
