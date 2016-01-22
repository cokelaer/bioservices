from bioservices import ENA



def test_ena():


    e = ENA()

    e.get_data('ERA000092', 'xml')
    e.get_data('ERA000092', 'text')
    e.get_data('ERA000092', 'fasta')


    res = e.get_data('ERA000092', 'fasta', fasta_range=[3,63])


    e.get_data('AL513382', frmt='text', expanded=True)


    e.get_data('BN000065', 'text', header=True)

    e.get_data('AM407889.1', 'fasta')
    e.get_data('AM407889.2', 'fasta')

    


