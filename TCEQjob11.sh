#!/bin/bash
#PBS -l walltime=60:00:00
#PBS -M vwarger@ufl.edu
#PBS -m bea
#PBS -q submit
#PBS -N basecase
#PBS -l nodes=1:ppn=8
export OMP_NUM_THREADS=8
cd ${PBS_O_WORKDIR}
for today in *.namelist
do
echo $today
  if [ ! -e ../output/camx453_cb05.${today}.hgb8h2.bc06aqs1.reg11si_MVS.2006ep1_eta_dbemis_fddats_newuhsst_newutcsrlulc_grell.avrg.grd01 ]; then
    ln -fs ${today} CAMx.in
    echo running
    time ../../../src/CAMx.hgb8h2.i_linuxomp 1> ../output/${today%.control.namelist}.stdout 2> ../output/${today%.control.namelist}.stderr
    if [ $? -ne 0 ]; then
    echo "Failed on $today"
    fi
  fi
done
