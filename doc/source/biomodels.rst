


.. seealso:: :class:`bioservices.biomodels.BioModels` for the full reference guide.


.. _biomodels_tutorial:

Biomodels tutorial
======================

Start a biomodels interface:


.. testsetup:: biomodels

    from bioservices import BioModels
    s = BioModels()


.. doctest:: biomodels

    >>> from bioservices import BioModels
    >>> s = BioModels()

look at the list of models Id::

    print s.modelsId

Get a specific model given its Id. Let us play with the first model:

.. doctest:: biomodels

    >>> s.modelsId[0]
    'BIOMD0000000299'

and look at some meta information:

.. doctest:: biomodels
    :options: +SKIP

    >>> print s.getSimpleModelsByIds(s.modelsId[0])
    <?xml version="1.0" encoding="UTF-8"?>
    <simpleModels>
    <simpleModel>
        <referenceId>10643740</referenceId>
        <modelId>BIOMD0000000299</modelId>
        <modelSubmissionId>MODEL1101140000</modelSubmissionId>
        <modelName>Leloup1999_CircadianRhythms_Neurospora</modelName>
        <publicationId>10643740</publicationId>
        <authors>
            <author>Leloup JC</author>
            <author>Gonze D</author>
            <author>Goldbeter A</author>
        </authors>
        <encoders>
            <encoder>Catherine Lloyd</encoder>
            <encoder>Vijayalakshmi Chelliah</encoder>
        </encoders>
        <lastModificationDate>2011-01-18T12:23:47+00:00</lastModificationDate>
    </simpleModel>
    </simpleModels>
    


Some of these information can be retrieved specifically:

.. doctest:: biomodels

    >>> ID = s.modelsId[0]
    >>> print s.getPublicationByModelId(ID)
    10643740


