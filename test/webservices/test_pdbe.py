from bioservices import PDBe





def test_pdbe():
    p = PDBe(verbose=False)
    res = p.get_summary('1cbs')
    assert len(res)==1
    res = p.get_summary('1cbs,2kv8')
    assert len(res)==2
    res = p.get_summary(['1cbs', '2kv8'])
    assert len(res)==2

    p.get_molecules('1cbs')
    p.get_molecules('1cbs,2kv8')

    p.get_related_publications('1cbs')
    p.get_related_publications('1cbs')

    p.get_experiment('1cbs')
    p.get_experiment('1cbs,2kv8')

    p.get_nmr_resources('1cbs')
    p.get_nmr_resources('1cbs,2kv8')

    p.get_ligand_monomers('1cbs')
    p.get_ligand_monomers('1cbs,2kv8')

    p.get_modified_residues('4v5j')
    p.get_modified_residues('4v5j,1cbs')

    p.get_mutated_residues('1bgj')
    p.get_mutated_residues('1bgj,4v5j')

    p.get_release_status('1cbs')
    p.get_release_status('1cbs,4v5j')

    p.get_observed_ranges('1cbs')
    p.get_observed_ranges('1cbs,4v5j')

    p.get_observed_ranges_in_pdb_chain('1cbs', "A")

    p.get_secondary_structure('1cbs')
    p.get_secondary_structure('1cbs,4v5j')

    p.get_residue_listing('1cbs')

    p.get_residue_listing_in_pdb_chain('1cbs', "A")

    p.get_binding_sites('1cbs')
    p.get_binding_sites('1cbs,4v5j')

    p.get_files('1cbs')
    p.get_files('1cbs,4v5j')

    p.get_observed_residues_ratio('1cbs')
    p.get_observed_residues_ratio('1cbs,4v5j')

    p.get_assembly('1cbs')
    p.get_assembly('1cbs,4v5j')

    p.get_electron_density_statistics('1cbs')
    p.get_electron_density_statistics('1cbs,4v5j')

    p.get_drugbank_annotation('5hht')
    p.get_drugbank_annotation('5hht,5hht')

    p.get_functional_annotation('1cbs,1cbs')
    p.get_functional_annotation('1cbs')

    p.get_related_dataset('5o8b')
    p.get_related_dataset('5o8b,5o8b')


