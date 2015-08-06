#!/usr/bin/python
#
# py_bonemat_abaqus - run
# ==========================
#
# Version: 1.0.1
# Created by Elise Pegg, University of Oxford, Aug 2015

__all__ = ['run']

#-------------------------------------------------------------------------------
# Import modules
#-------------------------------------------------------------------------------
import sys, os
from py_bonemat_abaqus import general, data_import, calc, data_output

#-------------------------------------------------------------------------------
# Define run program
#-------------------------------------------------------------------------------
def run(argv0, argv1, argv2):
    print("""
    ************** PY_BONEMAT ABAQUS 1.0.1 ************
    ** Elise Pegg,  University of Oxford,   Aug 2015 **
    ***************************************************
    """)
    
    #---------------------------------------------------------------------------
    # check input arguments
    #---------------------------------------------------------------------------
    argv = [argv0, argv1, argv2]
    if general.check_argv(argv) == False:
        sys.exit(1)
    param_file = argv[0]
    ct_data = argv[1]
    mesh_file = argv[2]
        
    #---------------------------------------------------------------------------
    # Import parameters
    #---------------------------------------------------------------------------
    param = data_import.import_parameters(param_file)

    #---------------------------------------------------------------------------
    # Import Abaqus input file data
    #---------------------------------------------------------------------------
    print("    Importing mesh file: " + mesh_file)
    parts = data_import.import_mesh(mesh_file, param)

    #---------------------------------------------------------------------------
    # Import CT data
    #---------------------------------------------------------------------------
    print("    Importing CT data: " + ct_data)
    vtk_data = data_import.import_ct_data(ct_data)
    
    #---------------------------------------------------------------------------
    # Determine material properties for elements within each part
    #---------------------------------------------------------------------------
    print("    Calculating material properties [- may take some time]")
    parts = calc.calc_mat_props(parts, param, vtk_data)

    #---------------------------------------------------------------------------
    # Write data to new abaqus input file
    #---------------------------------------------------------------------------
    print("    Writing material data to new abaqus input file:")
    print("\t" + mesh_file[:-4] + "MAT.inp")
    data_output.output_abq_inp(parts, mesh_file, param['poisson'])

    #---------------------------------------------------------------------------
    # End
    #---------------------------------------------------------------------------
    print("""
    **   !!! Bone material assignment complete !!!   **
    ***************************************************
    """)
