from pathlib import Path

import numpy as np

from csst.experiment.models import PropertyValue
from csst.experiment import load_experiments_from_folder
from .fixtures.data import csste_1014, manual_1014  # noqa: F401


def test_experiment_init_from_file_version_1014(csste_1014, manual_1014):  # noqa: F811
    """csste_1014 is the loaded data, manual_1014 is manually read data from the
    data file csste_1014 reads from
    """
    # test headers
    assert csste_1014.file_name == manual_1014.file_name
    assert csste_1014.experiment_details == manual_1014.experiment_details
    assert csste_1014.experiment_number == manual_1014.experiment_number
    assert csste_1014.experimenter == manual_1014.experimenter
    assert csste_1014.project == manual_1014.project
    assert csste_1014.lab_journal == manual_1014.lab_journal
    assert csste_1014.description == manual_1014.description
    assert csste_1014.start_of_experiment == manual_1014.start_of_experiment

    assert csste_1014.temperature_program.block == manual_1014.temperature_program.block
    assert csste_1014.bottom_stir_rate == manual_1014.bottom_stir_rate
    assert len(manual_1014.temperature_program.solvent_tune) == len(
        csste_1014.temperature_program.solvent_tune
    )
    for i in range(len(csste_1014.temperature_program.solvent_tune)):
        assert (
            manual_1014.temperature_program.solvent_tune[i]
            == csste_1014.temperature_program.solvent_tune[i]
        )

    assert len(manual_1014.temperature_program.sample_load) == len(
        csste_1014.temperature_program.sample_load
    )
    for i in range(len(csste_1014.temperature_program.sample_load)):
        assert (
            manual_1014.temperature_program.sample_load[i]
            == csste_1014.temperature_program.sample_load[i]
        )

    assert len(manual_1014.temperature_program.experiment) == len(
        csste_1014.temperature_program.experiment
    )
    for i in range(len(csste_1014.temperature_program.experiment)):
        assert (
            manual_1014.temperature_program.experiment[i]
            == csste_1014.temperature_program.experiment[i]
        )

    assert manual_1014.temperature_program == csste_1014.temperature_program

    datablock_size = 32337 - 38
    assert len(csste_1014.time_since_experiment_start.values) == datablock_size

    assert csste_1014.set_temperature.unit == "°C"
    assert len(csste_1014.set_temperature.values) == datablock_size

    assert csste_1014.actual_temperature.unit == "°C"
    assert len(csste_1014.actual_temperature.values) == datablock_size
    assert not np.array_equal(
        csste_1014.actual_temperature.values, csste_1014.set_temperature.values
    )

    assert csste_1014.stir_rates.unit == "rpm"
    assert len(csste_1014.stir_rates.values) == datablock_size

    assert len(csste_1014.reactors) == 3
    for i in range(len(csste_1014.reactors)):
        reactor = csste_1014.reactors[i]
        assert len(reactor.transmission.values) == datablock_size
        assert reactor.reactor_number == i + 1
        if i == 0:
            assert reactor.polymer == "PEG"
            assert reactor.polymer_id == 34
            assert reactor.conc == PropertyValue(
                name="concentration", value=5.11, unit="mg/ml"
            )
            assert reactor.solvent == "1,2dichlorobenzene"
            assert reactor.solvent_id == 37
        if i == 1:
            assert reactor.polymer == "PEO"
            assert reactor.polymer_id == 46
            assert reactor.conc == PropertyValue(
                name="concentration", value=5.19, unit="mg/ml"
            )
            assert reactor.solvent == "Ethyl Acetate"
            assert reactor.solvent_id == 19
        if i == 2:
            assert reactor.polymer == "PVP"
            assert reactor.polymer_id == 41
            assert reactor.conc == PropertyValue(
                name="concentration", value=5.10, unit="mg/ml"
            )
            assert reactor.solvent == "MeOH"
            assert reactor.solvent_id == 3

    csste_1014.reactors[0].experiment.actual_temperature.values[0] = 10000
    assert csste_1014.reactors[1].experiment.actual_temperature.values[0] == 10000
    csste_1014.reactors[0].experiment.actual_temperature.values[0] = 1
    assert csste_1014.reactors[1].experiment.actual_temperature.values[0] == 1


def test_temperature_program_hash(manual_1014):  # noqa: F811
    """This test will fail if the manual_1014 temperature program is changed at all"""
    assert manual_1014.temperature_program.hash() == "baa4a0e932fb273023e33317e51a5cc8"


def test_load_experiments_from_folder():
    folder = str(Path(__file__).parent.absolute() / "test_data")
    assert len(load_experiments_from_folder(folder)) == 2
    assert len(load_experiments_from_folder(folder, recursive=True)) == 3
