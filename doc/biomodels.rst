


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

look at the list of model identifiers::

    models = s.get_all_models()


If you have a specific model identifier, then it is easy. You can 
retrieve the model itself::

    model s.get_model("BIOMD0000000100")

and get its name or other types of information::

    >>> model['name']
    Rozi2003_GlycogenPhosphorylase_Activation

In particular, description, author and files associated with this model. Here,
we can see the files and in particular a PNG image called
**BIOMD0000000100.png**. You can get it as follows::

    s.get_model_download("BIOMD0000000100", filename="BIOMD0000000100.png")

or just download the whole bundle::
    
    s.get_model_download("BIOMD0000000100")

saved into **BIOMD0000000100.zip**.




