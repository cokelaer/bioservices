

.. contents::


.. _biomodels_tutorial:

Introduction
--------------
Start a biomodels interface:


.. doctest::

    from bioservices.biomodels import BioModels
    b = BioModels()

look at the list of models Id::

    print b.modelsId

Get a specific model given its Id. Let us play with the first model::

    >>> ID = b.modelsId[0]
    >>> ID
    'BIOMD0000000299'

and look at some meta information::


    >>> print b.getSimpleModelById(b.modelsId[0])
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

Some of these information can be retrieved specifically::


    >>> print b.getPublicationByModelId(ID)
    '10643740'


