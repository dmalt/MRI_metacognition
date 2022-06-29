#!/bin/bash
#SBATCH --job-name=fsf            # Название задачи 
#SBATCH --error=fsf-%j.err        # Файл для вывода ошибок 
#SBATCH --output=fsf-%j.log       # Файл для вывода результатов 
#SBATCH --time=20:10:00                      # Максимальное время выполнения 
#SBATCH --cpus-per-task=36                  # Количество CPU на одну задачу 

source deactivate
source activate fsf
echo "Working on node `hostname`"
srun --cpus-per-task=36 doit -n 36 -c                # Выполнение расчёта
