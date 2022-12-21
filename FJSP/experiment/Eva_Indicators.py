'''
评价指标
IGD指标值:通过计算每个参考点到最近的解距离的平均值得到，能同时反应解的收敛性和多样性，值越小说明算法收敛效果及多样性越好。

Spacing指标值：通过计算每个解到其他解的最小距离的标准差来反应解集的分布性，Spacing值越小，说明解的分布越均匀。

'''
############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Multivariate Indicators

# Citation:
# PEREIRA, V. (2022). GitHub repository: <https://github.com/Valdecy/pyMultiojective>

############################################################################

# Required Libraries
import itertools
import numpy as np
# import pygmo as pg

from scipy import spatial



# IGD - Inverted Generational Distance
# Function: IGD
def igd_indicator(sol,front):
    d_i = [(spatial.KDTree(sol).query(front[i, :])) for i in range(0, front.shape[0])]
    d = [item[0] for item in d_i]
    igd = np.sqrt(sum(d)) / len(d)
    return igd

# SP - Spacing
# Function:  Spacing
def sp_indicator(sol):
    dm = np.zeros(sol.shape[0])
    for i in range(0, sol.shape[0]):
        dm[i] = min([np.linalg.norm(sol[i] - sol[j]) for j in range(0, sol.shape[0]) if i != j])
    d_mean = np.mean(dm)
    spacing = np.sqrt(np.sum((dm - d_mean) ** 2) / sol.shape[0])
    return spacing
#
#
# # Hypervolume (S-Metric
# # Function: Hypervolume
def hv_indicator(sol):
    ref_point = [np.max(sol[:, j]) for j in range(0, sol.shape[1])]
    hv_c = pg.hypervolume(sol)
    hv = hv_c.compute(ref_point)
    return hv
